# -*- coding: utf-8 -*-
import sys, json
from pathlib import Path
sys.path.insert(0, r"F:\正式项目与模块化内容\Word 覆写模块\覆写引擎")
from msds_overwrite_engine import overwrite, verify_output, log

ENGINE = r"F:\正式项目与模块化内容\Word 覆写模块\覆写引擎"
PLAN = Path(ENGINE) / "EC-1801 推导方案.json"
TEMPLATE = r"F:\正式项目与模块化内容\MSDS 数据清理模块\标准模板\标准模板\定稿模板\PEA-4139 MSDS_CN 冠志 模板.docx"
OUT = r"F:\正式项目与模块化内容\Word 覆写模块\数据库\正式库\入库word  第一批\EC-1801 msds_CN 冠志_模板覆写输出.docx"
FIELD_MAP = Path(ENGINE) / "field_maps_pea4139_cn.json"

plan = json.loads(PLAN.read_text(encoding="utf-8"))
wi = {"sections": {}}
# meta -> S0（页眉页脚）
meta = plan.get("meta", {})
s0 = dict(plan.get("sections", {}).get("0", {}))
if meta.get("产品名称"):
    s0["页眉_产品名称"] = meta["产品名称"]
    s0.setdefault("页脚_产品名称", meta["产品名称"])
if meta.get("修订日期"):
    s0["页脚_修订日期"] = meta["修订日期"]
if meta.get("版本"):
    # 页眉_版本只给纯版本号：sync_section0 用正则捕获模板 'Version：V1.0' 中的
    # 'V1.0' 做子串替换，若值带 'Version：' 前缀会产生 'Version：Version：1.0'
    s0["页眉_版本"] = str(meta["版本"])
if s0:
    wi["sections"]["0"] = s0
for sec, payload in plan["sections"].items():
    if sec == "0":
        continue
    wi["sections"][sec] = payload

log("===== 执行覆写 EC-1801（PEA-4139 定稿模板驱动）=====")
# 缺值策略：模板字段方案未给 → 值格写"无数据"（清旧产品残留），S11 纯值驱动除外
logs = overwrite(TEMPLATE, wi, OUT, field_map=str(FIELD_MAP),
                 missing_policy="no_data", missing_text="无数据")
log(f"覆写操作日志 {len(logs)} 条（节序）")
# 按节统计
from collections import Counter, OrderedDict
stat = Counter()
for lg in logs:
    stat[(lg[0], lg[1])] += 1
for (kind, sec) in sorted(stat, key=lambda x: (x[1], x[0])):
    log(f"  S{sec} {kind}x{stat[(kind, sec)]}")

log("===== 闭环校验 =====")
ok, probs = verify_output(TEMPLATE, OUT, wi)
if ok:
    log("闭环校验通过 OK")
else:
    log("闭环校验失败：", "FAIL")
    for p in probs[:60]:
        log("  - " + p, "FAIL")
    sys.exit(1)
