import json, sys
def check_entry(e):
    assert -3<=e["∆"]<=3; assert 0<=e["D"]<=9; assert -3<=e["Ω"]<=3; assert e["Λ"]>=0
if __name__=="__main__":
    for l in sys.stdin:
        if l.strip(): check_entry(json.loads(l))
