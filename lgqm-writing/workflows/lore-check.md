# Workflow: 世界观一致性检查

## Trigger
路由器分类为 **LORE_CHECK** 时加载本文件。

## Protocol

1. **分类问题**：
   - 技术可行性问题（"澳洲人 1635 年能造蒸汽机吗？"）
   - 制度/政治问题（"元老院和归化民的关系怎么设定？"）
   - 角色行为问题（"杜雯会怎么处理这种情况？"）
   - 时间线问题（"登莱之乱发生在第几卷？"）
2. **调用相关角色 skill**：
   - 技术问题 → `Skill(skill="maqianzhu-perspective", args="...")`、`Skill(skill="wentong-perspective")` 等技术角色
   - 政治问题 → `Skill(skill="xiaozishan-perspective")` 等政治角色
   - 角色行为 → 对应角色
3. **综合判定**：
   - 一致：给出依据（来自哪个角色的 research 材料）
   - 需调整：指出矛盾点，给出调整方向
   - 与原著冲突：明确标注，避免误写

## Output Format

```markdown
判定：一致 / 需调整 / 与原著冲突

依据：
- [角色] 的 research 材料显示：[原文/锚点摘要]
- [细节点] 在 [卷] 中 [状态]

调整建议（如适用）：
- ...
```

## 边界
- 只依据本地角色 skill 的 research 材料，不臆造原著内容
- 材料不足时明确标注"材料限制"，不硬编
