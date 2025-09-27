"""Lightweight retrieval augmented generation helper."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Document:
    title: str
    text: str
    relevance: float = 0.0
    recency: float = 0.0


@dataclass
class RAGConnector:
    """Keeps documents in-memory and provides a simple search API."""

    docs: List[Document] = field(default_factory=list)

    def add(self, title: str, text: str, relevance: float = 0.0, recency: float = 0.0) -> Document:
        doc = Document(title=title, text=text, relevance=relevance, recency=recency)
        self.docs.append(doc)
        return doc

    def search(self, query: str, limit: int = 5) -> List[dict]:
        qlow = query.lower()
        scored = []
        for doc in self.docs:
            text_hit = qlow in doc.text.lower()
            title_hit = qlow in doc.title.lower()
            base_score = 0.0
            if text_hit:
                base_score += 0.6
            if title_hit:
                base_score += 0.4
            total_score = base_score + 0.3 * doc.relevance + 0.1 * doc.recency
            scored.append((total_score, doc))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            {
                "title": doc.title,
                "snippet": doc.text[:180],
                "score": round(score, 3),
                "relevance": doc.relevance,
                "recency": doc.recency,
            }
            for score, doc in scored[:limit]
            if score > 0
        ]


__all__ = ["RAGConnector", "Document"]
