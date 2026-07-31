#!/usr/bin/env python3
from pathlib import Path

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

missing = []
for rel in required:
    p = root / rel
    if not p.exists():
        missing.append(rel)
    elif p.stat().st_size < 800:
        missing.append(f"{rel} too small")

skill = (root / "SKILL.md").read_text(encoding="utf-8")
source = (root / "references/sources/SOURCE_INDEX.md").read_text(encoding="utf-8")
research_text = "\n".join((root / rel).read_text(encoding="utf-8") for rel in required if rel.startswith("references/research/"))

skill_needles = [
    "# 李默 · 思维操作系统",
    "角色扮演规则",
    "Agentic Protocol",
    "证据分级纪律",
    "原文明示",
    "他者评价",
    "政保推断",
    "本 skill 推断",
    "核心心智模型",
    "决策启发式",
    "表达 DNA",
    "时间线",
    "诚实边界",
    "来源附录",
    "Smoke Prompts",
    "李默",
    "李荃",
    "李丝雅",
    "李华梅",
    "紫明楼",
    "总务长",
    "省港总医院",
    "疑点无证据",
    "三级监控",
    "主动间谍",
    "吴南海情妇",
    "现代独立宣言",
]
missing += [f"SKILL.md missing {needle}" for needle in skill_needles if needle not in skill]

if skill.count("### 模型") < 7:
    missing.append("SKILL.md has fewer than 7 mental models")
if skill.count("| 第") < 15:
    missing.append("SKILL.md has fewer than 15 evidence anchors")

source_needles = [
    "本轮口径",
    "异名与边界",
    "核心锚点",
    "人物库校验",
    "来源纪律",
    "疑点无证据",
    "调岗降风险",
    "不得写成坐实主动间谍",
]
missing += [f"SOURCE_INDEX.md missing {needle}" for needle in source_needles if needle not in source]
if source.count("| 第") < 15:
    missing.append("SOURCE_INDEX.md has fewer than 15 source anchors")

research_needles = [
    "本轮按崇祯/陈同范式重修",
    "李荃",
    "李丝雅",
    "政保",
    "庶务",
    "原文",
]
missing += [f"research missing {needle}" for needle in research_needles if needle not in research_text]

banned_artifacts = [
    "practical concern",
    "TODO",
]
missing += [f"artifact remains: {bad}" for bad in banned_artifacts if bad in skill + source + research_text]

if missing:
    print("FAIL")
    for item in missing:
        print("-", item)
    raise SystemExit(1)

print("PASS", root.name)
