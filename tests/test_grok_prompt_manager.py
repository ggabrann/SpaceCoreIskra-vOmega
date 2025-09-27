import pytest

from GrokCoreIskra_vΓ.modules.prompt_manager import PromptManager


def test_prompt_manager_includes_metrics():
    manager = PromptManager()
    manager.add_prompt("status", "System status report")

    metrics = {"∆": 0.42, "D": 7}
    prompt_text = manager.get_prompt("status", metrics)

    assert "System status report" in prompt_text
    assert "∆=0.42" in prompt_text
    assert "D=7" in prompt_text


def test_prompt_manager_defaults_missing_metrics():
    manager = PromptManager()
    manager.add_prompt("status", "System status report")

    prompt_text = manager.get_prompt("status", {})

    assert "∆=N/A" in prompt_text
    assert "D=N/A" in prompt_text

    prompt_text_none = manager.get_prompt("status", None)
    assert "∆=N/A" in prompt_text_none
    assert "D=N/A" in prompt_text_none

    prompt_text_invalid = manager.get_prompt("status", [])
    assert "∆=N/A" in prompt_text_invalid
    assert "D=N/A" in prompt_text_invalid
