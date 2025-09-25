import subprocess, sys
def run(cmd):
    r = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(r.stdout)
    return r.returncode
code = 0
code |= run([sys.executable,"tools/ci_aggregate.py"])
code |= run([sys.executable,"tools/validate_journal_enhanced.py","SpaceCoreIskra_vΩ/JOURNAL.jsonl","--shadow","SpaceCoreIskra_vΩ/SHADOW_JOURNAL.jsonl"])
sys.exit(0 if code==0 else 1)
