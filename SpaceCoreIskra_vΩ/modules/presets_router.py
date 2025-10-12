"""Routing layer for generation presets.

The legacy implementation stored presets in a plain dictionary without any
validation or guardrails.  Downstream tools (including the Iskra Nexus router)
need richer metadata so that they can balance creativity, safety and latency
requirements.  The router below exposes a small, declarative API that keeps the
default presets immutable while allowing projects to register custom variants at
runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Mapping


@dataclass(frozen=True, slots=True)
class Preset:
    """Configuration bundle for a generation preset.

    Attributes
    ----------
    name:
        Human readable identifier used when routing the request.
    parameters:
        Low-level model parameters (temperature, top_p, etc.).
    description:
        Optional summary that can be displayed in UIs.
    metrics:
        Declarative hints about how the preset impacts ∆/D/Ω/Λ metrics.  The
        router does not interpret the numbers beyond keeping them available for
        downstream policy checks.
    """

    name: str
    parameters: Mapping[str, Any]
    description: str = ""
    metrics: Mapping[str, float] = field(default_factory=dict)

    def as_payload(self) -> Dict[str, Any]:
        """Return a serialisable representation of the preset."""

        return {
            "name": self.name,
            "parameters": dict(self.parameters),
            "description": self.description,
            "metrics": dict(self.metrics),
        }


class PresetRouter:
    """Manage preset definitions and resolve them by name."""

    def __init__(self, presets: Iterable[Preset] | None = None) -> None:
        self._presets: Dict[str, Preset] = {}
        for preset in presets or ():
            self.register(preset)

    def register(self, preset: Preset) -> None:
        """Register or replace a preset definition."""

        if not preset.name:
            raise ValueError("preset name must be a non-empty string")
        self._presets[preset.name] = preset

    def resolve(self, name: str | None, *, fallback: str = "balanced") -> Preset:
        """Return the preset associated with *name* or a fallback value.

        Parameters
        ----------
        name:
            Requested preset identifier.  ``None`` indicates the caller does not
            care which preset is used.
        fallback:
            Name of the preset returned when *name* is unknown.  This keeps the
            routing deterministic even when callers send stale preset names.
        """

        if name and name in self._presets:
            return self._presets[name]

        try:
            return self._presets[fallback]
        except KeyError as exc:  # pragma: no cover - only triggered by misuse
            raise KeyError(f"unknown preset '{name}' and fallback '{fallback}'") from exc

    def as_dict(self) -> Dict[str, Dict[str, Any]]:
        """Return all registered presets as a serialisable mapping."""

        return {name: preset.as_payload() for name, preset in self._presets.items()}


DEFAULT_PRESETS = (
    Preset(
        name="balanced",
        parameters={"temperature": 0.6, "top_p": 0.9, "max_tokens": 1024},
        description="Стандартный режим. Поддерживает стабильный баланс ∆/D/Ω/Λ.",
        metrics={"∆": 0.0, "D": 0.0, "Ω": 0.0, "Λ": 0.0},
    ),
    Preset(
        name="коротко",
        parameters={"temperature": 0.3, "top_p": 0.6, "max_tokens": 256},
        description="Сжатые ответы с минимальными отклонениями ∆.",
        metrics={"∆": -0.3, "D": -0.1},
    ),
    Preset(
        name="подробно",
        parameters={"temperature": 0.85, "top_p": 0.95, "max_tokens": 2048},
        description="Развёрнутые объяснения для глубокой фасетной проработки.",
        metrics={"∆": 0.4, "Ω": 0.2},
    ),
)

ROUTER = PresetRouter(DEFAULT_PRESETS)


def route(name: str | None, *, fallback: str = "balanced") -> Dict[str, Any]:
    """Public helper mirroring the legacy function signature."""

    preset = ROUTER.resolve(name, fallback=fallback)
    return preset.as_payload()["parameters"]

