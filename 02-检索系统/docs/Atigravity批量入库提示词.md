# Atigravity 批量入库提示词（MSDS 中文库）

> 直接复制以下提示词给 Atigravity（Claude Code / 任意 Agent）执行。
> 依据: 《数据导入-入库指引及强制性规范》 · 批量检索 skill · 定稿模板结构

---

```
你是 MSDS 标准字段库的数据清洗入库专员。

## 任务
把目录 `F:\正式项目与模块化内容\冠志\MSDS\Word 覆写模块\数据库\正式库\入库word  第一批\`
中所有**中文 MSDS**（*.docx）按既定标准与规范清洗入库到 SQLite 标准字段库
`F:\正式项目与模块化内容\冠志\MSDS\Word 覆写模块\数据库\正式库\Data Base\msds_standard.db`。

## 环境（固定，不要改动）
- Python 解释器: `E:\MorenAnzhuangLujing\Anaconda\python.exe`
- 入库工具: `F:\正式项目与模块化内容\冠志\MSDS\Word 覆写模块\结构读取\tools\build_msds_db.py`
- 数据库: 上述 msds_standard.db（四表: schema_field / msds_model / msds_field / msds_wide）
- 结构基线: 定稿模板 `F:\正式项目与模块化内容\冠志\MSDS\MSDS 数据清理模块\标准模板\标准模板\定稿模板\PEA-4139 MSDS_CN 冠志 模板.docx`

## 绝对禁止（违反即失败）
1. **严禁修改任何结构代码**: `core/schema.py`、`core/msds_db.py`（尤其 `_SKELETON`、
   `_db_std_name`、`_listed_field_names`、`STRUCT_FINGERPRINT`）、`core/extract.py`、
   `core/structure.py`、`core/docx_reader.py` 一律只读。
2. **严禁新增字段/列/结构**: 结构里没有的标签数据一律丢弃（入库层已自动处理），
   绝不自行扩充 Schema 或骨架。
3. **严禁绕过入库工具直接写数据库**: 只能用 `tools/build_msds_db.py` 入库；
   不得手写 SQL 修改 msds_model/msds_field/msds_wide。
4. **结构校验失败立即停止**: `build_msds_db.py` 每次运行会校验结构指纹
   (STRUCT_FINGERPRINT)；若报"冻结结构校验失败"，说明结构被改动 → 停止并报告，
   不要尝试绕过或改指纹。

## 执行步骤

### 1) 环境自检（结构校验必须通过）
```
E:\MorenAnzhuangLujing\Anaconda\python.exe F:\正式项目与模块化内容\冠志\MSDS\Word 覆写模块\结构读取\tools\build_msds_db.py "<db>" --models
```
- 输出当前型号列表（当前应有 PEA-4139、EC-1801 两条）即通过；
- 报"冻结结构校验失败" → 立即停止，报告，不继续。

### 2) 批量入库（全部中文 MSDS）
```
E:\MorenAnzhuangLujing\Anaconda\python.exe F:\正式项目与模块化内容\冠志\MSDS\Word 覆写模块\结构读取\tools\build_msds_db.py "<db>" "F:\正式项目与模块化内容\冠志\MSDS\Word 覆写模块\数据库\正式库\入库word  第一批"
```
- 目录内所有中文 MSDS docx 自动逐个入库（跳过 ~$ 锁文件）；
- 单文件失败不中断整体，失败清单会在末尾汇总；
- **不要**对已入库的 PEA-4139/EC-1801 做任何改动（它们已在库中且合规）。

### 3) 验证（必须逐项完成）
```
# 3.1 型号清单与数量
python ...\build_msds_db.py "<db>" --models
# 3.2 抽查 3-5 个新入库型号的骨架结构 (S1 父级/S3 成分子表/S8 生物限值/S15 说明段)
python ...\build_msds_db.py "<db>" --model <型号> --sections 1,3,8,15
# 3.3 检索验证
python ...\build_msds_db.py "<db>" --model-search 闪点
python ...\build_msds_db.py "<db>" --model-search 供应商
```
- 每个抽查型号的 S1: `1.1 产品名称`/`1.3 供应商信息` 应为父级（字段列空），子字段挂其下；
- S3: 成分子表（表头 成分|CAS|含量 + 每成分一行）；
- S8: `8.1 暴露控制`/`8.2 生物限值` 父级 + 5 列子表；
- S15: 指引段/说明段/法规条目独立行；
- 结构外内容一律显示「无数据」，不允许出现新增字段名。

### 4) 汇报
输出报告:
- 入库型号总数、成功/失败文件清单（含失败原因）
- 验证抽查结果（每型号结构是否符合骨架）
- 结构校验状态（指纹一致）

## 规范要点（入库层已实现，供你核对）
- **基于结构找内容**: 数据按 17 节骨架（定稿模板参照）一一对应填，结构永不随数据变化；
  清单外字段自动丢弃（写无数据），不扩任何结构。
- 父级（字段列空）: 0.1 页眉/0.2 页脚/1.1 产品名称/1.3 供应商信息/2.1 紧急情况概述/
  3.2 成分/8.1 暴露控制/8.2 生物限值。
- 子表: S3 成分（3 列）、S8.2 生物限值（5 列）; 无数据预留表头+空行。
- 总结句/说明槽位(13): 无内容写「无数据」; S15 说明段显示说明文字。
- S11/S12 子项归并国标大类; S15 任意法规名归并「法规条目」。
- 成分占位 CAS(商业机密/Trade secret) 原样保留。

## 成功标准
1. 第一批全部中文 MSDS 入库（失败文件清单明确且原因合理）；
2. 抽查型号结构与定稿模板完全一致（同一骨架，仅值不同）；
3. 结构校验通过（STRUCT_FINGERPRINT 未变）；
4. 汇报完整（数量/失败/抽查/校验）。
```

---

> 提示词使用说明：
> - `<db>` 占位符 = `F:\正式项目与模块化内容\冠志\MSDS\Word 覆写模块\数据库\正式库\Data Base\msds_standard.db`
> - 若 Atigravity 环境无法写 E:\ 盘 Python，可让其在提示词中自定位 Python（Anaconda 3.13）
> - 首次运行若库被清空/重建需求，先执行 `--init` 再入库（默认不要 --init，保留 PEA-4139/EC-1801）
