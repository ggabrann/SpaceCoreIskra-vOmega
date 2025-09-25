import json, os
class PromptsRepo:
    def __init__(self, path="prompts.json"):
        self.path = path; self.prompts = {}
        if os.path.exists(self.path):
            try: self.prompts = json.load(open(self.path,"r",encoding="utf-8"))
            except Exception: self.prompts = {}
    def add(self, name, prompt, meta):
        self.prompts[name] = {"text": prompt, "meta": meta}; self.save()
    def save(self):
        json.dump(self.prompts, open(self.path,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    def get(self, name): return self.prompts.get(name)
