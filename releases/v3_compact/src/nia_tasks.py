import json, os, uuid
class Tasks:
    def __init__(self,path='tasks.json'):
        self.p=path; self.t=json.loads(open(path,'r',encoding='utf-8').read()) if os.path.exists(path) else []
    def add(self,title,due=None):
        x={'id':str(uuid.uuid4()),'title':title,'due':due,'done':False}; self.t.append(x); open(self.p,'w',encoding='utf-8').write(json.dumps(self.t,ensure_ascii=False,indent=2)); return x
