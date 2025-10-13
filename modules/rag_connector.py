# -*- coding: utf-8 -*-
import os, math, re
from collections import Counter
def _tokenize(t:str): return re.findall(r"[A-Za-zА-Яа-я0-9_]+", t.lower())

class LocalRAG:
    def __init__(self, roots):
        self.docs=[]; self.df=Counter(); self.N=0
        for r in roots:
            for root,_,files in os.walk(r):
                for f in files:
                    if f.endswith((".md",".txt",".json",".yml",".yaml")):
                        p=os.path.join(root,f)
                        try: txt=open(p,"r",encoding="utf-8").read()
                        except: continue
                        toks=set(_tokenize(txt))
                        self.docs.append((p, txt))
                        for t in toks: self.df[t]+=1
                        self.N+=1
    def search(self, query:str, k=5):
        q=_tokenize(query); scores=[]
        for p,txt in self.docs:
            toks=_tokenize(txt); tf=Counter(toks)
            s=0.0
            for t in q:
                idf = math.log(1 + (self.N)/(1+self.df[t]))
                s += (tf[t]/(1+len(toks))) * idf
            scores.append((s,p,txt[:500]))
        scores.sort(reverse=True)
        return scores[:k]
