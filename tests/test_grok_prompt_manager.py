import pytest

from GrokCoreIskra_vΓ.modules.prompt_manager import PromptManager


def test_prompt_includes_metrics_values():
    manager = PromptManager()
    manager.add_prompt("status", "System ready")

    result = manager.get_prompt("status", {"∆": 1.23, "D": "stable"})

    assert "System ready" in result
    assert "∆=1.23" in result
    assert "D=stable" in result


def test_prompt_handles_missing_metrics():
    manager = PromptManager()
    manager.add_prompt("status", "System ready")

    result = manager.get_prompt("status", {"∆": None})

    assert "∆=N/A" in result
    assert "D=N/A" in result
