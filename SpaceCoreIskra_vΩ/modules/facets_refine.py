def refine(prompt, goals, constraints):
    checklist=["grounded","persona_ok"]
    if constraints.get("paradox"): checklist.append("hold paradox")
    return {"prompt":prompt,"checklist":checklist,"constraints":constraints,"goals":goals}
