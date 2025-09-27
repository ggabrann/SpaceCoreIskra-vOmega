import json, datetime
def gen(facet,snap,ans,metrics,mirror="shadow-000",modules=None,events=None,marks=None, path="JOURNAL.jsonl"):
    e={"facet":facet,"snapshot":snap,"answer":ans,"∆":metrics.get("∆",0),"D":metrics.get("D",0),"Ω":metrics.get("Ω",0),"Λ":metrics.get("Λ",0),"mirror":mirror,"modules":modules or [],"events":events or {},"marks":marks or [],"timestamp":datetime.datetime.utcnow().isoformat()+"Z"}
    with open(path,"a",encoding="utf-8") as f: f.write(json.dumps(e, ensure_ascii=False)+"\\n")
    return e
