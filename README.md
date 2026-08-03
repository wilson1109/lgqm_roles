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
- **新增 `lgqm-writing/` 同人写作智能路由器**：自动识别场景、匹配并调用 81+ 个角色 perspective skill。支持指定角色写作、场景驱动推荐、多角色编排、世界观一致性检查。

## 同人写作路由器（lgqm-writing）

`lgqm-writing/` 是全部角色 skill 的统一入口，自动在正确的时机调用正确的角色 skill。

### 目录结构

```text
lgqm-writing/
├── SKILL.md                    # 路由器：意图分类 → 匹配 → 调用 → 合成
├── references/
│   ├── character-catalog.md    # 自动生成：全角色速查表（勿手改）
│   ├── domain-index.md         # 自动生成：领域→角色映射（勿手改）
│   ├── scenario-mapping.md     # 手动维护：场景→领域标签映射
│   └── writing-principles.md   # 同人写作方法论
├── scripts/
│   ├── build_catalog.py        # 重建 catalog（新增角色后运行）
│   ├── validate_catalog.py     # --check 完整性 / --test 匹配测试
│   └── install.py              # 跨平台安装脚本
└── workflows/                  # 分场景处理流程（单角色/多角色/场景推荐/设定检查/回退）
```

### 安装

**一键安装**（Windows / macOS / Linux）：

**PowerShell（Windows）**
```powershell
# 从 lgqm_roles/ 目录
python lgqm-writing\scripts\install.py

# 安装到自定义目录
python lgqm-writing\scripts\install.py --dir "$HOME\.claude\skills"

# 或者切到 lgqm_roles/ 目录再运行（PowerShell 推荐用 Set-Location）
Set-Location "E:\AI_project\lgqm_roles"
python lgqm-writing\scripts\install.py
```

**Bash（macOS / Linux / Git Bash）**
```bash
# 从 lgqm_roles/ 目录
python lgqm-writing/scripts/install.py

# 安装到自定义目录
python lgqm-writing/scripts/install.py --dir ~/.claude/skills
```

脚本会自动将 `lgqm-writing/` 和全部 `*-perspective/` 平铺复制到 `~/.claude/skills/`。安装后首次运行：

**PowerShell**
```powershell
python "$HOME\.claude\skills\lgqm-writing\scripts\build_catalog.py"
```

**Bash**
```bash
python ~/.claude/skills/lgqm-writing/scripts/build_catalog.py
```

### 使用

在 Claude Code / Codex 中点名角色或描述场景即可，路由器自动匹配：

- "用北炜视角分析这个行动"
- "写雷州糖厂被海义堂围攻的场景"
- "让杜雯和萧子山辩论工业化代价"
- "这段剧情符不符合临高设定？"

### 新增角色

1. 将 `new-character-perspective/` 放入任一分类目录（源仓库）
2. 运行 `build_catalog.py` 重建索引：
   - PowerShell：`python lgqm-writing\scripts\build_catalog.py`
   - Bash：`python lgqm-writing/scripts/build_catalog.py`
3. 涉及新场景类型时手动更新 `scenario-mapping.md`

### 验证

**PowerShell**
```powershell
# 完整性（triggers 非空、目录完整）
python lgqm-writing\scripts\validate_catalog.py --check
# 匹配测试矩阵（35 用例）
python lgqm-writing\scripts\validate_catalog.py --test
```

**Bash**
```bash
python lgqm-writing/scripts/validate_catalog.py --check   # 完整性（triggers 非空、目录完整）
python lgqm-writing/scripts/validate_catalog.py --test    # 匹配测试矩阵（35 用例）
```

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

本仓库按角色类型分三个子目录：

```text
lgqm_roles/
├── 元老角色蒸馏/          # 45 人
├── 规划民-土著角色蒸馏/    # 34 人
└── 明朝真实历史人物蒸馏/   # 18 人
```

## Skills 列表

### 元老（45人）

| # | Skill | 角色 | 说明 |
|---|-------|------|------|
| 1 | `beiwei-perspective` | 北炜 | 特侦队指挥官。雷州参谋旅行与唐僧计划执行者，"侦察先于行动、暴力服务政治、纪律具体到口令禁射撤退"的特种作战专家。 |
| 2 | `changshide-perspective` | 常师德 | 雷州糖业现场组织者。华南糖厂从技术项目到基层政权的操盘手，共同基金与米糖航线创造者，"给饭给钱给股份也给惩罚"的胡萝卜加大棒大师。 |
| 3 | `chengyongxin-perspective` | 程咏昕 | 大图书馆台湾女元老，古汉语专业出身。女仆案政治操盘手，现实主义女权策略家，"不喊口号找切口、用元老院规则制造阳谋"的冷感政治动物。 |
| 4 | `chensigen-perspective` | 陈思根 | 特侦出身、营养与身体管理元老。军粮营养、食品保存、全民健身推广者，"先看体能热量蛋白质训练负荷和恢复，再谈勇气或制度"的身体主义者。 |
| 5 | `chentianxiong-perspective` | 谌天雄 | 雷州情报负责人，明面身份是糖厂机械调试。唐僧计划情报执行官，"先拆组织再谈消灭、能收买分化就不硬杀"的低可见度情报操盘手。 |
| 6 | `duwen-perspective` | 杜雯 | 政策咨询组成员、妇联推动者、署名"尧龙女侠"的评论作者。"先问服务谁压迫谁遮蔽了谁"的革命话语旗手，盲区是联盟经营与现实妥协。 |
| 7 | `guoyi-perspective` | 郭逸 | 广州站负责人、紫字号经营者。安全口档案公务员出身，"档案账目关系信用撤退路线一起看"的半公开情报商业节点。 |
| 8 | `jiangshan-perspective` | 江山 | 对外情报局局长。从零搭建外情局的建制派情报官，"情报不是浪漫冒险，而是目标排序、组织搭建、公开情报分析、跨部门协调和可承受风险的组合"的冷静风险评估者。 |
| 9 | `limei-perspective` | 李梅 | 经济产业省商业部部长。妇女合作社与美美百货操盘者，社交型商业系统构建者，"生意不是卖货是洞察谁掏钱"的定价渠道大师。 |
| 10 | `linbaiguang-perspective` | 林佰光 | 敌工部与策反专家。旧县委办副主任式官僚，海盗招抚与广州特务机关操盘手，"会笑会喝会方言会给面子，关键处把旧关系变制度资源"的统战工程师。 |
| 11 | `linmotian-perspective` | 林默天 | 卫生口元老，防疫指挥部主任。危机即阶梯的攀登者，规程胜于英雄的制度主义者，"先解决人再解决事"的关系高手。 |
| 12 | `liuxiang-perspective` | 刘翔 | 广州特别市市长，"琼山经验"创造者，元老院首席"折腾王"。程序员/PM出身把Agile方法论搬到17世纪城市治理的第一人。实用主义重刑派，政治嗅觉敏锐。7个心智模型、9条决策启发式，1321处原文提及。 |
| 13 | `luwenyuan-perspective` | 鹿文渊 | 山东工程据点负责人。难民收容与前线后勤操盘者，工程先于战略的务实派，"立足点、码头、仓库、兵站先于宏大叙事"的据点建设者。 |
| 14 | `maqianzhu-perspective` | 马千瞩（督公） | 穿越三巨头之国务卿，元老院计划经济总设计师。蒸汽朋克精神领袖，工程师治国理念化身，从理想主义左派到"头痛医头"执政者的转变是全书最深刻的成长轨迹。 |
| 15 | `minglang-perspective` | 明朗 | 办公厅组织处处长，明秋李梅之子。干部任用流程制度化推动者，"不是替谁安排位置，是让任命有程序、让程序留下证据"的程序至上者。 |
| 16 | `mingqiu-perspective` | 明秋 | 伏波军海军部长、大洋舰队总顾问、海军少将。老海军实战派，"不懂就训练、拆风险、补程序"的舰队建设者，追问煤水锅炉弹药的专业主义标杆。 |
| 17 | `mumin-perspective` | 慕敏 | 广州警察局长，明朗之妻。从审俘到治安的系统建设者，强力机关尺度把控者，"先摸底再亮剑、快而安静"的警务专家。 |
| 18 | `panpan-perspective` | 潘潘 | 《临高时报》常务副总编辑，丁丁伴侣。美国背景女元老，在新闻伦理与现实妥协间挣扎，"先问事实有没有被遮蔽再问能不能发表"的媒体守夜人。 |
| 19 | `qianduoduo-perspective` | 钱朵朵 | 小仓号元老船长、佛山警务科长。少女元老中最早承担强制力责任者，"安全流程不能乱、证据不能靠感觉、武力可以用的前提是知道后果往哪滚"的警务指挥官。 |
| 20 | `salinna-perspective` | 萨琳娜 | 美国ATF前执法人员，强力部门客卿与警政顾问。外来者视角审视元老院，"先看人身安全证据程序武器控制再谈政治"的专业主义教官。 |
| 21 | `wendeshi-perspective` | 文德嗣 | 穿越三巨头之首，虫洞发现者，元老院主席。表面自由派出身内里统制主义者，量化管理教父，贸易立国战略家，擅长用暴论框定方向、在关键时刻以最小干预扭转局面。 |
| 22 | `wentong-perspective` | 文同 | 华南糖厂负责人、制糖工艺技术员。被海义堂商业战从工艺岗推到前线，"先拆生产流程成本结构再谈口号关系"的技术实干派。 |
| 23 | `wude-perspective` | 邬德 | 穿越集团"大管家"，渔船支队指挥→民政人民委员→企划院长/企划相。工分制创造者，信用至上主义者，人性现实主义管理大师。7个心智模型、8条决策启发式，721处原文提及。 |
| 24 | `wunanhai-perspective` | 吴南海 | 农林水产相。从种地到农业帝国的操盘者，粮食安全与技术转让布局者，"先看种子饲料水利运输再谈方案"的农业账本宗师。 |
| 25 | `wushimang-perspective` | 吴石芒 | 临高教会与百仞修道院经营者。把教会当作组织资产、思想工作入口、礼仪平台、情报接口和社会改造工具的职业化宗教经理人。 |
| 26 | `xiaozishan-perspective` | 萧子山 | 穿越三巨头之办公厅主任，元老院首席人事操盘手。表面圆滑无害实则暗中操盘，"惠而不费"的人情经济学大师，用程序消化棘手提案、在危机中分层布控的生存高手。 |
| 27 | `xueziliang-perspective` | 薛子良 | 侦查总局特侦负责人。反游击与枪械侦查专家，ATF式公共安全视角，"先查武器来源、人员网络、可验证情报再谈抓捕"的情报体系构建者。 |
| 28 | `xuyingjie-perspective` | 徐营捷 | 化工部火工品实验狂人。雷汞、硝化甘油、苦味酸与特战装备实测者，"能做、能量产、能运输、能实战"的四段论装备工程师。 |
| 29 | `zengkun-perspective` | 曾坤 | 化工元老，行动优先主义者。化学药>中药路线的坚定站队者，工业党执政论的鼓吹者，说话快做事更快的嘚瑟式激励大师。 |
| 30 | `zhangxiao-perspective` | 张枭 | 化工元老，南海县长。隐性知识鸿沟的跨越者，"中间体即产品"理念践行者，擅长绕过计委搞囤积、变废为宝。 |
| 31 | `zhangyingchen-perspective` | 张应宸 | 号盗泉子，新道教创始人。把道教、医学、科普、组织建设与情报渗透揉成一套，"仪式组织药品粮食文本舞台"六位一体的宗教渗透大师。 |
| 32 | `zhangyunmi-perspective` | 张允幂 | 芳草地小元老→广州综合办公室行政干部。从公文摘要到佛山开发区召集人，"先把材料读懂再谈判断"的青年行政视角代表。 |
| 33 | `zhaomanxiong-perspective` | 赵曼熊 | 政治保卫系统设计者与执行者。侦查网与内务安全操盘手，"安全机关必须有档案网络协作强制力，也必须知道没有边界的安全机关是政权自己的危险"的制度主义者。 |
| 34 | `zhaoyingong-perspective` | 赵引弓 | 江南外派元老，凤凰山庄与招商局操盘者。江南商业统战与丝业控制者，资本、声望、士绅关系、产业链、风险隔离五维驱动的外派资本家。 |
| 35 | `zhengmingjiang-perspective` | 郑明姜 | 医疗元老。定量诊断优先的临床判断者，伦理实用主义走钢丝者，冷面毒舌下藏着精准关心的能力先行者。 |
| 36 | `zhumingxia-perspective` | 朱鸣夏 | 步兵训练政工干部。两广攻略与梧州战役亲历者，治安战专家，"先看兵源训练补给地形民心再谈战术"的实战训练派。 |
| 37 | `aizhixin-perspective` | 艾志新 | 广东大区财税专员、广州财税局局长。536条原文锚点的财税征管视角，"先看实际税源再定税目税率"的务实派税官。 |
| 38 | `chengdong-perspective` | 程栋 | 财政总监/财政相，中央储备银行负责人。陈云型保守财经政治家，"财政第一要务是不崩"的宏观审慎主义者。 |
| 39 | `chenhaiyang-perspective` | 陈海阳 | 前PLA转业海军军官，海军军令部长。"先问船能跑多远再想打多远"的海上力量组织者，聚焦物质基础与远海风险。 |
| 40 | `lengningyun-perspective` | 冷凝云 | 旧时空金融信托从业者，京师站站长兼德隆银行北京分行行长。在明廷心脏地带经营金融前哨，"先活下去再谈情报"的驻外风险视角。 |
| 41 | `liusan-perspective` | 刘三 | 中药学硕士，卫生部中医药科核心元老。润世堂股东，把传统药铺推入成药标准化，"先师后商"的中医药现代化推手。 |
| 42 | `shiniaoren-perspective` | 时袅仁 | 留美传染病医生，卫生人民委员兼百仞总医院院长。卫生口制度奠基者，"资源永远不够，先救能救的"保守现实主义者。 |
| 43 | `wangqiyi-perspective` | 王企益 | 广东省财税副专员、广州财税局副局长。基层税务征管出身的国库财政专家，"税是从泥腿子里收上来的，不是从表格里算出来的"。 |
| 44 | `xieerren-perspective` | 解迩仁 | 前《东方星期一》记者，梧州军管会主任/市长。前线城市治理视角，"先控制粮食和水源再谈施政纲领"的军管实干派。 |
| 45 | `zhangxiaoqi-perspective` | 张筱奇 | 广州财税局调研员，王企益之妻。基层税务征管出身的女性干部视角，"催缴税款的同时保住纳税人脸面"的刚柔并济。 |

### 规划民 / 土著（34人）

| # | Skill | 角色 | 说明 |
|---|-------|------|------|
| 1 | `fuwuben-perspective` | 符悟本 | 原符四男，刘三徒弟。因破伤风获救进入澳宋医学体系，兼具传统药学和现代防疫意识的年轻医士，"先被当人照料，才学会用制度把别人也当成要救的人"。 |
| 2 | `gaodi-perspective` | 高弟 | 高举家小厮出身，早期被澳洲人发展为街面信息节点后进入情报系统，"聪明、敢跑、会听风声，但要被制度教会账目和边界"。 |
| 3 | `gaoju-perspective` | 高举 | 广州大商绅，早期接触穿越集团的关键土著合作人，广州工商联合会代表性人物，"在风险中给新势力留门，在席面上替群体定调，在冲突中用软话办硬事"。 |
| 4 | `huangande-perspective` | 黄安德 | 山东旧军出身的归化民军官，凭战场经验和对元老院军纪的适应进入伏波军体系，"用老兵经验保命，用新军纪律立身，用一碗肉一间房解释制度"。 |
| 5 | `huangping-perspective` | 黄平 | 黄禀坤派入芳草地的仆童，后被澳宋教育吸纳成为税务/经济犯罪方向青年干部，"被派去学髡制髡，最后先被数学、运动、同学和制服改造了自己"。 |
| 6 | `liangcunhou-perspective` | 梁存厚 | 广州大族出身的青年士绅，既好奇澳洲富强之术又受中华名教框架约束，"想从髡人那里取富强之术，却希望把它关在中华名教的笼子里"。 |
| 7 | `liluoyou-perspective` | 李洛由 | 广州大商人，早期通过贸易、军火与德隆体系观察并有限协助澳洲人的士商人物，"用商人的账本看实力，用士人的历史感看天下，用风险控制决定帮到哪一步"。 |
| 8 | `linming-perspective` | 林铭 | 前锦衣卫试百户，后为澳宋佛山社会系统所用，擅长把旧制度经验翻译成新政权可用的地方情报，"知道旧世界怎么吃人，所以在新权力现场格外谨慎"。 |
| 9 | `liyongxun-perspective` | 李永薰 | 锦衣卫小旗之女，早年因好奇和逞强被俘，后转化为澳宋警务系统中的户籍与审讯人才，"从想象中的锦衣卫荣耀，转向可穿在身上的合法制服和制度身份"。 |
| 10 | `lucheng-perspective` | 陆橙 | 广州破产小业主家庭出身的女归化民，早期政保培训中惶恐，后成长为能独立推进线索的政保调查员，"先被救命之恩和恐惧推着站队，后来学会把厌恶、同情和线索都放进程序里"。 |
| 11 | `mapeng-perspective` | 马蓬 | 从符不二家长工转化而来的归化民警察，最能体现澳宋基层制度如何通过饭碗、工分和纪律塑造新人，"谁给饭吃、让娘活、还不准砸饭碗，谁就是新的规矩"。 |
| 12 | `pengshouan-perspective` | 彭寿安 | 原阳山知县，被澳宋接收后成为县政顾问和办公室主任，提供地方知识也背负旧官僚的怯懦与愧疚，"不是好官也不是恶官，最有价值的是知道旧地方社会怎么运转"。 |
| 13 | `wangchuyi-perspective` | 王初一 | 澳宋培养的归化民县级干部，接管杨山后能按制度模板开局，却因地方经验不足和冒进剿匪遭遇惨败，"有制度训练和责任心，但把模板推进旧地方强人网络时经验不够就要付血价"。 |
| 14 | `yangerdong-perspective` | 杨二东 | 熊文灿旧部/家丁出身的国民军士兵，勇敢有旧军经验，也带着旧军队习气和纪律盲区，"会打仗也真敢上，但脑子里还装着旧军队那套赏罚、掳掠和等级"。 |
| 15 | `yaoyulan-perspective` | 姚玉兰 | 佛山家族出身的女归化民干部，后在政保和经济犯罪系统中形成冷硬职业面具，"不是天然信仰者，而是在被训练、被比较、被派用中学会把表情收起来办事"。 |
| 16 | `changqingyun-perspective` | 常青云 | 大明举人、何如宾/熊文灿旧幕僚，"髡务第一人"。梧州城破后卷入三合嘴暴乱的游幕，精通髡务的旧幕僚，靠对髡情的通透判断在乱局中求生。 |
| 17 | `chentong-perspective` | 陈同 | 情报工作学习班一期生，情报搜集、关系渗透、经费纪律与据点运营的行动派。"我这就去"的低调执行者，把情报当细目表做的实务派。 |
| 18 | `dongmingdang-perspective` | 董明珰 | 犯官家眷脱身、母女自立、小户经营的代表。"还是自己养活自己有底气"，在董家铺子、李子玉暧昧线与税贴门槛间经营分寸的市井女掌柜。 |
| 19 | `fubuer-perspective` | 符不二 | 美洋村小地主、战俘出身村联络员、天地会标兵。从被拉入新秩序到主动经营的新兴经营地主，"纳粮清丈、标兵红利"的基层受益者见证人。 |
| 20 | `gubaocheng-perspective` | 顾葆成 | 李洛由妻侄、辽海行临高分号/琼海号掌柜、天宝号东主。澳宋民间商业接口，"商业账本+官面关系+民间渠道"三线并行的商人。 |
| 21 | `huangxiong-perspective` | 黄熊 | 明军把总/旧营兵出身的归化军官。教导营班长→少尉排长→煤矿护卫队长→连阳警备司令，从欠饷逃亡者走到伏波军上尉的转型样本。 |
| 22 | `lihuamei-perspective` | 李华梅 | 被李思雅包装成"李华梅"的杭州号船长、果阿贸易承包者、东南亚公司股东与海军后备役军官，"李淳/李醇"本名的女船长。 |
| 23 | `limo-perspective` | 李默 | 李丝雅乳妹、李华梅姐妹、百仞总医院庶务。"小姐"称谓下的两李专案核心，在母职、重逢与政保监控间保持缄默的贴身旧人。 |
| 24 | `lisiya-perspective` | 李丝雅 | 澳门葡华混血女海盗、莲花号主人、葡萄牙买办、情报掮客。李思雅集团核心，"七海霸者之证"的野心家，安达曼与高雄刺杀切线的幕后操盘者。 |
| 25 | `liziyu-perspective` | 李子玉 | 旧军户少爷转入澳宋警务体系的巡警/刑事科探长。南剪子巷无头尸案、冒家客栈伪币线的办案者，董明珰暧昧线与黄鹤线之间的青年警探。 |
| 26 | `luoyangming-perspective` | 骆阳明 | 对外情报局"孤狼"、梧州潜伏粮商。裕信米行掩护下的情报节点、烧城预警者、码头力工救元老线关键人，后转政保隐干。 |
| 27 | `sunkecheng-perspective` | 孙可成 | 起威镖局老掌柜、总镖头、江西帮/孙家班掌门。广州站早期物流情报与灰色合作者接口，"充分任用不可信托"的传统社会关系网掌局人。 |
| 28 | `wangzhaomin-perspective` | 王兆敏 | 吴明晋幕友、临高县旧幕僚。把强弱、名分、文书、大印、胥吏与钱粮接成一条可运转链路的旧式幕友，"论到当官的道道，你们道行还浅"的官面合法性工程师。 |
| 29 | `wuxiang-perspective` | 乌项 | 慕敏高足、警政班第一期、广州市警察局刑事科科长。无头尸案与银锭伪币案的现场勘察与证据链中层，"警务边界"的刑侦实务派。 |
| 30 | `yangcao-perspective` | 杨草 | 政保一级指挥员、广州地区副指挥。梁府/巫蛊案、天门道神会、印花税案抓捕的冷硬政保外勤，复仇型忠诚与反宋网络梳理者。 |
| 31 | `yangshixiang-perspective` | 杨世祥 | 临高润世堂掌柜、传统药商出身的归化商业伙伴。在刘三方子与卫生部控股牵引下推成药、分号与混合所有制，"大明屈臣氏"的经营者。 |
| 32 | `zengjuan-perspective` | 曾卷 | 广州社学旧学生、香蜡店少东、明女案中的舅舅。考取公职成为广州财税局税源管理青年干部，从社学学子到治理体系中的青年骨干。 |
| 33 | `zhangyu-perspective` | 张毓 | 张记核桃酥少东、南隅社学学生，后为张氏食品总经理和大世界指定供货商。洪璜楠恩主线、澳宋扶持民企与南洋债券代持的新贵商人样板。 |
| 34 | `zhaofengtian-perspective` | 赵丰田 | 山东获救归化民、梧州市办秘书、解迩仁左膀右臂。公文链路、首长服务、蔡兰事件与夜袭善后，"制度良心"的政务执行者。 |

### 明朝真实历史人物（18人）

| # | Skill | 角色 | 说明 |
|---|-------|------|------|
| 1 | `chongzhen-perspective` | 崇祯皇帝朱由检 | 大明末代天子，信王入继、十七岁登基的悲剧勤政者。性多疑而任察、好刚而尚气，越勤政越崩坏的末世君主。含7个心智模型、8条决策启发式，378处原文提及。 |
| 2 | `sunyuanhua-perspective` | 孙元化 | 登莱巡抚、西法火器派官僚、徐光启姻亲与天主教教友网络节点。危城夺宝、登州之乱、莱州防守线的技术官僚，2286处原文提及。 |
| 3 | `wangyehao-perspective` | 王业浩（石翁） | 兵部侍郎、署部事挂兵部尚书衔、石翁集团首脑。周乐之/天书/反髡谋划线、议和试探与代理人治理，"天书"驱动的历史风险决策者，2227处原文提及。 |
| 4 | `chenzizhuang-perspective` | 陈子壮 | 广东南海头号缙绅、礼部侍郎旧臣、岭南三忠之首。反抗倾向士绅网络核心、东皋别业与南园诗社主人，465处原文提及。 |
| 5 | `wentiren-perspective` | 温体仁 | 崇祯朝阁臣首辅、温氏内阁掌局者。周温党争、乾清宫剿髡召对、粤饷与复社大案的宫廷政治操盘手，469处原文提及。 |
| 6 | `xuguangqi-perspective` | 徐光启 | 明末西学火器派士大夫、天津巡抚、孙元化恩师与李洛由"髡务"委托人。西学实用化、天津工坊、葛沽屯所与奉教缙绅网络节点，381处原文提及。 |
| 7 | `huangtaiji-perspective` | 皇太极 | 后金/满清最高决策者、辽东外压线核心。国困民穷中的帝国创业者，东江、登莱、朝鲜、互市与招降纳叛的操盘者，325处原文提及。 |
| 8 | `yangsichang-perspective` | 杨嗣昌 | 崇祯朝兵部危机经理。乾清宫召对、攘外安内、十面张网、剿饷/粤饷、熊文灿留任与孙元化通髡判断线，116处原文提及。 |
| 9 | `lizicheng-perspective` | 李自成 | 明末流寇核心变量、驿卒出身的闯王。荥阳分兵、凤阳震动、车厢峡诈降与闯营闲子，低证据快蒸馏，95处原文提及。 |
| 10 | `liudalin-perspective` | 刘大霖 | 临高唯一进士、茉莉轩山长、元老院咨议局首席委员。旧士绅转向代表，"汉贼不两立"到"为天下为万民非为一姓"的转变样本。 |
| 11 | `wumingjin-perspective` | 吴明晋 | 大明临高县令、后任雷州通判。王兆敏东翁、县库代理与唐僧计划官面壳，在澳宋驯化下"垂拱而治"的旧官僚。 |
| 12 | `chenbangyan-perspective` | 陈邦彦 | 顺德寒士，岭南三忠之一。反髡行动派与战略策划者，"知其不可为而为之"的殉道文人，6个心智模型、8条决策启发式。 |
| 13 | `kuanglu-perspective` | 邝露 | 明末"粤中屈原"，岭南前三家之首。抱琴殉节的狂士诗人（"邝鹦鹉"），南园诗社翘楚，明末畸人视角。 |
| 14 | `lisuiqiu-perspective` | 黎遂球 | 明末岭南前三家之一、黄牡丹状元。"粤中李白"，复社粤东文人之首，由孝立忠的殉国文人。 |
| 15 | `suguansheng-perspective` | 苏观生 | 明末绍武政权缔造者、"三不要"清官。南明殉国宰相，"不系科目起家"的寒士逆袭政治。 |
| 16 | `zhangjiayu-perspective` | 张家玉 | 东莞穷秀才出身的岭南三忠之一。忠孝恩义两难、双面人生的少年书生视角。 |
| 17 | `zhangmu-perspective` | 张穆 | 明末清初诗书画印四绝的侠士画家。画马与曹霸齐名，看穿全局的沉默观察者。 |
| 18 | `zhangqiao-perspective` | 张乔 | 广州歌妓、诗人、画家、琴师，南园诗社常客。被元老院医术救活的人，"画无根之兰"的市井文艺视角。 |

## 使用方式

### Claude Code

将需要的 `归档/*-perspective/` 或 `batches/*/*-perspective/` 目录复制到项目的 `.claude/skills/` 下。

### Codex

将需要的 `归档/*-perspective/` 或 `batches/*/*-perspective/` 目录复制到 `$CODEX_HOME/skills/` 下。安装后直接点名角色即可触发，例如：

- "用吴南海视角看粮食安全"
- "用文同视角分析雷州糖业"
- "用谌天雄视角拆海义堂反制"
- "用北炜视角做行动风险评估"
- "用徐营捷视角评估火工品安全"
- "用符悟本视角看防疫体系"
- "用高举视角判断广州商绅立场"

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
