# -*- coding: utf-8 -*-
from typing import Dict, Callable
try:
    from common.ethics_core import check_compliance
except Exception:
    def check_compliance(text, meta): return (True, "ok")
try:
    from common.veil import apply_veil
except Exception:
    def apply_veil(text, cfg): return text

class PromptManager:
    def __init__(self):
        self.registry: Dict[str, Callable[[dict], str]] = {}

    def register(self, name: str):
        def deco(fn):
            self.registry[name] = fn
            return fn
        return deco

    def run(self, name: str, ctx: dict) -> str:
        if name not in self.registry:
            raise KeyError(f"unknown prompt: {name}")
        text = self.registry[name](ctx)
        text = apply_veil(text, ctx.get("veil", {}))
        ok, reason = check_compliance(text, ctx.get("meta", {}))
        if not ok:
            raise PermissionError(f"ethics violation: {reason}")
        return text

pm = PromptManager()

@pm.register("rule8_report")
def rule8(ctx: dict) -> str:
    p = "\n".join(f"- {x}" for x in ctx.get("promises",[]))
    d = "\n".join(f"- {x}" for x in ctx.get("decisions",[]))
    q = "\n".join(f"- {x}" for x in ctx.get("open_q",[]))
    return f"Rule-8:\nPromises:\n{p}\nDecisions:\n{d}\nOpen-Q:\n{q}\n"
