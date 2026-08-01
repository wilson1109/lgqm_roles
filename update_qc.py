import os, glob

batch_dir = '/Users/gao/Documents/lgqm/batches/20260731-1048-natives-batch-03'

for skill in glob.glob(os.path.join(batch_dir, '*-perspective')):
    skill_basename = os.path.basename(skill)
    qc_content = f"""#!/usr/bin/env python3
import os, sys

def run_check():
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    errors = []
    
    skill_md = os.path.join(skill_dir, 'SKILL.md')
    if not os.path.exists(skill_md):
        errors.append("SKILL.md missing")
    else:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
            if len(content) < 1000:
                errors.append("SKILL.md content too short")
            if "思维操作系统" not in content:
                errors.append("SKILL.md missing '思维操作系统' title")
                
    research_dir = os.path.join(skill_dir, 'references', 'research')
    for i in range(1, 7):
        prefix = f"0{{i}}-"
        found = False
        if os.path.exists(research_dir):
            for f_item in os.listdir(research_dir):
                if f_item.startswith(f"0{{i}}-"):
                    found = True
                    break
        if not found:
            errors.append(f"Research file 0{{i}} missing")
            
    source_index = os.path.join(skill_dir, 'references', 'sources', 'SOURCE_INDEX.md')
    if not os.path.exists(source_index):
        errors.append("SOURCE_INDEX.md missing")
    else:
        with open(source_index, 'r', encoding='utf-8') as f:
            c_str = f.read()
            if "/Users/gao/Library/Mobile Documents/com~apple~CloudDocs/旅顺口写作计划/原著/md" not in c_str:
                errors.append("SOURCE_INDEX.md missing exact novel path")
                
    if errors:
        print("[FAIL] {skill_basename}: " + ", ".join(errors))
        sys.exit(1)
    else:
        print("[PASS] {skill_basename} quality check passed.")
        sys.exit(0)

if __name__ == '__main__':
    run_check()
"""
    qc_path = os.path.join(skill, 'scripts', 'quality_check.py')
    with open(qc_path, 'w', encoding='utf-8') as f:
        f.write(qc_content)
    os.chmod(qc_path, 0o755)

print("Updated quality_check.py scripts.")
