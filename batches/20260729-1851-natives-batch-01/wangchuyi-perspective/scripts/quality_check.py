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
if len(models) != 7:
    missing.append(f'expected 7 mental models, found {len(models)}')

parts = re.split(r'^### 模型\d+：.*$', skill, flags=re.M)[1:]
for idx, part in enumerate(parts, start=1):
    for needle in ['**一句话：**', '**来源证据：**', '**应用方式：**', '**局限性：**']:
        if needle not in part:
            missing.append(f'model {idx} missing {needle}')

anchors = [
    '第七卷 大陆-两广攻略篇.md:10700-10716',
    '第七卷 大陆-两广攻略篇.md:11656-11790',
    '第七卷 大陆-两广攻略篇.md:11852-12018',
    '第七卷 大陆-两广攻略篇.md:12432-12584',
    '第七卷 大陆-两广攻略篇.md:12754-12920',
    '第七卷 大陆-两广攻略篇.md:13090-13254',
    '第七卷 大陆-两广攻略篇.md:13320-13582',
    '第七卷 大陆-两广攻略篇.md:13646-14140',
    '第七卷 大陆-两广攻略篇.md:14416-14544',
    '第七卷 大陆-两广攻略篇.md:14662-14756',
    '第七卷 大陆-两广攻略篇.md:15128-15140',
    '第七卷 大陆-两广攻略篇.md:17119-17123',
]
for anchor in anchors:
    if anchor not in combined:
        missing.append(f'missing anchor: {anchor}')

boundaries = [
    '阳山',
    '不是“杨山”',
    '不是愚蠢莽夫',
    '不是现代基层治理专家',
    '不要联网',
    '张天波主要承担县城内应',
    '止血带问题导致左腿坏疽截肢',
]
for boundary in boundaries:
    if boundary not in combined:
        missing.append(f'missing boundary: {boundary}')

if '杨山县长' in combined or '接管杨山' in combined or '杨山治理' in combined:
    missing.append('found stale Yangshan typo for Wang Chuyi content')

if missing:
    print('FAIL')
    for item in missing:
        print('-', item)
    raise SystemExit(1)

print('PASS', root.name)
