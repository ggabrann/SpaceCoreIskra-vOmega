"""Lightweight retrieval layer with pluggable providers."""
from __future__ import annotations

from typing import List, Dict


class OracleRAG:
    def __init__(self) -> None:
        self._local_docs: List[Dict[str, str]] = []

    def register_document(self, title: str, text: str) -> None:
        self._local_docs.append({"title": title, "text": text})

    def search(self, query: str, limit: int = 3) -> List[Dict[str, str]]:
        query_low = query.lower()
        hits: List[Dict[str, str]] = []
        for doc in self._local_docs:
            if query_low in doc["title"].lower() or query_low in doc["text"].lower():
                hits.append(doc)
        return hits[:limit]
