PRESETS = {
    "коротко": {"temp": 0.5, "top_p": 0.7},
    "подробно": {"temp": 0.9, "top_p": 0.95},
    "инсайт": {"temp": 0.7, "top_p": 0.85},
}


def route(name: str, overrides: dict = None) -> dict:
    preset = dict(PRESETS.get(name, {}))
    if overrides:
        preset.update(overrides)
    return preset


def list_presets() -> list[str]:
    return list(PRESETS.keys())
