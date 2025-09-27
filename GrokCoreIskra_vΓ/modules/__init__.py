"""Expose the GrokCore module primitives."""
from __future__ import annotations

from .prompt_manager import PromptManager
from .rag_connector import RAGConnector
from .ethics_layer import EthicsLayer
from .persona_module import PersonaRegistry
from .self_journal import SelfJournal

__all__ = [
    "PromptManager",
    "RAGConnector",
    "EthicsLayer",
    "PersonaRegistry",
    "SelfJournal",
]
