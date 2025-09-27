import json, sys
def validate(line):
    e = json.loads(line)
    assert -3 <= e["∆"] <= 3
    assert 0 <= e["D"] <= 9
    assert -3 <= e["Ω"] <= 3
    assert e["Λ"] >= 0
for l in sys.stdin:
    if l.strip():
        try: validate(l)
        except Exception as ex: print("ERR", ex)
