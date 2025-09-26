class PromptManager:
    def __init__(self): self.prompts={}
    def add_prompt(self,name,text): self.prompts[name]=text
    def get_prompt(self,name,metrics):
        p=self.prompts.get(name,"")
        delta=metrics.get("∆","N/A")
        distance=metrics.get("D","N/A")
        return f"{p} [Metrics: ∆={delta}, D={distance}]"
