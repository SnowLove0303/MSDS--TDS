# -*- coding: utf-8 -*-
"""MSDS SQLite 标准字段库 CLI (build_msds_db).

以「父子级 + 标签」结构表为模型, 把 MSDS docx / 透视总表 xlsx 入库为
SQLite 四表: schema_field 标准字段字典 / msds_model 型号主表 /
msds_field 明细长表 / msds_wide Schema 宽表.

用法:
  python tools/build_msds_db.py <db路径> <docx或目录...> [--from-xlsx 透视表.xlsx...]
  python tools/build_msds_db.py <db路径> --list                 # 列出全部型号
  python tools/build_msds_db.py <db路径> --model <型号> [--json|--tsv] [--sections 1,9]   # 按型号检索 (三级树)
  python tools/build_msds_db.py <db路径> --model-search <关键词> [--sections 1,9]          # 关键词检索库内数据
  python tools/build_msds_db.py <db路径> --query 关键词          # 检索
  python tools/build_msds_db.py <db路径> --wide <型号>           # 宽表一行
  python tools/build_msds_db.py <db路径> --init                 # 仅重建表结构

示例:
  python tools/build_msds_db.py "../../数据库/正式库/Data Base/msds_standard.db" ^
      "templates/MSDS_CN 国彩 模板.docx" --from-xlsx "../../数据库/正式库/标准字段数据库Excel/导出表/PEA-4139 MSDS_CN 冠志 模板_信息_20260817_085127.xlsx"
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.msds_db import (find_models, insert_docx, insert_pivot_xlsx,
                          list_models, model_detail, model_search, open_db,
                          render_model_json, render_model_tree,
                          render_model_tsv, search, wide_row)


def _collect_docx(inputs: list[str]) -> list[Path]:
    """docx 或目录展开 (排除 ~$ 临时文件 / 输出·模板·正文 等非数据文件)."""
    out: list[Path] = []
    for raw in inputs:
        p = Path(raw)
        if p.is_dir():
            out.extend(sorted(f for f in p.glob("*.docx")
                              if not f.name.startswith("~$")))
        elif p.exists() and p.suffix.lower() == ".docx":
            out.append(p)
        else:
            print(f"  ⚠️ 跳过 (非 docx 或不存在): {p}")
    return sorted(set(out), key=lambda x: str(x).lower())


def _parse_sections(rest: list[str]) -> set[int] | None:
    """解析 --sections 1,3,9 → {1,3,9}; 缺省 None (全部)."""
    if "--sections" in rest:
        i = rest.index("--sections")
        if i + 1 < len(rest):
            s = {int(x) for x in rest[i + 1].split(",") if x.strip().isdigit()}
            return s or None
    return None


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    db_path = args[0]
    rest = args[1:]

    # 结构写死: 每次运行强制校验冻结结构 (防其他线程/Agent 改动 schema/骨架)
    from core.msds_db import validate_structure
    try:
        validate_structure()
    except RuntimeError as exc:
        print(str(exc))
        return 3

    # 只读子命令
    db = open_db(db_path)
    if "--list" in rest or "--models" in rest:
        for model, src, file_, n, ts in list_models(db):
            print(f"  {model:<16} [{src}] {n:>3} 行 | {file_}")
        return 0
    if "--model" in rest:
        # 按型号检索 (唯一索引): 三级树 / JSON / TSV, 支持 --sections 范围过滤与 --s9-clean 过滤无数据
        q = rest[rest.index("--model") + 1]
        hits = find_models(db, q)
        if not hits:
            print(f"  ✗ 库中无此型号: {q}")
            return 1
        mid, model, src, file_, n, ts = hits[0]
        sections = _parse_sections(rest)
        s9_active_only = ("--s9-clean" in rest or "--active-only" in rest or "--clean" in rest)
        out_path = rest[rest.index("--out") + 1] if ("--out" in rest and rest.index("--out") + 1 < len(rest)) else None
        if "--write-items" in rest:
            from core.msds_db import model_to_write_items
            items = model_to_write_items(db, mid, s9_active_only=True)
            import json as _json
            dumped = _json.dumps(items, ensure_ascii=False, indent=2)
            if out_path:
                Path(out_path).write_text(dumped, encoding="utf-8")
                print(f"✅ 覆写写入项已导出 → {out_path} (S9 有效字段 {len(items['sections'].get('9', []))} 项)")
            else:
                print(dumped)
            return 0
        if "--json" in rest:
            txt = render_model_json(db, mid, sections, s9_active_only=s9_active_only)
        elif "--tsv" in rest:
            txt = render_model_tsv(db, mid, sections, s9_active_only=s9_active_only)
        else:
            d = model_detail(db, mid)
            header = f"型号: {model} | 来源: {src} | 明细 {n} 行 | 入库: {ts}\n"
            if d.get("sha256"):
                header += f"sha256: {d['sha256'][:16]}… | 文件: {file_}\n"
            txt = header + render_model_tree(db, mid, sections, s9_active_only=s9_active_only)
        if out_path:
            enc = "utf-8-sig" if "--tsv" in rest else "utf-8"
            Path(out_path).write_text(txt, encoding=enc)
            print(f"✅ 已导出 → {out_path}")
        else:
            print(txt)
        return 0
    if "--model-search" in rest:
        # 关键词检索库内数据 → 命中型号清单 + 节/标签位置
        q = rest[rest.index("--model-search") + 1]
        sections = _parse_sections(rest)
        hits = model_search(db, q, sections)
        if not hits:
            print(f"  ✗ 无匹配: {q}")
            return 1
        by_model: dict[str, list] = {}
        for model, mid, sec, seq, label, value, kind, std_name in hits:
            by_model.setdefault(model, []).append((sec, seq, label, value, kind, std_name))
        for model, items in by_model.items():
            print(f"== {model} ({len(items)} 处命中) ==")
            for sec, seq, label, value, kind, std_name in items:
                tag = (std_name if (sec == 3 and kind == "component" and std_name) else (label or kind))
                print(f"   S{sec} {seq:<5} {tag:<30} {value}")
        return 0
    if "--query" in rest:
        q = rest[rest.index("--query") + 1]
        for model, sec, seq, label, value in search(db, q):
            print(f"  {model:<16} S{sec} {seq:<5} {label:<24} {value}")
        return 0
    if "--wide" in rest:
        model_name = rest[rest.index("--wide") + 1]
        row = db.execute(
            "SELECT model_id FROM msds_model WHERE model=? ORDER BY model_id LIMIT 1",
            (model_name,)).fetchone()
        if not row:
            print(f"  ✗ 未找到型号: {model_name}")
            return 1
        vals = wide_row(db, row[0])
        for k in sorted(vals):
            print(f"  {k:<34} = {vals[k][:80].replace(chr(10), ' / ')}")
        return 0
    if "--init" in rest:
        # 真正重建表结构 (schema 变更后使用): DROP msds_wide + 重灌 schema_field
        from core.msds_db import init_db
        init_db(db)
        print(f"  ✅ 表结构已重建: {db_path} (schema_field 字典 {db.execute('SELECT COUNT(*) FROM schema_field').fetchone()[0]} 项)")
        return 0

    # 入库
    xlsx_inputs: list[str] = []
    docx_inputs: list[str] = []
    i = 0
    while i < len(rest):
        if rest[i] == "--from-xlsx":
            xlsx_inputs.extend(rest[i + 1:])
            break
        docx_inputs.append(rest[i])
        i += 1

    if not docx_inputs and not xlsx_inputs:
        print(__doc__)
        return 2

    files = _collect_docx(docx_inputs)
    print(f"  docx {len(files)} 份 | xlsx 透视表 {len(xlsx_inputs)} 份 → {db_path}")

    from core.msds_db import wide_columns
    cols = wide_columns()

    failed = []
    for p in files:
        try:
            mid = insert_docx(db, p, cols)
            print(f"  ✓ {p.name} (model_id={mid})")
        except Exception as exc:
            failed.append((p.name, str(exc)))
            print(f"  ✗ {p.name}: {exc}")
    for x in xlsx_inputs:
        try:
            mid = insert_pivot_xlsx(db, x, cols)
            print(f"  ✓ xlsx {Path(x).name} (model_id={mid})")
        except Exception as exc:
            failed.append((Path(x).name, str(exc)))
            print(f"  ✗ xlsx {Path(x).name}: {exc}")

    n_model = db.execute("SELECT COUNT(*) FROM msds_model").fetchone()[0]
    n_field = db.execute("SELECT COUNT(*) FROM msds_field").fetchone()[0]
    n_wide = db.execute("SELECT COUNT(*) FROM msds_wide").fetchone()[0]
    print(f"\n  ✅ 入库完成: 型号 {n_model} | 明细 {n_field} 行 | 宽表 {n_wide} 行 | 失败 {len(failed)}")
    for name, err in failed:
        print(f"     - {name}: {err}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
