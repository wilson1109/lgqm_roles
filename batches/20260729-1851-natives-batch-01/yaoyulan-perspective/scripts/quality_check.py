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
missing = []
for rel in required:
    p = root / rel
    if not p.exists() or p.stat().st_size < 200:
        missing.append(rel)
text = (root / 'SKILL.md').read_text(encoding='utf-8')
needles = [
    'triggers:',
    '思维操作系统',
    '角色扮演规则',
    '语料契约',
    '回答工作流',
    '核心心智模型',
    '决策启发式',
    '表达 DNA',
    '人物时间线',
    '价值观与反模式',
    '智识谱系',
    '诚实边界',
    '附录：调研来源',
    'Evidence Anchors',
]
missing += [f'SKILL.md missing {n}' for n in needles if n not in text]
facts = [
    '苏菀',
    '隐干',
    '非契约奴',
    '豆腐西施',
    '死鱼脸',
    '二队队长',
    '佛山姚家',
    '柯云',
    '杨草',
    '长款',
]
missing += [f'SKILL.md missing corrected fact {n}' for n in facts if n not in text]
reference_needles = {
    'references/research/01-writings.md': [
        '安全账压过热血',
        '从被监视者变成监视者',
        '「隐干」不是升迁，是安置',
    ],
    'references/research/02-conversations.md': ['两人小队队长', '噤声手势'],
    'references/research/03-expression-dna.md': ['佛山姚家', '苏菀', '隐干'],
    'references/research/04-external-views.md': ['死鱼脸', '敌意视角'],
    'references/research/05-decisions.md': ['不做恶人', '两条线分开走'],
    'references/research/06-timeline.md': ['非契约奴', '712专案组二队队长'],
    'references/sources/SOURCE_INDEX.md': ['苏菀，不是「苏莞」', '已退役的错误锚点'],
}
for rel, terms in reference_needles.items():
    body = (root / rel).read_text(encoding='utf-8')
    missing += [f'{rel} missing {term}' for term in terms if term not in body]
# 退役错字「苏莞」只允许出现在同时给出正确写法「苏菀」的修正语句里
for rel in required:
    for lineno, line in enumerate(
        (root / rel).read_text(encoding='utf-8').splitlines(), start=1
    ):
        if '苏莞' in line and '苏菀' not in line:
            missing.append(f'{rel}:{lineno} uses retired token 苏莞 without correction')
if missing:
    print('FAIL')
    for item in missing:
        print('-', item)
    raise SystemExit(1)
print('PASS', root.name)
