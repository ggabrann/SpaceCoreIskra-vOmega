from datetime import datetime, timedelta
from collections import Counter
import re

def summarize(texts):
    toks = re.findall(r'[\wЁёА-Яа-я]+',' '.join(texts).lower()); c=Counter(toks)
    return [w for w,_ in c.most_common(50)]

def srs_dates(start, steps=(3,7,21,45,90)):
    base=datetime.utcnow(); return [(base+timedelta(days=d)).isoformat() for d in steps]
