# 陈同词条修订 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把陈同词条重建为证据受限、可进入角色且可自检的“思维操作系统”。

**Architecture:** `SKILL.md` 负责触发后必须执行的角色规则和回答协议；六份 research 文件负责按需提供证据；`SOURCE_INDEX.md` 固化原著范围、锚点和排除项；`quality_check.py` 对结构与高风险事实做确定性检查。

**Tech Stack:** Markdown、YAML frontmatter、Python 3、Git、ZIP

---

### Task 1: 建立失败基线

**Files:**
- Test: `batches/20260730-1231-natives-batch-02/chentong-perspective/SKILL.md`
- Test: `batches/20260730-1231-natives-batch-02/chentong-perspective/scripts/quality_check.py`

- [ ] **Step 1: 运行现有检查**

```bash
python3 batches/20260730-1231-natives-batch-02/chentong-perspective/scripts/quality_check.py
```

Expected: `PASS chentong-perspective`，证明旧检查存在漏检。

- [ ] **Step 2: 运行新结构的只读基线断言**

```bash
python3 -c "from pathlib import Path; p=Path('batches/20260730-1231-natives-batch-02/chentong-perspective/SKILL.md').read_text(); req=['角色扮演规则','回答工作流','核心心智模型','决策启发式','价值观与内部张力','来源附录']; missing=[x for x in req if x not in p]; assert not missing, missing"
```

Expected: FAIL，至少报告缺少角色规则、回答工作流、价值观与内部张力。

- [ ] **Step 3: 记录籍贯矛盾**

```bash
rg -n '广东梅州出身线索明确|小同乡.*推断' batches/20260730-1231-natives-batch-02/chentong-perspective/SKILL.md
```

Expected: 同时命中“明确”和“推断”口径。

### Task 2: 重写角色操作系统

**Files:**
- Modify: `batches/20260730-1231-natives-batch-02/chentong-perspective/SKILL.md`

- [ ] **Step 1: 收紧 frontmatter**

仅保留：

```yaml
---
name: chentong-perspective
description: 基于《临高启明》第三至第五卷原文，以陈同第一人称分析情报搜集、关系渗透、经费纪律、据点运营、局势汇报和内勤调度；当用户要求“以陈同视角/口吻”、询问陈同经历、决策、表达方式或要求比较陈同与高第时使用。必须区分原文明示、可证推断与未知，不得混入第八卷的陈小兵、陈识新或泛称“陈同志”。
---
```

- [ ] **Step 2: 写入角色规则和回答工作流**

加入进入/退出规则、一次性虚构声明、五类问题路由、按需读取 references、回答前事实分级。

- [ ] **Step 3: 展开六个心智模型**

每个模型固定包含：

```markdown
### 模型名称
**一句话：**
**来源证据：**
**应用方式：**
**局限性：**
```

- [ ] **Step 4: 加入决策启发式与表达约束**

覆盖经费、关系切口、报告环境、情报到行动、据点连续性、内勤分发和不确定性表达。

- [ ] **Step 5: 修正身份边界**

写明“十五六岁”为琼州任务时明示；“广东梅州或附近同乡网络”为基于“小同乡”的推断，原文没有直接写籍贯。

### Task 3: 重整研究材料和来源索引

**Files:**
- Modify: `batches/20260730-1231-natives-batch-02/chentong-perspective/references/research/01-writings.md`
- Modify: `batches/20260730-1231-natives-batch-02/chentong-perspective/references/research/02-conversations.md`
- Modify: `batches/20260730-1231-natives-batch-02/chentong-perspective/references/research/03-expression-dna.md`
- Modify: `batches/20260730-1231-natives-batch-02/chentong-perspective/references/research/04-external-views.md`
- Modify: `batches/20260730-1231-natives-batch-02/chentong-perspective/references/research/05-decisions.md`
- Modify: `batches/20260730-1231-natives-batch-02/chentong-perspective/references/research/06-timeline.md`
- Modify: `batches/20260730-1231-natives-batch-02/chentong-perspective/references/sources/SOURCE_INDEX.md`

- [ ] **Step 1: 为每份研究材料增加证据等级**

每条关键结论标注 `明示`、`推断` 或 `未知`，并给出卷名与原文行号。

- [ ] **Step 2: 校正统计口径**

第三卷 35 次、第四卷 25 次、第五卷 3 次，共 63 次“陈同”字符串命中；不把重复汇编或第八卷“陈同志”计入。

- [ ] **Step 3: 保留 14 个核心锚点**

锚点覆盖佛山随行、琼州测试、海家调查、经费表、内宅管事、海家渗透、资产判断、临高结算、码头建设、码头驻守、局势口述、广州总事务长、广州追踪任务和第五卷带队入城。

### Task 4: 强化确定性检查

**Files:**
- Modify: `batches/20260730-1231-natives-batch-02/chentong-perspective/scripts/quality_check.py`

- [ ] **Step 1: 检查 frontmatter 键**

解析 frontmatter，断言键集合严格等于 `{'name', 'description'}`。

- [ ] **Step 2: 检查结构与高风险事实**

断言必要章节、六模型字段、63 次统计、十四锚点和第八卷排除语句存在；若命中“广东梅州出身明确”等确定性表述则失败。

- [ ] **Step 3: 运行检查**

```bash
python3 batches/20260730-1231-natives-batch-02/chentong-perspective/scripts/quality_check.py
```

Expected: `PASS chentong-perspective`。

### Task 5: 前向测试、归档和提交

**Files:**
- Modify: `batches/20260730-1231-natives-batch-02/chentong-perspective.zip`
- Verify: `batches/20260730-1231-natives-batch-02/chentong-perspective/**`

- [ ] **Step 1: 前向测试角色回答**

测试：

```text
陈同如何用二十两活动经费调查海述祖？用陈同第一人称说明。
陈同是不是广东梅州人？请区分原文明示和推断。
```

Expected: 第一题分清“给二十两”和“实际花四两三钱”；第二题不得把“小同乡”升级为明示籍贯。

- [ ] **Step 2: 重建 ZIP**

从批次目录运行确定性压缩，只包含 `chentong-perspective/`。

- [ ] **Step 3: 比较 ZIP 与源码**

列出 ZIP 清单并核对 `SKILL.md`、六份 research、`SOURCE_INDEX.md`、`quality_check.py` 均存在。

- [ ] **Step 4: 检查变更边界**

```bash
git status --short
git diff -- batches/20260730-1231-natives-batch-02/chentong-perspective
```

Expected: 不改崇祯目录，不覆盖高第与无关 README 改动。

- [ ] **Step 5: 提交陈同相关改动**

只暂存陈同目录、陈同 ZIP、设计与计划文件，提交信息：

```text
fix: rebuild chentong perspective from source
```
