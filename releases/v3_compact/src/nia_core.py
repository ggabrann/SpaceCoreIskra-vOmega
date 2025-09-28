from src.nia_core_ext import Guardian, load_modes
from src.nia_memory import write_short_term

class Nia:
    def __init__(self):
        self.mode='practical'; self.guard=Guardian(); self.modes=load_modes()
    def set_mode(self,m): self.mode=m
    def reply(self,text:str)->str:
        act,msg=self.guard.inspect(text)
        if act: return msg or 'Мягкая пауза. Переформулируем цель.'
        write_short_term(text=text, tags=['input'])
        return 'Давай мягко начнём с дыхания: три цикла. Я рядом.'
