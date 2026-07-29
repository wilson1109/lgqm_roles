#!/usr/bin/env python3
from pathlib import Path
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
missing = [rel for rel in required if not (root / rel).exists() or (root / rel).stat().st_size < 300]
text = (root / 'SKILL.md').read_text(encoding='utf-8')
for needle in ['江山', '对外情报局', 'Mental Models', 'Evidence Anchors', 'Honest Boundaries']:
    if needle not in text:
        missing.append(f'SKILL.md missing {needle}')
if 'name: jiangshan-perspective' not in text:
    missing.append('SKILL.md has wrong frontmatter name')
if missing:
    print('FAIL')
    for item in missing:
        print('-', item)
    raise SystemExit(1)
print('PASS', root.name)
