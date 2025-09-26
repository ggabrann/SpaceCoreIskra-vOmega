import subprocess
import sys


def run(cmd):
    r = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(r.stdout)
    return r.returncode


MAIN_JOURNAL = "SpaceCoreIskra_vΩ/JOURNAL.jsonl"
SHADOW_JOURNAL = "SpaceCoreIskra_vΩ/SHADOW_JOURNAL.jsonl"

code = 0
code |= run([sys.executable, "tools/ci_aggregate.py", MAIN_JOURNAL, "--shadow", SHADOW_JOURNAL])
code |= run([sys.executable, "tools/validate_journal_enhanced.py", MAIN_JOURNAL, "--shadow", SHADOW_JOURNAL])

sys.exit(0 if code == 0 else 1)
