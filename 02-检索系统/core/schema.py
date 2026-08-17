# -*- coding: utf-8 -*-
"""MSDS 标准字段 Schema: 任意写法的 MSDS 统一映射到标准字段视图.

定位: reader 产出原始行, Schema 负责归一化/折叠. 供透视总表、标准化
覆写输出、数据库构建直接消费. 不依赖 docx_reader, 可独立调用.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .structure import SectionData, SectionRow, split_seq


@dataclass(frozen=True)
class SchemaField:
    """一个标准字段 (每节 Schema 的最小单元)."""
    name: str                 # 标准字段名 (显示/列名, 如 "GHS危险性类别")
    aliases: tuple = ()       # 同义标签 (源文件可能写法, 归一化到 name)
    kind: str = "field"       # field | sub | note | comp
    seq: str = ""             # 标准序号 (如 "2.1"; 空 = 不固定)
    collapse: bool = False    # 空父级分组标签 → 折叠 (不产列, 子级上提)
    multi: bool = False       # 可多行值 (列表字段, 如 防范说明 P 代码)


# 每节标准字段集 (以 GB/T 16483 + 全库实际模板字段为基准).
SECTION_SCHEMAS: dict[int, list[SchemaField]] = {
    0: [  # 页眉页脚
        SchemaField("物料安全数据表", collapse=True),
        SchemaField("Version", aliases=("版本",)),
        SchemaField("产品名称"),
        SchemaField("公司名称"),
        SchemaField("产品型号"),
        SchemaField("修订日期"),
        SchemaField("页码"),
    ],
    1: [
        SchemaField("产品名称", kind="sub", collapse=True),
        SchemaField("中文名称"),
        SchemaField("产品类型", aliases=("化学品分类", "产品分类", "Product type", "Product classification", "Chemical category")),
        SchemaField("产品使用建议和使用限制", aliases=("使用建议", "用途", "Application of the substance / the preparation", "Product use suggestions and restrictions")),
        SchemaField("供应商信息", kind="sub", collapse=True),
        SchemaField("供应商名称", aliases=("Name of supplier", "Manufacturer/Supplier", "Supplier name")),
        SchemaField("供应商地址", aliases=("Supplier address", "Head Office Address")),
        SchemaField("电话", aliases=("Tel", "TEL", "Telephone")),
        SchemaField("传真", aliases=("Fax",)),
        SchemaField("应急电话", aliases=("紧急电话", "Emergency telephone")),
        SchemaField("电子邮件", aliases=("E-mail", "Email", "Further information obtainable from")),
    ],
    2: [
        SchemaField("物质或混合物分类", aliases=("物质或混合物的分类",), kind="sub", collapse=True),
        SchemaField("GHS危险性类别", aliases=("GHS分类", "危险性分类", "GHS危险性", "GHS hazard category", "CHS hazard category", "Hazard classification", "GHS risk category", "GHS Classification", "根据GHS不属于危害化学品", "无危险", "不属于危害化学品", "CHS危险性类别", "GHS 危险性类别", "急性毒性 (经口) 类别 4", "急性毒性 (经皮) 类别 4", "急性毒性 (吸入) 类别 4", "皮肤腐蚀/刺激 类别 1B", "皮肤腐蚀/刺激 类别 1", "重眼损伤/眼刺激 类别 1", "重眼损伤/眼刺激 类别 2", "皮肤致敏物 类别 1", "皮肤致敏物 类别 1B", "急性水生毒性 类别 3", "慢性水生毒性 类别 3", "急性水生毒性 类别 2", "慢性水生毒性 类别 2", "特异性靶器官毒性-反复接触 类别 2")),
        SchemaField("标签要素", aliases=("GHS标签要素", "标签元素", "Labelling according to EU guidelines", "Label elements"), kind="sub", collapse=True),
        SchemaField("象形图", aliases=("GHS-象形图", "GHS象形图", "危险象形标记", "Pictogram", "Pictograms", "Hazard pictograms")),
        SchemaField("信号词", aliases=("警示语", "警告词", "Signal word", "Warning word", "警示词")),
        SchemaField("标签有害成分", aliases=("必须列在标签上的有害成分", "必须列在标签上的有害成份", "有害成分", "Dangerous components")),
        SchemaField("危害性说明", aliases=("危险性说明", "危险说明", "Hazard statements", "Hazard statement", "Hazard Statement", "危险声明")),
        SchemaField("防范说明", aliases=("Prevention instructions", "Preventive instructions", "Precautions", "Precautionary statements", "Precautionary measures", "预防措施", "预防声明", "防范", "事故响应", "泄露", "泄漏", "灭火", "安全存储", "安全储存", "废弃处置", "入眼睛"), multi=True),
        SchemaField("其他危险", aliases=("其他危害", "其它危害", "其它危险", "Information concerning particular hazards for human and environment", "Other hazards", "物理化学危险", "健康危害", "环境危害", "物理和化学危险", "没有分类的其他危害")),
    ],
    9: [
        SchemaField("外观", aliases=("外 观", "Appearance", "Form", "Colour", "Color", "General Information Appearance: Form")),
        SchemaField("气味", aliases=("性状", "感官性状", "Odor", "Odour")),
        SchemaField("嗅觉阈值", aliases=("嗅觉阀值", "Odour threshold", "Olfactory threshold")),
        SchemaField("pH值", aliases=("PH值", "pH", "PH value", "pH-value", "pH-value at 20 °C", "pH-value at 25 °C", "pH (10% in water)")),
        SchemaField("熔点/凝固点", aliases=("熔点", "凝固点", "Melting point/Melting range", "Change in condition", "Change in condition Melting point/Melting range")),
        SchemaField("初沸点/沸点", aliases=("初沸点", "沸点", "最低初沸点", "Boiling point/Boiling range", "Initial boiling point")),
        SchemaField("闪点", aliases=("Flash point",)),
        SchemaField("蒸发速率", aliases=("蒸发速度", "Evaporation rate", "Percent volatility", "Volatility")),
        SchemaField("易燃性", aliases=("可燃性", "可燃性（固态、气态）", "Flammability (solid, gaseous)")),
        SchemaField("爆炸上下限", aliases=("爆炸极限", "Explosion limits", "Danger of explosion", "Lower", "Upper", "Lower: Upper")),
        SchemaField("饱和蒸气压", aliases=("蒸气压", "蒸汽压", "Vapour pressure", "Vapor pressure")),
        SchemaField("蒸气密度", aliases=("相对蒸气密度", "Vapour density", "Relative vapor density")),
        SchemaField("相对密度", aliases=("相对密度（水=1）", "比重", "Relative density")),
        SchemaField("水溶性", aliases=("水中溶解度", "溶解度", "溶解性", "Water solubility", "Solubility in / Miscibility with water")),
        SchemaField("分配系数", aliases=("分配系数n-辛醇/水", "辛醇/水分配系数", "辛醇/水分配系数的对数值", "辛醇/水分配系数对数值", "Partition coefficient (n-octanol/water)", "Logarithm value of octanol/water partition coefficient", "Log Pow")),
        SchemaField("自燃温度", aliases=("自燃点", "引燃温度", "着火点", "Ignition temperature", "Autoignition temperature", "Self-igniting")),
        SchemaField("分解温度", aliases=("Decomposition temperature",)),
        SchemaField("粘度", aliases=("动力粘度", "Dynamic viscosity", "Viscosity", "Kinematic", "Dynamic at 20 °C", "Dynamic at 20 °C: Kinematic", "Viscosity: Dynamic at 20 °C: Kinematic")),
        SchemaField("密度", aliases=("Density", "Density at 20 °C", "Density at 25°C", "Relative density (water=1)")),
        SchemaField("离子性", aliases=("Ionicity",)),
        SchemaField("有效成分", aliases=("有效成份", "Effective constituent", "Active ingredient", "effective constituent")),
        SchemaField("固体含量", aliases=("Solid content", "Solids content")),
        SchemaField("表面张力", aliases=("Surface tension",)),
        SchemaField("燃烧值", aliases=("Combustion value", "Heat of combustion")),
        SchemaField("粉尘爆炸级别", aliases=("粉尘爆炸",)),
        SchemaField("NCO含量", aliases=("异氰酸酯含量", "游离异氰酸酯", "NCO content")),
        SchemaField("玻璃化温度", aliases=("玻璃化温度Tg/℃", "Tg")),
        SchemaField("最低成膜温度", aliases=("最低成膜温度MFFT/℃", "MFFT")),
        SchemaField("酸值", aliases=("酸价", "Acid value")),
        SchemaField("碘值", aliases=("碘价",)),
        SchemaField("倾点", aliases=("Pour point",)),
        SchemaField("浊点", aliases=("Cloud point",)),
        # 独立物理量 (非"其他信息"折叠): 分子量/APHA值/含量/HLB 有各自语义
        SchemaField("分子量", aliases=("Molecular weight",)),
        SchemaField("APHA值", aliases=("APHA",)),
        SchemaField("含量", aliases=("Content",)),
        SchemaField("HLB值", aliases=("HLB",)),
        SchemaField("其他信息", aliases=("Other information", "General Information", "General Information Form")),
    ],
    11: [
        SchemaField("急性毒性", aliases=("Acute toxicity", "Acute oral toxicity", "急性毒性，经口", "急性毒性，经皮", "急性毒性，吸入")),
        SchemaField("主要皮肤刺激性", aliases=("皮肤刺激性", "原发性皮肤刺激", "Primary irritant effect", "Primary skin irritation", "on the skin", "皮肤腐蚀/刺激")),
        SchemaField("主要眼睛刺激性", aliases=("眼睛刺激性", "主要粘膜刺激性", "on the eye", "Primary mucosal irritation", "原发性粘膜刺激", "Eye irritation", "严重的眼部损伤/眼部刺激", "严重眼损伤/眼刺激", "严重眼损伤/刺激")),
        SchemaField("致敏性", aliases=("皮肤致敏性", "Sensitization", "Skin sensitization", "皮肤致敏", "呼吸或皮肤过敏")),
        SchemaField("致突变性", aliases=("Mutagenicity", "生殖细胞致突变性", "生殖细胞致突变性物质", "Mutability", "体外遗传毒性", "体内基因毒性")),
        SchemaField("致癌性", aliases=("Carcinogenicity", "致癌性", "IARC专著。致癌性的总体评估")),
        SchemaField("生殖毒性", aliases=("生殖毒性/生育力", "Reproductive toxicity", "生殖毒性（生育能力、未出生小孩）", "Reproductive toxicity/fertility", "生殖毒性/致畸性", "生殖毒性/致畸形", "Teratoxicity", "致畸性")),
        SchemaField("特异性靶器官系统毒性", aliases=("特异性靶器官系统毒性（一次接触/反复接触）", "特定靶器官毒性，单次暴露", "特定靶器官毒性，重复暴露", "特定靶器官毒性-单次曝光", "特定靶器官毒性-重复暴露", "STOT评估-一次性接触", "STOT评估-重复性接触", "STOT 评估 – 一次性接触", "STOT 评估 – 重复性接触", "特异性靶器官毒性-一次接触", "特异性靶器官毒性-反复接触")),
        SchemaField("吸入危险", aliases=("Aspiration hazard", "吸入危害", "吸入性危害", "Inhalation hazard", "吞咽及进入呼吸道可能致命")),
        SchemaField("附加信息", aliases=("Additional toxicological information", "Additional information", "可能接触途径的信息", "慢性影响", "与相关的症状物理、化学和毒理学特征", "CMR评估", "CMR evaluation")),
    ],
    12: [
        SchemaField("生态毒性", aliases=("Ecotoxicity", "Aquatic toxicity", "对水生环境有害",)),
        SchemaField("持久性和降解性", aliases=("持久性/降解性", "Durability and degradability", "Persistence and degradability")),
        SchemaField("生物累积潜力", aliases=("生物累积性", "Bioaccumulation")),
        SchemaField("土壤中迁移性", aliases=("迁移性", "Mobility in soil")),
        SchemaField("其他不利的影响", aliases=("其他不利影响", "其他", "Other adverse effects", "Additional ecological information", "General notes", "Other", "Others", "Water hazard class 1 (German Regulation) (Self-assessment)", "PBT", "vPvB", "Results of PBT and vPvB assessment", "通用信息")),
    ],
    13: [
        SchemaField("处理方法", aliases=("废弃处置方法", "Disposal methods", "Handling method", "Recommendation", "Uncleaned packaging", "Recommended cleansing agents", "Void")),
    ],
    16: [
        SchemaField("版本", aliases=("Version", "修订日期", "签发日期")),
        SchemaField("免责声明", aliases=("声明", "Disclaimer", "Department issuing MSDS")),
        SchemaField("参考标准", aliases=("标准", "References", "Standards")),
    ],
}

# 其余节的基础字段 (待实证补全, 先给最常出现的)
_BASE_SCHEMAS: dict[int, list[SchemaField]] = {
    3: [SchemaField("产品类型", aliases=("Mixtures", "单一物质", "Substance", "Product type")),
        SchemaField("组分", aliases=("Composition", "Dangerous components", "成分", "Chemical name")),
        SchemaField("CAS号", aliases=("CAS No.", "CAS number", "CAS登记号"))],
    4: [SchemaField("一般措施", aliases=("General measures", "General information")),
        SchemaField("误服", aliases=("食入", "After swallowing", "Ingestion", "Swallowed")),
        SchemaField("接触眼睛", aliases=("After eye contact", "Eye contact")),
        SchemaField("接触皮肤", aliases=("After skin contact", "Contact with skin", "Skin contact")),
        SchemaField("吸入", aliases=("After inhalation", "Inhalation"))],
    5: [SchemaField("合适的灭火剂", aliases=("灭火剂", "Suitable extinguishing agent", "Suitable extinguishing agents")),
        SchemaField("不合适的灭火剂", aliases=("Unsuitable extinguishing agent", "Unsuitable extinguishing agents")),
        SchemaField("物质或混合物的特殊危害", aliases=("特殊危害", "Special hazards of substances or mixtures")),
        SchemaField("消防预防措施和保护设备", aliases=("防护设备", "Protective equipment", "Fire prevention measures and protection equipment")),
        SchemaField("有害燃烧产物", aliases=("燃烧产物", "Hazardous combustion products"))],
    6: [SchemaField("个人预防措施、应急程序", aliases=("个人预防措施", "Spill and Leak Procedures", "Precautions for safe handling")),
        SchemaField("环境保护措施", aliases=("Environmental precautions",)),
        SchemaField("污染物收集和清除的方法", aliases=("收集和清除方法", "Methods and material for containment and cleaning up"))],
    7: [SchemaField("安全操作防范", aliases=("操作注意事项", "安全操作", "Handling/Storage Precautions", "Information about fire - and explosion protection")),
        SchemaField("安全储存条件", aliases=("储存条件", "Storage", "Storage Period and Temperature", "Requirements to be met by storerooms and receptacles", "Information about storage in one common storage facility", "Further information about storage conditions"))],
    8: [SchemaField("暴露控制", kind="sub", collapse=True),
        SchemaField("生物限值", kind="sub", seq="8.2"),   # 子表: 组分名称|标准来源|生物监测指标|生物限值|采样时间
        SchemaField("工程控制", seq="8.3"),
        SchemaField("呼吸系统防护", aliases=("呼吸防护", "Respiratory protection")),
        SchemaField("手部防护", aliases=("Hand Protection", "Protection of hands")),
        SchemaField("防护手套的合适材料", aliases=("手套材料", "Suitable material for protective gloves")),
        # 三种手套材质是独立子行 (各有厚度/穿透时间值), 不是"防护手套的合适材料"同义写法
        SchemaField("氟化橡胶 –FKM", aliases=("氟化橡胶 - FKM", "氟化橡胶-FKM", "Fluorinated rubber - FKM", "Fluorinated rubber -FKM")),
        SchemaField("丁基橡胶 –IIR", aliases=("丁基橡胶 - IIR", "丁基橡胶-IIR", "Butyl rubber - IIR", "Butyl rubber -IIR")),
        SchemaField("丁腈橡胶 – NBR", aliases=("丁腈橡胶 - NBR", "丁腈橡胶-NBR", "Nitrile rubber - NBR", "Nitrile butadiene rubber - NBR")),
        SchemaField("眼睛防护", aliases=("眼部防护", "Eye protection")),
        SchemaField("身体防护", aliases=("皮肤防护", "Body protection")),
        SchemaField("建议", aliases=("Recommendation", "Suggestion", "Personal protective equipment", "General protective and hygienic measures", "Additional information about design of technical facilities"))],
    10: [SchemaField("稳定性", aliases=("化学稳定性", "Chemical stability")),
         SchemaField("危险反应", aliases=("反应性", "可能的危害反应", "Possible hazardous reactions", "Reactivity")),
         SchemaField("应避免的条件", aliases=("避免条件", "Conditions to be avoided", "Thermal decomposition / conditions to be avoided")),
         SchemaField("不相容的材料", aliases=("不相容物质", "Incompatible materials")),
         SchemaField("危险的分解产物", aliases=("分解产物", "危险分解产物", "Hazardous decomposition products"))],
    14: [SchemaField("UN编号", aliases=("联合国编号", "UN-Number", "UN number")),
         SchemaField("联合国运输名称", aliases=("UN proper shipping name",)),
         SchemaField("运输危险级别", aliases=("危险级别", "运输类别", "Transport hazard class(es)")),
         SchemaField("包装类型", aliases=("包装组", "Packing group")),
         SchemaField("海洋污染物", aliases=("Environmental hazards", "环境危险")),
         SchemaField("运输注意事项", aliases=("运输信息", "Transport in bulk according to Annex II of MARPOL73/78 and the IBC Code", "Transport in bulk")),
         SchemaField("公路和铁路运输", aliases=("Road and railway transportation",)),
         SchemaField("海上运输", aliases=("Sea transportation",)),
         SchemaField("空运", aliases=("Air transportation",)),
         SchemaField("用户特殊注意事项", aliases=("特殊注意事项", "Special precautions for user", "Special precautions for users"))],
    15: [SchemaField("适用法规", aliases=("法规", "Applicable regulations")),
         SchemaField("法规符合性", aliases=("Regulatory compliance",)),
         SchemaField("符合下列法规要求", aliases=("Comply with the following regulatory requirements",)),
         SchemaField("其它的规定", aliases=("其他规定", "Other rules", "Other regulations", "Other provisions", "Other regulations"))],
}


def standard_fields(num: int) -> list[SchemaField]:
    """该节标准字段列表 (已定义节返回详情, 未定义节返回基础字段)."""
    return SECTION_SCHEMAS.get(num, _BASE_SCHEMAS.get(num, []))


# 同义别名 → 标准字段名 查找表: {节: {别名: 标准名}}
_ALIAS_LOOKUP: dict[int, dict[str, str]] = {}


def _build_alias_lookup() -> None:
    if _ALIAS_LOOKUP:
        return
    for num, flds in list(SECTION_SCHEMAS.items()) + list(_BASE_SCHEMAS.items()):
        m = _ALIAS_LOOKUP.setdefault(num, {})
        for f in flds:
            m[f.name] = f.name
            for a in f.aliases:
                m[a] = f.name


# ------------------------------------------------------------------
# 引导段识别 (S11/S12 等 "以下为XX的参考数据:" 说明段)
# ------------------------------------------------------------------

# 引导段模式: "以下为二乙二醇单丁醚 （CAS号：112-34-5）的生态毒理学参考数据："
#             "以下为类似产品的风险评估数据："
#             "类似产品的风险评估数据：" (CX-470 等省略"以下为"前缀)
# 这类行是"块引导"说明 (父级/说明段), 不是字段标签. 识别后作为
# note (跨行保留原格式), 不当空值字段/加粗标签.
# 前缀可选以兼容省略式; 冒号必须 (无冒号的完整陈述句如
# "根据EC指令2006/121/EG,无可用的接触限值信息" 不是引导段).
# 排除祈使句引导 "请参阅以下数据：" (BL-8085 S11, 该句作为结构化标题
# pending_label, 后续毒理字段配对; 若按引导段判为 note 会堆积通栏文本).
_GUIDE_RE = re.compile(
    r"^(?!请)(?:以下(?:为|是)?)?[^。；;]{4,}?(?:参考数据|数据|资料|信息|风险评估|评估数据|报告)[：:]\s*$")


def is_guide_line(text: str) -> bool:
    """判断一行是否是引导段 (说明性父级, 非字段标签)."""
    t = (text or "").strip()
    return bool(t) and bool(_GUIDE_RE.match(t))


# ------------------------------------------------------------------
# 归一化 API
# ------------------------------------------------------------------

def _clean_label(raw: str) -> str:
    """去序号前缀 + 去尾冒号 + 压缩空白."""
    _, lbl = split_seq((raw or "").strip())
    return re.sub(r"\s+", " ", lbl).rstrip("：:。 .").strip()


# S9 理化特性 单位括号剥离: 统一字段的关键.
#   "pH值（1%水溶液）" → "pH值"   "闪点（闭口）" → "闪点"
#   "粘度/25℃" → "粘度"   "蒸汽压（25℃）" → "蒸汽压"
#   "粘度/mPa·S" → "粘度"   "密度/g/cm3" → "密度"   "粘度/mPa·S（3号转子）" → "粘度"
# 剥离后与标准字段 (pH值/闪点/粘度/饱和蒸气压 等) 归并为同一列,
# 避免总库成分列因写法不同而爆炸 (用户核心诉求).
# S9 可剥的"通用条件"括号: 内容含 浓度%/温度℃/压力单位/状态词 → 是通用条件,
# 剥离后归并 (如 pH值（1%水溶液）→pH值, 蒸汽压（20℃，Kpa）→蒸汽压);
# 特殊限定括号 (具体物质/介质名, 如 蒸发速度（醋酸丁酯-1）) → 保留独立列.
_S9_COND_RE = re.compile(
    r"[\d.]+%|℃|°C|Kpa|kPa|hPa|Pa\b|mPa|g/|kg/|水溶液|固态|气态|闭口|开口")
_S9_UNIT_RE = re.compile(r"[（(]([^（）()]*)[）)]$")   # 尾部括号 (条件判断后决定剥/留)
# "/25℃" "/25°C" "/mPa·S" "/g/cm3" "/g/cm³" "/19-21%" 等尾部斜杠单位
#   (只剥纯数字/ASCII/℃°³ 单位段; 含中文的斜杠段如 辛醇/水分配系数对数值 必须保留
#    → 字符集用 [0-9A-Za-z·±/%\-³], 不含 一-鿿)
_S9_SLASH_RE = re.compile(
    r"[/／]\s*(?:[\d.]+(?:℃|°C)?|[0-9A-Za-z·±/%\-³]{1,12})$")


def _strip_s9_unit(label: str) -> str:
    """剥离 S9 标签尾部通用条件括号/单位, 返回最简形态.

    - 通用条件括号 (浓度/温度/压力/状态) → 剥:  pH值（1%水溶液）→pH值
    - 特殊限定括号 (具体物质/介质) → 保留:    蒸发速度（醋酸丁酯-1）原样
    - 尾部斜杠单位 → 剥:                     粘度/25℃→粘度
    """
    t = (label or "").strip()
    m = _S9_UNIT_RE.search(t)
    if m and _S9_COND_RE.search(m.group(1)):
        t = t[:m.start()].strip()
    t = _S9_SLASH_RE.sub("", t).strip()
    return t


def standard_name(num: int, raw_label: str) -> str:
    """任意原始标签 → 标准字段名 (同义映射; 未命中返回清理后的原名).

    S9 特殊: 直接匹配失败时, 循环剥离单位括号后多次回退匹配:
      'pH值（1%水溶液）' → pH值    '有效成分/% / 30±1' → 有效成分
      '比重（25℃） / 1.001' → 相对密度   '粘度/mPa·S（3号转子）' → 粘度
    使不同写法/值混入标签的理化特性字段都归并到同一标准列.
    """
    _build_alias_lookup()
    lbl = _clean_label(raw_label)
    if not lbl:
        return ""
    lookup = _ALIAS_LOOKUP.get(num, {})
    hit = lookup.get(lbl)
    if hit:
        return hit
    if num == 9:
        t = lbl
        for _ in range(3):                    # 最多剥 3 轮 (单位括号/斜杠/值)
            stripped = _strip_s9_unit(t)
            if stripped == t:
                break
            t = stripped
            hit = lookup.get(t)               # 剥离一轮后立刻回查
            if hit:
                return hit
            for f in SECTION_SCHEMAS.get(9, ()):
                if f.name == t:               # 与标准字段名一致 → 归并
                    return t
    return lbl


def standard_field_of(num: int, raw_label: str) -> SchemaField | None:
    """原始标签 → 标准 SchemaField; 未命中返回 None."""
    name = standard_name(num, raw_label)
    for f in standard_fields(num):
        if f.name == name:
            return f
    return None


# ------------------------------------------------------------------
# 折叠 + 标准行序列
# ------------------------------------------------------------------

def iter_standard_rows(sec: SectionData) -> list[SectionRow]:
    """产出 Schema 化后的标准行序列 (折叠空父级, 归一化标签).

    规则:
      - field 行: label 归一化到标准字段名 (保留 value); 同义字段合并
      - collapse=True 且值空的父级分组标签 → 折叠 (不产列)
      - note/span 行 (总结句/引导段) → 原样保留 (跨行说明)
    返回 SectionRow 列表 (kind: field/note/sub/section).
    """
    rows: list[SectionRow] = []
    last_std: str | None = None   # 上一个标准字段名 (用于同义合并)
    for row in sec.iter_rows():
        if row.kind == "section":
            rows.append(row)
            last_std = None
            continue
        if row.kind == "field":
            std = standard_name(sec.number, row.label)
            f = standard_field_of(sec.number, row.label)
            # 折叠空父级分组标签
            if f is not None and f.collapse and not row.value.strip():
                continue
            if std and std == last_std and f is not None and f.multi:
                # 多值字段连续行 (如 防范说明 P 代码多行) → 合并到上一行
                prev = rows[-1]
                if prev.kind == "field":
                    prev.value = (prev.value + "\n" + row.value).strip()
                continue
            new = SectionRow(kind="field", seq=row.seq, label=std,
                             value=row.value, editable=row.editable,
                             index=row.index, span=row.span)
            rows.append(new)
            last_std = std
            continue
        # sub 行: Schema 标记 collapse 的分组子标题 → 折叠 (空父级不产列)
        if row.kind == "sub":
            f = standard_field_of(sec.number, row.label)
            if f is not None and f.collapse:
                last_std = None
                continue
        # note / sub / 其他 → 原样保留 (引导段已在读取层转 note)
        rows.append(row)
        last_std = None
    return rows


def standard_field_values(sec: SectionData) -> dict[str, list[str]]:
    """该节的标准字段 → 值列表 (同义合并 + 折叠空父级后).

    返回 {标准字段名: [值, ...]} (多值字段可能多行; 单值字段通常 1 项).
    """
    out: dict[str, list[str]] = {}
    for row in iter_standard_rows(sec):
        if row.kind == "field" and row.label:
            out.setdefault(row.label, []).append(row.value)
    return out


def standard_result(result) -> dict[int, dict[str, list[str]]]:
    """整个 ParseResult 的 Schema 化标准字段视图.

    返回 {节号: {标准字段名: [值, ...]}} — 供覆写/建库/透视直接消费.
    """
    return {num: standard_field_values(sec)
            for num, sec in sorted(result.sections.items())}