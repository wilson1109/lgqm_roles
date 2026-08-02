# Workflow: 单角色分发

## Trigger
路由器分类为 **DIRECT_CHARACTER** 时加载本文件。

## Protocol

1. **解析角色名**：从用户输入提取角色名/别名/外号
   - 查 `references/character-catalog.md` 中的触发词列表
   - 别名映射示例：督公→maqianzhu，杜女王→duwen，石翁→wangyehao，江局→jiangshan
2. **唯一匹配**：若命中唯一角色
   - 调用 `Skill(skill="<匹配的skill名>", args="<用户的原始查询>")`
   - 直接按该角色视角输出
3. **多候选匹配**（2-5 个角色都命中关键词）：
   - 列出候选，标注各自擅长领域
   - 询问用户："你要用 [A] 的 [领域1] 视角，还是 [B] 的 [领域2] 视角？"
4. **无匹配**：转 `workflows/fallback.md`

## Output Format

按被调用角色 skill 的视角输出。若用户请求是"分析 X"，则用角色视角分析；若是"写一段对话"，则按角色 voice 写对白。

## 边界
- 不混合其他角色视角（单角色场景）
- 不补充角色 skill 之外的设定知识（除非用户明确要求）
