# 20260731-1048 natives batch 03

状态：当前目录保留 6 人；本批专门处理《临高启明》中归化民与土著角色，全员统一遵循 `chongzhen-perspective` 崇祯范本（思维操作系统版）。

## 当前名单（6 人）

| # | Skill | 角色 | 来源 | 描述/锚点 |
|---:|---|---|---|---|
| 1 | `zengjuan-perspective` | 曾卷 | 原著 md；`natives.md` | 广州社学学生，香蜡店少东，考取公职成为广州特别市财税局青年干部。 |
| 2 | `changqingyun-perspective` | 常青云 | 原著 md；`natives_local.md` | 明朝举人，原何如宾/熊文灿幕僚，梧州绝户计、俘营求生与三合嘴暴乱线索人物。 |
| 3 | `fubuer-perspective` | 符不二 | 原著 md；`natives.md` | 临高美洋村地主，天地会合作、纳粮清丈、标兵红利与经营地主转型见证人。 |
| 4 | `huangxiong-perspective` | 黄熊 | 原著 md；`natives.md` | 明军旧把总/旧营兵出身的归化军官，教导营、矿区护卫、发动机行动与连阳治安战人物。 |
| 5 | `yangshixiang-perspective` | 杨世祥 | 原著 md；`natives.md` | 临高润世堂药铺掌柜，刘三方子、成药经营、分号扩张与混合所有制药企线索人物。 |
| 6 | `zhaofengtian-perspective` | 赵丰田 | 原著 md；`natives.md` | 梧州市办秘书，公文链路、首长服务、蔡兰事件、夜袭善后与听证会线索人物。 |

## 复核口径
- `extract_evidence.py` 只配置当前 6 人；运行时从 `/Users/gao/Library/Mobile Documents/com~apple~CloudDocs/旅顺口写作计划/原著/md/临高启明全本.md` 抽取逐字证据。
- 每个 Skill 包含标准的 `SKILL.md`、`references/research/` 01-06 文件、`references/sources/SOURCE_INDEX.md`、`references/sources/EVIDENCE.jsonl` 及 `scripts/quality_check.py`。
- 批次级验收以 `python3 /Users/gao/Documents/lgqm/verify_batch.py /Users/gao/Documents/lgqm/batches/20260731-1048-natives-batch-03` 为准。
