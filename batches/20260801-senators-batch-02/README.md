# 20260801 Senators Batch 02

本批处理 [SENATORS-BATCH-20260801-LIST.md](/Users/gao/Documents/lgqm/SENATORS-BATCH-20260801-LIST.md) 的第 4 位 Senator：艾志新。

## 命名规范

- 批次目录延续 `YYYYMMDD-senators-batch-NN`。
- 人物 skill 目录使用角色拼音短名：`aizhixin-perspective`。
- 原著世界观术语保留中文，例如“元老院”“财税局”“广州特别市”。

## 本批产物

- [艾志新](/Users/gao/Documents/lgqm/batches/20260801-senators-batch-02/aizhixin-perspective/SKILL.md)

## 写作准则

- 本批以 `batches/20260801-senators-batch-01/lengningyun-perspective` 为近例范文。
- 来源锚点只使用本地原著 md；人物库、草稿、规划文只用于名单、主名和身份校验，不作为剧情证据。
- `SKILL.md` 必须采用长画像结构：frontmatter、角色扮演规则、回答工作流、身份卡、心智模型、决策启发式、表达 DNA、价值观与反模式、内在张力、时间线、智识谱系、诚实边界、调研来源。
- 回答工作流必须围绕艾志新的真实能力域：广州财税、新币、税制设计、征管落地、代收代缴、专卖、风俗税、经济罪案调查、预算争夺和大户治理。
- 人物厚度必须覆盖关键关系网：刘翔、王企益、张筱奇、程栋、孟贤、郑尚洁、慕敏、午木、财税局归化民干部、广州大户和元老院舆论。
- 证据呈现使用“《章节》：摘录”格式；审计 ID 只保留在 `references/sources/EVIDENCE.jsonl` 中。

## 本地验收

- 单 skill 验收：`python3 batches/20260801-senators-batch-02/aizhixin-perspective/scripts/quality_check.py`
- 批次验收：`python3 verify_batch.py batches/20260801-senators-batch-02`
