# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Persona:
    name: str
    tone: str
    rituals: List[str]
    symbols: List[str]

def load_personas(config: Dict)->Dict[str, Persona]:
    out={}
    for p in config.get("personas",[]):
        out[p["name"]] = Persona(
            name=p["name"],
            tone=p.get("tone","plain"),
            rituals=p.get("rituals",[]),
            symbols=p.get("symbols",[])
        )
    return out
