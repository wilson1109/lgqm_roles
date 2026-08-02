---
name: lgqm-writing
description: >
  临高启明同人写作智能路由器。当用户要写临高启明同人文、讨论临高剧情、
  设计角色对白、需要角色视角、构建场景、构思剧情、设定复核，或提到"临高启明"
  "同人""写文""穿越""元老院""澳宋""髡贼""角色对话""场景写作"且涉及临高世界时使用。
  自动识别场景、匹配并调用对应的角色 perspective skill（81+ 个）。
  支持：指定角色写作 / 场景驱动角色推荐 / 多角色对话编排 / 世界观一致性审查。
triggers:
  - 临高启明
  - 同人写作
  - 临高同人
  - 元老院
  - 澳宋
  - 髡贼
  - 穿越小说
  - 临高视角
  - 角色对话
  - 场景写作
---

# 临高启明同人写作智能路由器

本 skill 是 81+ 个角色 perspective skill 的统一入口。它**不替代**角色 skill，而是在正确的时机调用正确的角色 skill，并在多角色场景中编排它们。

## 核心原则

1. **角色 skill 是唯一事实源**：具体角色知识、语气、心智模型都在 `*-perspective/SKILL.md` 中，本 skill 只负责路由和编排
2. **先读目录，再调用**：匹配前必须查阅 `references/character-catalog.md` 和 `references/domain-index.md`
3. **多角色要编排**：多角色场景不是简单拼接，而是有主次、有过渡、有冲突的对位
4. **不越俎代庖**：当用户明确指定角色时，直接调用；当不确定时，推荐后请用户确认

## 路由协议

### Phase 1: 意图分类

将用户请求分为四类：

| 类型 | 判定 | 转交 |
|------|------|------|
| **DIRECT_CHARACTER** | 用户点名角色名/别名/外号（"用北炜视角""萧子山会怎么处理""督公怎么看"） | `workflows/single-character.md` |
| **SCENARIO_WRITING** | 用户描述场景未点名角色（"写雷州糖厂的冲突戏""元老在会议上争论工业化"） | `workflows/scenario-recommend.md` |
| **MULTI_CHARACTER** | 用户要多个角色互动（"让杜雯和萧子山辩论""刘翔慕敏郭逸三人会议"） | `workflows/multi-character.md` |
| **LORE_CHECK** | 用户问设定/世界观一致性（"澳洲人能造蒸汽机吗""这段符不符合临高设定"） | `workflows/lore-check.md` |

### Phase 2: 匹配

1. 在 `character-catalog.md` 中查找角色名、别名、触发词
2. 在 `domain-index.md` 中按领域标签模糊匹配（场景/主题关键词）
3. 在 `scenario-mapping.md` 中按场景类型查推荐领域组合
4. 综合三个来源计算置信度，选 top-3

**匹配优先级**：scenario-mapping 推荐 > domain-index 领域匹配 > 纯关键词匹配

### Phase 3: 调用

调用角色 skill，使用 `Skill` 工具：

```text
Skill(skill="beiwei-perspective", args="[用户的原始查询]")
```

多角色场景先调用主视角，再调用次级视角，最后合成。

### Phase 4: 合成输出

- 单角色：直接按该角色 skill 的视角输出
- 多角色：按角色 skill 的各自视角交替叙述，标注角色名，保持各自 voice
- 场景推荐：给出 top-3 推荐及理由，请用户确认后再调用
- 设定检查：给出一致性结论（一致 / 需调整 / 与原著冲突）+ 依据

## 回退策略（Fallback）

| 情况 | 行为 |
|------|------|
| **无匹配** | 不拒绝。从 `character-catalog.md` 输出分类摘要，引导用户缩小范围。提示关键词：雷州/广州/山东/江南/军事/政治/商业/医疗/教育... |
| **匹配过多**（>5 个） | 按优先级选 top-5，告知"还有 N 个可选角色，需要更精确筛选？" |
| **Skill 调用失败** | 返回部分结果 + 标注"以下角色未能加载：[name]"，提示检查 `*-perspective/` 是否已安装 |
| **用户输入太模糊** | 读 `workflows/fallback.md`，按其澄清流程处理 |

## 写作质量要求

1. **设定一致性**：调用角色 skill 前，如涉及技术/制度细节，先想清楚当前时间线
2. **角色 voice**：每个角色的表达 DNA 来自其 skill，不可互换
3. **本时空人物主体性**：明朝人、归化民不是背景板，要有合理动机
4. **技术可行性**：写工业/军事时遵循"原料→能源→人才→供应链"链条
5. **反模式**：不写全能元老、不写瞬间接受现代价值的明朝人、不靠一场会议解决所有矛盾

## 文件索引

| 文件 | 用途 |
|------|------|
| `references/character-catalog.md` | 全角色速查表（自动生成，勿手改） |
| `references/domain-index.md` | 领域→角色映射（自动生成，勿手改） |
| `references/scenario-mapping.md` | 场景→领域标签映射（手动维护） |
| `references/writing-principles.md` | 同人写作方法论 |
| `scripts/build_catalog.py` | 重建 catalog（新增角色后运行） |
| `workflows/*.md` | 分场景的详细处理流程 |

## 新增角色后的操作

1. 将 `new-character-perspective/` 放入任一分类目录（源仓库）或平铺（安装后）
2. 运行 `python lgqm-writing/scripts/build_catalog.py`
3. 如涉及新场景类型，手动更新 `scenario-mapping.md`
