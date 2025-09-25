class ConceptSet:
    def __init__(self, items): self.items=set(items or [])
    def distance(self, other:"ConceptSet")->float:
        u=len(self.items|other.items); i=len(self.items&other.items)
        return 0.0 if u==0 else 1 - i/u

class PersonaSpec:
    def __init__(self, name:str, concepts:list, traits:dict|None=None):
        self.name=name; self.concepts=ConceptSet(concepts); self.traits=traits or {}
