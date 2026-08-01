# 20260730-1643 historical batch 01

状态：进行中；本批专门处理《临高启明》中真实存在的明末历史人物。当前主名单 10 人，不追求凑满 15 人；后续逐人蒸馏为 `*-perspective/` 目录和同名 zip。

已完成：`sunyuanhua-perspective`、`chenzizhuang-perspective`、`xuguangqi-perspective`、`huangtaiji-perspective`、`lizicheng-perspective`、`yangsichang-perspective`。

## 选人规则

- 只收真实历史人物，不收元老、原创土著/归化民、架空组织人格。
- 主名单按用户指定范围和本地原文提及量共同确定，源路径遵守根 README 硬规则：`/Users/gao/Library/Mobile Documents/com~apple~CloudDocs/旅顺口写作计划/原著/md`。
- 蒸馏对象是“小说文本中的历史人物形象”，不是通用史学传记；史实只做边界校对，不能替代原文锚点。
- `SOURCE_INDEX.md` 和 research 情节锚点只能写入原著 md 位置；不得把人物库、草稿、外部史料当情节证据。
- 崇祯皇帝已有 `明朝真实历史人物蒸馏/chongzhen-perspective/`，本批只列为参照，不重复占名额。

## 主名单

| # | Skill | 角色 | 原文提及量 | 备注 |
|---:|---|---|---:|---|
| 1 | `sunyuanhua-perspective` | 孙元化 | 2286 | 已完成。登莱、西法火器、髡器/髡术认知接口。 |
| 2 | `wangyehao-perspective` | 王业浩（石翁） | 2227 | 兵部侍郎、石翁集团首脑、周乐之/天书/反髡谋划线。 |
| 3 | `xiongwencan-perspective` | 熊文灿 | 1295 | 两广总督、剿抚夹缝和广东失守责任线。 |
| 4 | `wentiren-perspective` | 温体仁 | 469 | 崇祯朝阁臣、宫廷政治和剿抚话术接口。 |
| 5 | `chenzizhuang-perspective` | 陈子壮 | 465 | 已完成。广东士人官僚、地方危局和朝廷奏议线。 |
| 6 | `xuguangqi-perspective` | 徐光启 | 381 | 已完成。西学、火器、士大夫技术派和李洛由委托线。 |
| 7 | `huangtaiji-perspective` | 皇太极 | 325 | 已完成。后金/清方最高决策者，辽东外压线。 |
| 8 | `yangsichang-perspective` | 杨嗣昌 | 116 | 已完成。乾清宫召对、攘外安内、十面张网、剿饷/粤饷、熊文灿和孙元化判断线。 |
| 9 | `lizicheng-perspective` | 李自成 | 95 | 已完成。低证据；流寇动员、闯王闲子、内乱压力和明末崩溃背景。 |
| 10 | `zhengchenggong-perspective` | 郑成功 | 84 | 郑氏后继、海上政权想象和东南长期伏笔。 |

## 已有参照

| Skill | 角色 | 位置 | 备注 |
|---|---|---|---|
| `chongzhen-perspective` | 崇祯皇帝朱由检 | `明朝真实历史人物蒸馏/chongzhen-perspective/` | 已完成旧目录；可作为本批真实历史人物蒸馏结构参照。 |

## 候补池

| Skill | 角色 | 原文提及量 | 备注 |
|---|---|---:|---|
| `hongchengchou-perspective` | 洪承畴 | 52 | 辽东、剿寇和降清前后线。 |
| `nuerhachi-perspective` | 努尔哈赤 | 46 | 后金起点和辽东压力来源。 |
| `zhangxianzhong-perspective` | 张献忠 | 37 | 流寇并行线。 |
| `shangkexi-perspective` | 尚可喜 | 36 | 辽东军头和降清线。 |
| `duoergun-perspective` | 多尔衮 | 33 | 清方后续权力核心。 |
| `gaoyingxiang-perspective` | 高迎祥 | 30 | 早期流寇线。 |
| `wusangui-perspective` | 吴三桂 | 30 | 关宁军、辽东和后续入关节点。 |
| `fanwencheng-perspective` | 范文程 | 21 | 清方汉臣谋略接口。 |
| `luxiangsheng-perspective` | 卢象升 | 21 | 崇祯朝军事勤王与战死样本。 |
| `zudashou-perspective` | 祖大寿 | 18 | 关宁军和辽东防线。 |

## 蒸馏口径

- 每个人物先跑本地原文检索，抽取全部可用锚点，再决定是否进入完整蒸馏。
- 对真实历史人物必须区分三层：小说中明确写出的言行、小说角色对其评价、现实史实背景。
- 材料少的人物可以做“低证据 skill”，但要在 `诚实边界` 明确说明，不硬编心理模型。
- 每个完成目录应包含 `SKILL.md`、`references/research/01-06`、`references/sources/SOURCE_INDEX.md`、`scripts/quality_check.py` 和同名 zip。
