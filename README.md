# lgqm_roles

《临高启明》角色视角 Skills。每个 `*-perspective/` 目录是一套可安装的角色视角 skill，用于写作、分析、设定复核和角色口吻模拟。

> 本 Skill 由 [女娲 · Skill造人术](https://github.com/alchaincyf/nuwa-skill) 生成  
> 创建者：[花叔](https://x.com/AlchainHust)  
> 角色版权：临高启明同人作者 | 蒸馏用途：角色研究/思维训练

## 本次更新

- 将 36 个元老角色 skill 统一整理到 `归档/`，每个目录旁提供同名 `.zip`。
- 按 `maqianzhu-perspective` 标准返工：补齐 `SKILL.md`、`scripts/`、`references/research/01-06` 和 `references/sources/SOURCE_INDEX.md`。
- 重新打包 36 个元老 zip，压包时排除 `.DS_Store`。
- 新增第一批归化民/土著角色目录：`batches/20260729-1851-natives-batch-01/`，共 15 人。
- 已完成本地检查：元老目录 36/36 通过，元老 zip 36/36 通过；第一批归化民/土著目录 15/15 通过，zip 15/15 通过。

## 目录组织

```text
归档/
├── [person]-perspective/
├── [person]-perspective.zip
└── ...

batches/
└── YYYYMMDD-HHMM-[topic]-batch-NN/
    ├── [person]-perspective/
    └── [person]-perspective.zip
```

后续新增角色按批次进入 `batches/`，每批最多 15 人；确认稳定后再移动到 `归档/` 或单独发布。

## Nuwa 标准结构

AI 有时不能稳定遵循 `nuwa-skill` 的标准格式，蒸馏完成后建议人工复核文件结构。标准结构如下：

```text
.claude/skills/[person-name]-perspective/
├── SKILL.md
├── scripts/
└── references/
    ├── research/
    │   ├── 01-writings.md
    │   ├── 02-conversations.md
    │   ├── 03-expression-dna.md
    │   ├── 04-external-views.md
    │   ├── 05-decisions.md
    │   └── 06-timeline.md
    └── sources/
```

## 已归档元老 Skills

| Skill | 角色 | 说明 |
|-------|------|------|
| `beiwei-perspective` | 北炜 | 特侦队指挥官。雷州参谋旅行与唐僧计划执行者，强调侦察先于行动、暴力服务政治、纪律具体到口令禁射撤退。 |
| `changshide-perspective` | 常师德 | 雷州糖业现场组织者。华南糖厂基层秩序、共同基金与米糖航线操盘手。 |
| `chengyongxin-perspective` | 程咏昕 | 大图书馆台湾女元老，古汉语专业出身。女仆案政治操盘手，现实主义女权策略家。 |
| `chensigen-perspective` | 陈思根 | 特侦训练、救援干涉、军粮营养、食品保存与身体管理视角。 |
| `chentianxiong-perspective` | 谌天雄 | 雷州情报负责人，明面身份是糖厂机械调试。擅长策反、收买、分化和低可见度情报工作。 |
| `duwen-perspective` | 杜雯 | 政策咨询组成员、妇联推动者、署名“尧龙女侠”的评论作者。偏革命话语、女性权利和群众动员。 |
| `guoyi-perspective` | 郭逸 | 广州站负责人、紫字号经营者。半公开情报商业节点，重视档案、账目、关系、信用和撤退路线。 |
| `jiangshan-perspective` | 江山 | 对外情报局局长型情报组织者。处理公开情报、跨部门协调、秘密行动、风险排序和外部势力研判。 |
| `limei-perspective` | 李梅 | 经济产业省商业部部长。妇女合作社、美美百货、渠道定价和社交型商业系统操盘者。 |
| `linbaiguang-perspective` | 林佰光 | 敌工部与策反专家。海盗招抚、广州特务机关和旧关系制度化的统战工程师。 |
| `linmotian-perspective` | 林默天 | 卫生口元老，防疫指挥部主任。危机处置、规程建设和医疗组织秩序视角。 |
| `liuxiang-perspective` | 刘翔 | 广州特别市市长，“琼山经验”创造者。程序员/PM 出身的城市治理折腾派。 |
| `luwenyuan-perspective` | 鹿文渊 | 山东工程据点负责人。难民收容、前线后勤、码头仓库兵站和据点建设视角。 |
| `maqianzhu-perspective` | 马千瞩 | 穿越三巨头之国务卿，元老院计划经济总设计师。资源分配、工业化和工程师治国视角。 |
| `minglang-perspective` | 明朗 | 元老院办公厅组织处处长。干部任用、编制流程、机构规则和组织技术视角。 |
| `mingqiu-perspective` | 明秋 | 伏波军海军部长、大洋舰队总顾问、海军少将。舰队建设、训练、煤水锅炉弹药和海军专业主义视角。 |
| `mumin-perspective` | 慕敏 | 广州警察局长，明朗之妻。从审俘到治安的系统建设者，擅长警务摸底、尺度控制和快速处置。 |
| `panpan-perspective` | 潘潘 | 《临高时报》常务副总编辑，丁丁伴侣。新闻伦理、舆论包装和现实妥协之间的媒体视角。 |
| `qianduoduo-perspective` | 钱朵朵 | 小仓号元老船长、佛山警务科长。海事、警务、证据程序和强制力使用视角。 |
| `salinna-perspective` | 萨琳娜 | 美国 ATF 前执法人员，强力部门客卿与警政顾问。外来者、人身安全、证据程序和武器控制视角。 |
| `wendeshi-perspective` | 文德嗣 | 穿越三巨头之首，虫洞发现者，元老院主席。量化管理、贸易立国和关键时刻最小干预视角。 |
| `wentong-perspective` | 文同 | 华南糖厂负责人、制糖工艺技术员。制糖工艺、成本结构、收购信誉和海义堂商业战视角。 |
| `wude-perspective` | 邬德 | 穿越集团“大管家”。工分制、信用秩序、民政组织和人性现实主义管理视角。 |
| `wunanhai-perspective` | 吴南海 | 农林水产相。粮食安全、种子饲料、水利运输、农垦产权和技术转让的农业账本视角。 |
| `wushimang-perspective` | 吴石芒 | 临高教会与百仞修道院经营者。把教会作为组织资产、思想工作入口、礼仪平台和社会改造工具。 |
| `xiaozishan-perspective` | 萧子山 | 穿越三巨头之办公厅主任，元老院首席人事操盘手。程序、人情和危机分层布控视角。 |
| `xueziliang-perspective` | 薛子良 | 侦查总局特侦负责人。反游击、枪械来源、治安战、公共安全和可验证情报视角。 |
| `xuyingjie-perspective` | 徐营捷 | 化工部火工品实验与特战装备负责人。雷汞、硝化甘油、苦味酸和装备实测视角。 |
| `zengkun-perspective` | 曾坤 | 化工元老，行动优先主义者。化学药路线、工业党执政论和快速执行视角。 |
| `zhangxiao-perspective` | 张枭 | 制药工程师元老、南海县长。工业口转地方治理，擅长绕过流程、囤积资源和变废为宝。 |
| `zhangyingchen-perspective` | 张应宸 | 号盗泉子，新道教创始人。道教、医学、科普、组织建设与情报渗透混合视角。 |
| `zhangyunmi-perspective` | 张允幂 | 芳草地小元老到广州综合办公室行政干部。公文摘要、会议执行和青年行政视角。 |
| `zhaomanxiong-perspective` | 赵曼熊 | 政治保卫系统设计者与执行者。侦查网、内务安全、强制力边界和安全机关制度化视角。 |
| `zhaoyingong-perspective` | 赵引弓 | 江南外派元老，凤凰山庄与招商局操盘者。江南商业统战、丝业控制、士绅渠道和风险隔离视角。 |
| `zhengmingjiang-perspective` | 郑明姜 | 医疗元老。定量诊断、药监标准化、伦理实用主义和冷面专业判断视角。 |
| `zhumingxia-perspective` | 朱鸣夏 | 步兵训练政工干部。两广攻略、梧州战役、治安战、训练补给地形民心视角。 |

## 第一批归化民/土著 Skills

| Skill | 角色 | 说明 |
|-------|------|------|
| `fuwuben-perspective` | 符悟本 | 刘三徒弟、归化民医生、防疫所医生。中医巡诊、鼠疫与广州防疫视角。 |
| `gaodi-perspective` | 高弟 | 高家小厮、早期儿童线人和跑外管事。广州街面、郭逸与琼州站情报视角。 |
| `gaoju-perspective` | 高举 | 广州士绅、高家东主、工商联合会主席。地方协商和士绅合作视角。 |
| `huangande-perspective` | 黄安德 | 山东旧军出身的归化民军官。军纪、住房、老兵兄弟和新军秩序视角。 |
| `huangping-perspective` | 黄平 | 黄禀坤书童、芳草地学生、税务调查员。教育跃迁和经济犯罪调查视角。 |
| `liangcunhou-perspective` | 梁存厚 | 广州士子、玉源社成员。髡学、中体西用和士子改革视角。 |
| `liluoyou-perspective` | 李洛由 | 广州大商人。润世堂、髡货、德隆钱庄、火器贸易和早期外部观察视角。 |
| `linming-perspective` | 林铭 | 锦衣卫旧人、佛山社会科长。梁家案、旧制度情报和广州治理视角。 |
| `liyongxun-perspective` | 李永薰 | 李小旗之女、户籍警、佛山借调警员。澳门跟踪、审讯和女警务视角。 |
| `lucheng-perspective` | 陆橙 | 女归化民政保干部。政保培训、惠州药品案、炉石散和郑明姜线视角。 |
| `mapeng-perspective` | 马蓬 | 长工出身的东门警察、南宝副所长。工分、买米、拒贿和基层警务视角。 |
| `pengshouan-perspective` | 彭寿安 | 杨山知县降官顾问、县办公室主任。地方士绅、县衙经验和剿匪建议视角。 |
| `wangchuyi-perspective` | 王初一 | 杨山县长、归化民干部。合理负担、地方治理和剿匪冒进教训视角。 |
| `yangerdong-perspective` | 杨二东 | 旧官兵、国民军士兵、伍长。旧兵习气、纪律转化、梧州与杨山剿匪视角。 |
| `yaoyulan-perspective` | 姚玉兰 | 佛山姚家女、政保见习协理员、税务经济犯罪干部。冷面女干部视角。 |

## 使用方式

### Claude Code

将需要的 `归档/*-perspective/` 或 `batches/*/*-perspective/` 目录复制到项目的 `.claude/skills/` 下。

### Codex

将需要的 `归档/*-perspective/` 或 `batches/*/*-perspective/` 目录复制到 `$CODEX_HOME/skills/` 下。安装后直接点名角色即可触发，例如：

- “用吴南海视角看粮食安全”
- “用文同视角分析雷州糖业”
- “用黄安德视角分析归化民军官”
- “用李洛由视角判断澳宋贸易信誉”

## 质量检查

每个标准目录应至少包含：

- `SKILL.md`
- `scripts/`
- `references/research/01-writings.md`
- `references/research/02-conversations.md`
- `references/research/03-expression-dna.md`
- `references/research/04-external-views.md`
- `references/research/05-decisions.md`
- `references/research/06-timeline.md`
- `references/sources/SOURCE_INDEX.md`

角色材料较少时，应在 `诚实边界` 中说明材料限制，不要硬编。
