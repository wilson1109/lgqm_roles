#!/usr/bin/env python3
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
required = [
    "SKILL.md",
    "references/research/01-writings.md",
    "references/research/02-conversations.md",
    "references/research/03-expression-dna.md",
    "references/research/04-external-views.md",
    "references/research/05-decisions.md",
    "references/research/06-timeline.md",
    "references/sources/SOURCE_INDEX.md",
]

problems = []
for rel in required:
    path = root / rel
    if not path.exists() or path.stat().st_size < 800:
        problems.append(f"missing or undersized: {rel}")

skill_path = root / "SKILL.md"
text = skill_path.read_text(encoding="utf-8") if skill_path.exists() else ""
needles = [
    "角色扮演规则（最重要）",
    "回答工作流（Agentic Protocol）",
    "身份卡",
    "核心心智模型",
    "决策启发式",
    "表达 DNA",
    "人物时间线",
    "价值观、反模式与内部张力",
    "常见错误",
    "诚实边界",
    "来源附录",
    "Smoke Prompts",
    "证据分级纪律",
    "原文明示",
    "可证推断",
    "未知",
    "广东人",
    "南直人",
    "汪兆铭",
    "学艺不精",
    "兆记只是账簿账户名",
    "无上下文的“王先生”",
    "刑名师爷",
    "钱粮",
    "代理县库",
    "座谈会",
]
problems += [f"SKILL.md missing {needle}" for needle in needles if needle not in text]

frontmatter = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.S)
if not frontmatter:
    problems.append("missing YAML frontmatter")
else:
    block = frontmatter.group(1)
    if "name: wangzhaomin-perspective" not in block:
        problems.append("wrong skill name")
    description_match = re.search(r"^description:\s*(.+)$", block, flags=re.M)
    if not description_match:
        problems.append("missing one-line description")
    elif len(description_match.group(1)) > 1024:
        problems.append("description exceeds 1024 characters")

model_count = len(re.findall(r"^### 模型\d+：", text, flags=re.M))
if model_count != 7:
    problems.append(f"expected 7 mental models, found {model_count}")

try:
    heuristic_section = text.split("## 决策启发式", 1)[1].split("\n---", 1)[0]
except IndexError:
    heuristic_section = ""
heuristic_count = len(re.findall(r"^\d+\. \*\*", heuristic_section, flags=re.M))
if heuristic_count != 10:
    problems.append(f"expected 10 decision heuristics, found {heuristic_count}")

try:
    anchor_section = text.split("### 25 个核心证据锚点", 1)[1].split("### 内部研究文件", 1)[0]
except IndexError:
    anchor_section = ""
anchor_count = len(re.findall(r"^\|\s*\d+\s*\|", anchor_section, flags=re.M))
if anchor_count != 25:
    problems.append(f"expected 25 evidence anchors, found {anchor_count}")

source_index_path = root / "references/sources/SOURCE_INDEX.md"
source_index = source_index_path.read_text(encoding="utf-8") if source_index_path.exists() else ""
for anchor in [
    "第二卷 新世界.md:3601-3629",
    "第二卷 新世界.md:12125-12173",
    "第三卷 新社会.md:11035-11105",
    "第三卷 新社会.md:26036-26096",
    "第三卷 新社会.md:26322-26358",
    "第三卷 新社会.md:28996-29024",
    "第三卷 新社会.md:29026-29096",
    "第四卷 新澳洲.md:10427-10449",
    "第六卷.md:4067-4125",
    "第七卷 大陆-广州治理篇.md:20163-20169",
    "不使用《临高启明全本.md》与备份文件建立新证据",
    "“兆记”只作账户名",
    "无上下文的“王先生”",
]:
    if anchor not in source_index:
        problems.append(f"SOURCE_INDEX.md missing {anchor}")

if problems:
    print("FAIL")
    for problem in problems:
        print("-", problem)
    raise SystemExit(1)

print("PASS", root.name)
print(f"models={model_count} heuristics={heuristic_count} anchors={anchor_count}")
