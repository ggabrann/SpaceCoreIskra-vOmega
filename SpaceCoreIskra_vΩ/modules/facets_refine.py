def refine(prompt: str, goals: list, constraints: dict):
    """Возвращает структуру с чек-листами, предупреждениями и сигналами."""
    checklist = ["grounded", "persona_ok", "cite_sources"]
    warnings = []

    if constraints.get("paradox"):
        checklist.append("hold_paradox")
    if constraints.get("tone") == "creative":
        checklist.append("allow_metaphors")
    if goals and any("risk" in g.lower() for g in goals):
        warnings.append("goal_contains_risk")

    priority = constraints.get("priority", "normal")
    signal = {
        "∆": constraints.get("target_delta", 0),
        "Λ": 2 if priority == "high" else 0,
    }

    return {
        "prompt": prompt,
        "checklist": checklist,
        "constraints": constraints,
        "goals": goals,
        "warnings": warnings,
        "signal": signal,
    }
