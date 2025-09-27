"""Simplified retrieval connector for GrokCoreIskra vΓ."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Document:
    title: str
    text: str
    score: float = 0.0


@dataclass
class RAGConnector:
    documents: List[Document] = field(default_factory=list)

    def add(self, title: str, text: str, score: float = 0.5) -> Document:
        doc = Document(title=title, text=text, score=score)
        self.documents.append(doc)
        return doc

    def search(self, query: str, *, limit: int = 3) -> List[dict]:
        q = query.lower()
        scored = []
        for doc in self.documents:
            match = 0.3 if q in doc.text.lower() else 0.0
            match += 0.2 if q in doc.title.lower() else 0.0
            scored.append((doc.score + match, doc))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            {"title": doc.title, "snippet": doc.text[:120], "score": round(score, 3)}
            for score, doc in scored[:limit]
        ]


__all__ = ["Document", "RAGConnector"]
