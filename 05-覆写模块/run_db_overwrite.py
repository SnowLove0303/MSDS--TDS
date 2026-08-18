#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MSDS 数据库检索与覆写流水线
============================================
从 SQLite 数据库 (msds_standard.db) 检索指定型号数据，
自动构建符合覆写引擎契约的标准写入项 (write_items)，
调用 msds_overwrite_engine 注入标准 Word 模板并输出新的 MSDS docx 文档。

用法:
  python run_db_overwrite.py --model EC-1801
  python run_db_overwrite.py --model PEA-4139 --out outputs/PEA-4139_out.docx
"""

import os
import sys
import json
import argparse
from pathlib import Path

# 添加结构读取与覆写引擎到 sys.path
BASE_DIR = Path(r"F:\正式项目与模块化内容\冠志\MSDS\Word 覆写模块")
READ_DIR = BASE_DIR / "结构读取"
ENGINE_DIR = BASE_DIR / "覆写引擎"

if str(READ_DIR) not in sys.path:
    sys.path.insert(0, str(READ_DIR))
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

import core.msds_db as m
import msds_overwrite_engine as moe

DB_PATH = BASE_DIR / "数据库" / "正式库" / "Data Base" / "msds_standard.db"
DEFAULT_TEMPLATE = Path(r"F:\正式项目与模块化内容\冠志\MSDS\MSDS 数据清理模块\标准模板\标准模板\定稿模板\PEA-4139 MSDS_CN 冠志 模板.docx")
DEFAULT_FIELD_MAP = ENGINE_DIR / "field_maps_pea4139_cn.json"


def build_write_items_from_db(conn, model_id: int) -> dict:
    """从数据库中提取指定 model_id 的全节数据并构建 write_items。"""
    detail = m.model_detail(conn, model_id)
    model_name = detail.get("model", "")

    sections = {}

    # S0: 页眉与页脚
    s0_rows = m.listed_section_rows(conn, model_id, 0)
    s0_items = []
    for r in s0_rows:
        if r.kind == "field" and r.value and r.label not in ("物料安全数据表", "页码"):
            s0_items.append({"seq": "", "label": r.label, "value": r.value})
    if not s0_items:
        s0_items = [
            {"seq": "", "label": "Version", "value": "1.0"},
            {"seq": "", "label": "产品名称", "value": model_name},
            {"seq": "", "label": "公司名称", "value": "广州冠志新材料科技有限公司"},
            {"seq": "", "label": "产品型号", "value": model_name},
            {"seq": "", "label": "修订日期", "value": "2026-08-14"},
        ]
    sections["0"] = s0_items

    # S1 ~ S16
    for sec in range(1, 17):
        rows = m.listed_section_rows(conn, model_id, sec)
        if sec == 3:
            s3_type = "混合物"
            comps = []
            for r in rows:
                if r.kind == "field" and r.label == "产品类型" and r.value:
                    s3_type = r.value
                elif r.kind == "subtable" and r.label == "成分":
                    for row in r.sub_rows:
                        if len(row) >= 3 and any(str(x).strip() for x in row):
                            name_clean = str(row[0]).strip().replace(" ", "")
                            comps.append({
                                "name": name_clean,
                                "cas": str(row[1]).strip(),
                                "conc": str(row[2]).strip(),
                            })
            sections["3"] = {"产品类型": s3_type, "components": comps}
        else:
            items = []
            for r in rows:
                if r.kind == "field" and m.is_meaningful_value(r.value):
                    items.append({"seq": r.seq or "", "label": r.label, "value": r.value})
                elif r.kind == "note" and m.is_meaningful_value(r.value):
                    items.append({"seq": r.seq or "", "label": r.label, "value": r.value})
            if items or sec in (1, 2, 9):
                sections[str(sec)] = items

    return {
        "sections": sections,
        "keep_structure": [2],
        "empty_policy": "warn",
    }


def run_pipeline(model_query: str = "EC-1801", template_path: str = None, out_path: str = None):
    if not DB_PATH.exists():
        raise FileNotFoundError(f"数据库文件不存在: {DB_PATH}")

    template_file = Path(template_path) if template_path else DEFAULT_TEMPLATE
    if not template_file.exists():
        raise FileNotFoundError(f"模板文件不存在: {template_file}")

    conn = m.open_db(str(DB_PATH))
    print(f"[1/4] 连接数据库: {DB_PATH}")
    
    # 检索型号
    matches = m.find_models(conn, model_query)
    if not matches:
        all_models = m.list_models(conn)
        avail = [row[0] for row in all_models]
        raise ValueError(f"未在数据库中找到型号 '{model_query}'。当前库内可用型号: {avail}")
    
    target_model = matches[0]
    model_id = target_model[0]
    model_name = target_model[1]
    print(f"[2/4] 检索到目标型号: ID={model_id}, 型号={model_name}, 来源={target_model[2]}, 字段数={target_model[4]}")

    # 构建写入项
    print(f"[3/4] 正在从数据库提取并转换 16 节写入项...")
    write_items = build_write_items_from_db(conn, model_id)
    sec_count = len(write_items["sections"])
    print(f"      成功生成 {sec_count} 个 Section 写入项")

    # 确定输出路径
    if out_path:
        out_file = Path(out_path)
    else:
        out_dir = ENGINE_DIR / "outputs"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{model_name}_MSDS_CN_冠志_覆写输出.docx"

    out_file.parent.mkdir(parents=True, exist_ok=True)

    # 执行覆写
    print(f"[4/4] 正在调用覆写引擎注入模板: {template_file.name} -> {out_file.name} ...")
    field_map_arg = str(DEFAULT_FIELD_MAP) if DEFAULT_FIELD_MAP.exists() else None
    logs = moe.overwrite(
        str(template_file),
        write_items,
        str(out_file),
        field_map=field_map_arg,
        missing_policy="no_data",
        missing_text="无数据",
    )
    print(f"      覆写完成，记录操作日志 {len(logs)} 条")

    # 闭环校验
    ok, probs = moe.verify_output(str(template_file), str(out_file), write_items)
    if ok:
        print(f"      [PASS] 闭环校验通过！所有字段与成分表一致。")
    else:
        print(f"      [WARN] 闭环校验发现 {len(probs)} 处差异:")
        for p in probs[:10]:
            print(f"        - {p}")

    print(f"\n>> 最终生成文档: {out_file}")
    return str(out_file)


def main():
    parser = argparse.ArgumentParser(description="MSDS 数据库检索与覆写生成")
    parser.add_argument("--model", default="EC-1801", help="目标型号名称 (默认: EC-1801)")
    parser.add_argument("--template", default=None, help="底模 docx 路径")
    parser.add_argument("--out", default=None, help="输出 docx 路径")
    args = parser.parse_args()

    run_pipeline(model_query=args.model, template_path=args.template, out_path=args.out)


if __name__ == "__main__":
    main()
