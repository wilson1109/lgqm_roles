#!/usr/bin/env python3
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
required = [
    'SKILL.md',
    'references/research/01-writings.md',
    'references/research/02-conversations.md',
    'references/research/03-expression-dna.md',
    'references/research/04-external-views.md',
    'references/research/05-decisions.md',
    'references/research/06-timeline.md',
    'references/sources/SOURCE_INDEX.md',
]

missing = []
for rel in required:
    p = root / rel
    if not p.exists() or p.stat().st_size < 500:
        missing.append(f'missing or too small: {rel}')

skill = (root / 'SKILL.md').read_text(encoding='utf-8')
source = (root / 'references/sources/SOURCE_INDEX.md').read_text(encoding='utf-8')
combined = skill + '\n' + source

fm = re.match(r'^---\n(.*?)\n---\n', skill, re.S)
if not fm:
    missing.append('SKILL.md missing YAML frontmatter')
else:
    for key in ['name:', 'description:', 'triggers:']:
        if key not in fm.group(1):
            missing.append(f'frontmatter missing {key}')

sections = [
    '角色扮演规则',
    '语料契约（Corpus Contract）',
    '回答工作流（Agentic Protocol）',
    '身份卡',
    'Evidence Anchors',
    '核心心智模型（Mental Models）',
    '决策启发式',
    '表达 DNA',
    '时间线',
    '关系网络',
    '价值观与内部张力',
    'Honest Boundaries',
    'Common Mistakes',
    'Smoke Prompts',
    '来源附录',
]
for section in sections:
    if section not in skill:
        missing.append(f'SKILL.md missing section: {section}')

models = re.findall(r'^### 模型\d+：', skill, re.M)
if len(models) != 7:
    missing.append(f'expected 7 mental models, found {len(models)}')

parts = re.split(r'^### 模型\d+：.*$', skill, flags=re.M)[1:]
for idx, part in enumerate(parts, start=1):
    for needle in ['**一句话：**', '**来源证据：**', '**应用方式：**', '**局限性：**']:
        if needle not in part:
            missing.append(f'model {idx} missing {needle}')

anchors = [
    '第七卷 大陆-两广攻略篇.md:10680-10762',
    '第七卷 大陆-两广攻略篇.md:11524-11654',
    '第七卷 大陆-两广攻略篇.md:11678-11758',
    '第七卷 大陆-两广攻略篇.md:14682-14762',
    '第七卷 大陆-两广攻略篇.md:14780-14816',
    '第七卷 大陆-两广攻略篇.md:15958-15976',
    '第七卷 大陆-两广攻略篇.md:16062-16158',
    '第七卷 大陆-两广攻略篇.md:16158-16168',
    '第七卷 大陆-两广攻略篇.md:16960-17010',
]
for anchor in anchors:
    if anchor not in combined:
        missing.append(f'missing anchor: {anchor}')

boundaries = [
    '不是清官',
    '不是纯恶吏',
    '不是坚定澳宋干部',
    '阳山',
    '不是「杨山」',
    '不使用网络',
]
for boundary in boundaries:
    if boundary not in combined:
        missing.append(f'missing boundary: {boundary}')

bad_yangshan_lines = []
for line in combined.splitlines():
    if '杨山' not in line:
        continue
    if any(marker in line for marker in ['不是', '误写', '校正', '错误', '旧文件', '地名统一', '写成']):
        continue
    bad_yangshan_lines.append(line)
if bad_yangshan_lines:
    missing.append('unexpected 杨山 typo outside explicit correction note')

if missing:
    print('FAIL')
    for item in missing:
        print('-', item)
    raise SystemExit(1)

print('PASS', root.name)
