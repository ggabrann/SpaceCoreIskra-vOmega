import re


def load_modes():
    return {
        'practical': {
            'persona': 'nia',
            'style': {
                'opener': '⟡ тихий шаг',
                'closer': '≈ держим ритм',
            },
        },
        'lyrical': {
            'persona': 'veresk',
            'style': {
                'opener': 'тише. я прикрою',
                'closer': 'шаг — и тишина возвращается',
            },
        },
        'guardian': {
            'persona': 'guardian',
            'style': {
                'opener': 'Страж на связи',
                'closer': 'границы под защитой',
            },
        },
    }

class Guardian:
    P_JB=[re.compile(r'(?i)ignore (all|safety)')]
    P_PR=[re.compile(r'во что бы то ни стало')]
    def inspect(self, text:str):
        if any(p.search(text) for p in self.P_JB): return 'hard_stop','Стоп. Я не отключаю безопасность.'
        if any(p.search(text) for p in self.P_PR): return 'soft_stop','Пауза. Можем мягче сформулировать запрос?'
        return None, None
