# 20260801 Senators Batch 01

本批处理 [SENATORS-BATCH-20260801-LIST.md](/Users/gao/Documents/lgqm/SENATORS-BATCH-20260801-LIST.md) 的前三位 Senator：刘三、解迩仁、冷凝云。

## 命名规范

- 批次、名单、目录统一使用 `Senator` / `senators`，不再使用 `Elder` / `elders`。
- 批次目录格式：`YYYYMMDD-senators-batch-NN`。
- 名单文件格式：`SENATORS-BATCH-YYYYMMDD-LIST.md`。
- 原著世界观术语保留中文，例如“元老院”“元老身份”“在元老院的位置”；这些不是文件命名，不翻译成 Senator。
- 人物 skill 目录仍使用角色拼音短名，例如 `liusan-perspective`、`xieerren-perspective`、`lengningyun-perspective`。

## 本批产物

- [刘三](/Users/gao/Documents/lgqm/batches/20260801-senators-batch-01/liusan-perspective/SKILL.md)
- [解迩仁](/Users/gao/Documents/lgqm/batches/20260801-senators-batch-01/xieerren-perspective/SKILL.md)
- [冷凝云](/Users/gao/Documents/lgqm/batches/20260801-senators-batch-01/lengningyun-perspective/SKILL.md)

## 写作准则

- 固定范本：`/Users/gao/Documents/lgqm/元老角色蒸馏/maqianzhu-perspective/SKILL.md`。
- `SKILL.md` 必须采用马千瞩范本的长画像结构：frontmatter、角色扮演规则、回答工作流、身份卡、心智模型、决策启发式、表达 DNA、价值观与反模式、内在张力、时间线、智识谱系、诚实边界、调研来源。
- 回答工作流不能只套章节名。Step 1 必须是人物专属的问题路由表，类型来自人物真实能力域、权力位置和风险域；禁止使用“原文考据/角色判断/制度分析/伦理风险”这类通用分类充数。
- Step 3 必须是人物专属输出算法，像马千瞩的“数字说话、方向框定、具体方案”或刘翔的“数据、任务卡、政治账”一样能体现角色方法论；禁止使用“先给结论，再说明依据，最后列风险边界”这类通用模板。
- 心智模型以 7 个左右为目标，每个模型必须给来源证据、应用方式和局限性；不能只写泛泛性格标签。
- 决策启发式以 8-10 条为目标，必须能回到原著行为或明确文本推断。
- 人物厚度必须覆盖关键关系网。凡证据中高频出现且影响人物行动的对象、组织、地点和事件，必须进入规则、模型、时间线、智识谱系或诚实边界，不能只写进 triggers。
- 智识谱系必须拆成至少两个子分类：`思想来源` 和 `在元老院的位置`；不能只列松散影响源。
- 研究文件 `references/research/01-06` 不能以“详见 SKILL.md”充数；每份都要能独立支撑最终画像。
- 来源锚点只使用本地原著 md；人物库、草稿、规划文只用于名单、主名和身份校验，不作为剧情证据。
- SKILL 和 research 中的来源必须以“《章节》：摘录”呈现；不得写 `EVIDENCE #... | offset ...`，也不得用 `#2/#5/#893` 这种只有审计意义、没有阅读意义的引用。
- 标注为“原文摘录”“原著引用”“核心名言”的文字必须保留原文字符，不得替换引号、标点或关键字；必须能在 `临高启明全本.md` 中逐字命中，并通过批次级 `verify_batch.py`。
- 生成器必须 fail closed：缺少 `problem_types`、`response_method`、分裂后的 `genealogy` 或关键关系边界时，不得用 fallback 模板静默生成。

## 提交范围

提交只包含最终结果：

- 本 README。
- 三个人物 skill 目录按范式完整保留：
  - `SKILL.md`
  - `references/research/`
  - `references/sources/`
  - `scripts/quality_check.py`

不提交工作过程文件：

- `build_skills.py`
- `extract_evidence.py`
- `__pycache__/`
- `.DS_Store`
- 根目录或批次目录中的临时校验脚本，例如 `verify_batch.py`

## 本地验收记录

- 批次验收已运行：`python3 /Users/gao/Documents/lgqm/verify_batch.py /Users/gao/Documents/lgqm/batches/20260801-senators-batch-01`
- 结果：3/3 通过，65 条引用，0 条伪造。

## 本轮返工复盘

| 错误 | 原标准是否覆盖 | 为什么没执行 | 修正 |
|---|---|---|---|
| 刘三初版厚度不足，佛山、柳工作、李洛由、萱春、乌云花没有进入核心模型 | 只部分覆盖；原标准只说长画像和模型数量 | 没有强制“关系网/关键事件必须入模型”，只按主题概括 | 已补关系模型，并加入“关键关系网”准则 |
| 冷凝云初版厚度不足，太监、石翁、李洛由、山西商帮、院内位置不足 | 只部分覆盖 | 同上，且 triggers 误当作覆盖 | 已补 9 个模型，并要求不能只写 triggers |
| `EVIDENCE #... | offset ...` 和 `#2/#5` 等引用无阅读意义 | 未覆盖 | 原标准只要求证据真，没有要求引用可读 | 已改为章节+摘录，审计 ID 只保留在 `SOURCE_INDEX.md` |
| 智识谱系忘记拆子分类 | 未覆盖到细节 | 原标准只写“智识谱系”，没写必须拆成哪些栏 | 已要求至少 `思想来源` / `在元老院的位置` |
| Step 1 使用通用问题分类 | 未覆盖 | 生成器有 fallback 通用表，结构检查无法发现 | 已改为人物专属 `problem_types`，去掉 fallback |
| Step 3 使用通用回答模板 | 未覆盖 | 生成器硬编码同一句话，三人共享 | 已新增人物专属 `response_method`，缺失即构建失败 |
| 引用字符被清洗函数替换，造成 9 条误判伪造 | 已覆盖“逐字命中”，但执行冲突 | `clean_quote` 把原文引号替换成另一种字符，破坏逐字匹配 | 已改为只压缩空白，不替换原文字符 |
