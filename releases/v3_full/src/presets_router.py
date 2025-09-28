
"""Inference planning (o1-style): выбирает глубину размышления по признакам сложности"""
from dataclasses import dataclass

TRIGGERS = ("доказательство", "алгоритм", "архитектура", "документ", "исследование", "план релиза")

@dataclass
class PlanPreset:
    thought_time: int = 3
    beam: int = 1
    steps: int = 1

def route(task: str) -> dict:
    hard = any(k in task.lower() for k in TRIGGERS)
    return PlanPreset(thought_time=12, beam=3, steps=3).__dict__ if hard else PlanPreset().__dict__
