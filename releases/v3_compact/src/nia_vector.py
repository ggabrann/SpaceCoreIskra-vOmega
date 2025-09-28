import re, math
from collections import Counter
TOK=re.compile(r'[\w\-]+', re.UNICODE)

def tok(t): return [x.lower() for x in TOK.findall(t)]
class TfIdf:
    def __init__(self): self.docs=[]; self.df=Counter(); self.N=0
    def add(self,id,text): tf=Counter(tok(text)); self.docs.append((id,tf)); [self.df.__setitem__(k,self.df.get(k,0)+1) for k in tf]; self.N+=1
    def idf(self,t): d=self.df.get(t,0); return 0 if d==0 else math.log(1+self.N/d)
    def vec(self,tf): return {t:(1+math.log(v))*self.idf(t) for t,v in tf.items() if v>0}
