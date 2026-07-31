#!/usr/bin/env python3
from pathlib import Path
import re
import sys

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

fm = re.match(r'^---\n(.*?)\n---\n', skill, re.S)
if not fm:
    missing.append('SKILL.md missing YAML frontmatter')
else:
    keys = []
    for line in fm.group(1).splitlines():
        if line and not line.startswith(' ') and ':' in line:
            keys.append(line.split(':', 1)[0])
    if keys != ['name', 'description']:
        missing.append(f'frontmatter keys should be name, description only: {keys}')

sections = [
    '角色扮演规则',
    '语料契约（Corpus Contract）',
    '回答工作流（Agentic Protocol）',
    '身份卡',
    '核心心智模型（Mental Models）',
    '决策启发式',
    '表达 DNA',
    '时间线',
    '价值观与内部张力',
    'Honest Boundaries',
    'Evidence Anchors',
    '来源附录',
    'Common Mistakes',
    'Smoke Prompts',
]
for section in sections:
    if section not in skill:
        missing.append(f'SKILL.md missing section: {section}')

models = re.findall(r'^### 模型\d+：', skill, re.M)
if len(models) != 6:
    missing.append(f'expected 6 mental models, found {len(models)}')

parts = re.split(r'^### 模型\d+：.*$', skill, flags=re.M)[1:]
for idx, part in enumerate(parts, start=1):
    for needle in ['**一句话：**', '**来源证据：**', '**应用方式：**', '**局限性：**']:
        if needle not in part:
            missing.append(f'model {idx} missing {needle}')

anchors = [
    '第二卷 新世界.md:3084-3090',
    '第二卷 新世界.md:3473-3498',
    '第二卷 新世界.md:4037-4085',
    '第二卷 新世界.md:4215',
    '第二卷 新世界.md:7146-7176',
    '第二卷 新世界.md:7448-7452',
    '第二卷 新世界.md:7572-7588',
    '第二卷 新世界.md:7654',
    '第二卷 新世界.md:15326-15340',
    '第二卷 新世界.md:15346-15370',
    '第二卷 新世界.md:15394-15457',
    '第二卷 新世界.md:15491-15537',
    '第三卷 新社会.md:18149-18155',
    '第三卷 新社会.md:25198-25242',
]
combined = skill + '\n' + source
for anchor in anchors:
    if anchor not in combined:
        missing.append(f'missing anchor: {anchor}')

boundaries = [
    '不是现代廉政英雄',
    '不是成熟干部',
    '不能把后期能力倒灌回早期场景',
    '马棚',
    '不使用网络',
]
for boundary in boundaries:
    if boundary not in combined:
        missing.append(f'missing boundary: {boundary}')

if '现代廉政英雄。拒贿是饭碗纪律' not in skill:
    missing.append('missing anti-hero clarification for refusal of bribes')

if missing:
    print('FAIL')
    for item in missing:
        print('-', item)
    raise SystemExit(1)

print('PASS', root.name)
