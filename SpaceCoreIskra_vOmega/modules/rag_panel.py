class RAGPanel:
    def __init__(self): self.docs=[]
    def add(self,title,text): self.docs.append({"title":title,"text":text})
    def search(self,q):
        ql=q.lower()
        return [d for d in self.docs if ql in d["text"].lower() or ql in d["title"].lower()]
