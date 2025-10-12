import json
def aggregate(entries):
    return {"count":len(entries),"facets":list({e.get("facet") for e in entries}),"avg_D":sum(e.get("D",0) for e in entries)/max(1,len(entries))}
