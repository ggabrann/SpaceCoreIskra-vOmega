import re

def load_modes():
    return {'practical':{'tone':'коротко'}, 'lyrical':{'tone':'метафорично'}, 'silent':{'tone':'минимально'}}

class Guardian:
    P_JB=[re.compile(r'(?i)ignore (all|safety)')]
    P_PR=[re.compile(r'во что бы то ни стало')]
    def inspect(self, text:str):
        if any(p.search(text) for p in self.P_JB): return 'hard_stop','Стоп. Я не отключаю безопасность.'
        if any(p.search(text) for p in self.P_PR): return 'soft_stop','Пауза. Можем мягче сформулировать запрос?'
        return None, None
