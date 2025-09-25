class PromptManager:
    def __init__(self): self.prompts={}
    def add_prompt(self,name,text): self.prompts[name]=text
    def get_prompt(self,name,metrics): 
        p=self.prompts.get(name,""); return f"{p} [Metrics: ∆={metrics.get(∆)}, D={metrics.get(D)}]"
