#!/usr/bin/env python3
"""validate_catalog.py — 校验角色目录完整性和路由匹配质量。

用法:
    python validate_catalog.py --check   # 校验完整性（triggers 非空、目录结构完整）
    python validate_catalog.py --test    # 运行匹配测试矩阵（30+ 用例）

通过标准:
    --check: 所有角色 triggers 非空、目录结构完整 → exit 0
    --test:  匹配准确率 ≥ 90% → exit 0
"""
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_catalog as bc


# ============ --check: 完整性校验 ============

def check_completeness():
    """校验所有角色 skill 的目录结构和 triggers。"""
    errors = []
    warnings = []
    skills_root, skill_dirs = bc.get_skills_root()

    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        # 1. SKILL.md 存在
        skill_md = skill_dir / 'SKILL.md'
        if not skill_md.exists():
            errors.append(f"[ERROR] {skill_name}: 缺少 SKILL.md")
            continue
        # 2. frontmatter 可解析
        fm = bc.parse_frontmatter(skill_md)
        if not fm:
            errors.append(f"[ERROR] {skill_name}: frontmatter 解析失败")
            continue
        # 3. triggers 非空
        triggers = bc.extract_triggers(fm)
        if not triggers:
            errors.append(f"[ERROR] {skill_name}: triggers 为空")
        # 4. references/research 存在
        research = skill_dir / 'references' / 'research'
        if not research.exists():
            warnings.append(f"[WARNING] {skill_name}: 缺少 references/research/")
        # 5. sources 索引存在
        sources = skill_dir / 'references' / 'sources'
        if not sources.exists():
            warnings.append(f"[WARNING] {skill_name}: 缺少 references/sources/")

    # 6. catalog 与磁盘一致性
    _, all_chars, scan_warnings = bc.scan_all()
    catalog_missing = set(skill_dirs) - {Path(d['path']) for d in all_chars.values()}
    if catalog_missing:
        errors.append(f"[ERROR] catalog 缺失 {len(catalog_missing)} 个角色: {[p.name for p in catalog_missing]}")

    for w in warnings:
        print(w)
    for e in errors:
        print(e)
    print(f"\nCHECK: {len(skill_dirs)} skills, {len(errors)} errors, {len(warnings)} warnings")
    return 0 if not errors else 1


# ============ --test: 匹配测试矩阵 ============

def _match_characters(query, all_chars):
    """模拟路由器的匹配逻辑：返回按置信度排序的角色名列表。"""
    # 领域关键词反向扫描：query 命中哪个领域的关键词，该领域角色加分
    query_domains = set()
    for domain, keywords in bc.DOMAIN_PATTERNS.items():
        if any(kw in query for kw in keywords):
            query_domains.add(domain)
    scores = {}
    for skill_name, data in all_chars.items():
        score = 0
        triggers = data['triggers']
        desc = data['description']
        # 触发词精确匹配
        for t in triggers:
            if t and t in query:
                score += 5 if len(t) >= 2 else 1
        # 角色名匹配（最高权重）
        char_name = data.get('character_name', '')
        if char_name and char_name in query:
            score += 10
        # 领域匹配（query 含领域名 或 领域关键词命中 query）
        for d in data['domains']:
            if d in query:
                score += 2
            if d in query_domains:
                score += 2
        # description 实体匹配（模拟 Claude Code 的 description 触发机制）
        for term in re.findall(r'[一-鿿]{2,5}', query):
            if term in desc:
                score += 3
        if score > 0:
            scores[skill_name] = score
    return sorted(scores, key=lambda k: scores[k], reverse=True)


# 测试用例：(query, 期望匹配的角色名集合, 说明)
TEST_CASES = [
    # --- 精确人物名匹配 ---
    ("用北炜的视角", {'北炜'}, "直接点名"),
    ("萧子山会怎么处理这件事", {'萧子山'}, "直接点名+行为"),
    ("让常师德来说说雷州的事", {'常师德'}, "点名+场景"),
    ("林默天怎么搞防疫", {'林默天'}, "点名+主题"),
    ("钱朵朵出警", {'钱朵朵'}, "点名"),
    ("吴南海看粮食安全", {'吴南海'}, "点名+主题"),
    ("慕敏查案", {'慕敏'}, "点名"),
    ("文德嗣怎么看待贸易", {'文德嗣'}, "点名+主题"),
    # --- 别名/外号匹配 ---
    ("督公怎么看工业化", {'马千瞩'}, "别名"),
    ("杜女王又来了", {'杜雯'}, "外号"),
    ("石翁的谋划", {'王业浩'}, "外号"),
    ("江局怎么看外情局", {'江山'}, "外号"),
    ("崇祯会怎么想", {'崇祯皇帝'}, "皇帝称谓"),
    # --- 领域/地点匹配 ---
    ("写雷州糖厂被围攻", {'文同', '常师德'}, "雷州+糖业"),
    ("广州站的情报业务", {'郭逸'}, "广州站"),
    ("临高教会的传教", {'吴石芒'}, "宗教"),
    ("山东基地难民安置", {'鹿文渊', '黄安德'}, "山东+难民"),
    ("江南丝业生意", {'赵引弓'}, "江南"),
    ("佛山警务", {'慕敏', '钱朵朵'}, "警务"),
    ("芳草地的小元老", {'张允幂', '黄平'}, "教育"),
    ("登莱巡抚的火器", {'孙元化'}, "大明+军事"),
    # --- 事件/情节匹配 ---
    ("女仆案的政治影响", {'程咏昕'}, "事件"),
    ("唐僧计划的执行", {'北炜', '谌天雄'}, "事件"),
    ("发动机行动", {'鹿文渊', '黄安德'}, "事件"),
    ("海义堂的商业战", {'文同'}, "事件"),
    ("临高时报的舆论", {'潘潘'}, "事件"),
    ("两广攻略", {'朱鸣夏', '黄熊', '北炜'}, "事件"),
    # --- 模糊/多义输入 ---
    ("写一场战斗", {'北炜', '朱鸣夏', '黄熊'}, "模糊战斗"),
    ("商业谈判", {'李梅', '郭逸', '张毓'}, "模糊商业"),
    ("防疫怎么搞", {'林默天', '符悟本'}, "模糊防疫"),
    ("宗教渗透", {'张应宸', '吴石芒'}, "模糊宗教"),
    ("政治斗争", {'萧子山', '杜雯', '程咏昕', '明朗'}, "模糊政治"),
    # --- 无匹配输入 ---
    ("帮我写个架空兵器", None, "无匹配，应不误报"),
    ("外星人来到地球", None, "无匹配"),
    ("怎么写代码", None, "无匹配"),
]


def run_tests():
    _, all_chars, _ = bc.scan_all()
    # 角色中文名索引（用于把期望名字映射到 skill）
    name_to_skill = {}
    for skill_name, data in all_chars.items():
        cn = data.get('character_name', '')
        if cn:
            name_to_skill[cn] = skill_name
        # 也匹配 description 中的显式角色名
        for m in re.findall(r'[一-鿿]{2,3}（|^\s*([一-鿿]{2,4})\s*[,，]', data['description']):
            pass

    passed, total = 0, 0
    failures = []
    for query, expected_names, note in TEST_CASES:
        total += 1
        matched = _match_characters(query, all_chars)
        if expected_names is None:
            # 无匹配用例：只要不返回明显错误的强匹配即可（允许低分弱匹配）
            top = matched[:1]
            if top:
                # 检查 top1 是否有强命中（得分 >= 5）
                strong = any(all_chars[s]['triggers'] and any(t in query for t in all_chars[s]['triggers']) for s in top)
                if strong:
                    failures.append((query, note, "无匹配用例却强命中", matched[:3]))
                    continue
            passed += 1
        else:
            # 期望匹配：top-3 内应包含至少一个期望角色
            top3_skills = matched[:3]
            hit = False
            for en in expected_names:
                if en in name_to_skill and name_to_skill[en] in top3_skills:
                    hit = True
                    break
            if hit:
                passed += 1
            else:
                failures.append((query, note, f"期望 {expected_names}", top3_skills))

    print(f"\nTEST: {passed}/{total} passed ({100.0*passed/total:.0f}%)")
    if failures:
        print("\n失败用例：")
        for q, note, expect, got in failures:
            print(f"  [{note}] {q}\n    期望: {expect}\n    实际top3: {got}")
        return 1
    return 0


if __name__ == '__main__':
    if '--test' in sys.argv:
        sys.exit(run_tests())
    else:
        sys.exit(check_completeness())
