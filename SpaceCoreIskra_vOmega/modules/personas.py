class Persona:
    def __init__(self,name,concepts):
        self.name=name; self.concepts=set(concepts)
    def distance(self,other):
        union=self.concepts|other.concepts
        return 0.0 if not union else 1.0 - len(self.concepts & other.concepts)/len(union)
