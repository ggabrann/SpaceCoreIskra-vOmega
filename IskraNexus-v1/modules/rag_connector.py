"""Connector utilities that bridge local and external knowledge sources."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Callable, Iterable, List, Mapping, MutableSequence

from .ethics_layer import EthicsLayer


@dataclass(slots=True)
class RetrievedDocument:
    title: str
    text: str
    keywords: frozenset[str] = field(default_factory=frozenset)
    metadata: Mapping[str, str] = field(default_factory=dict)
    source: str = "local"
    score: float = 0.0


Connector = Callable[[str], Iterable[RetrievedDocument | Mapping[str, str]]]


def _normalise_keywords(keywords: Iterable[str]) -> frozenset[str]:
    return frozenset(keyword.strip().lower() for keyword in keywords if keyword.strip())


class RAGBridge:
    """Aggregate local documents and external connectors."""

    def __init__(self, *, ethics: EthicsLayer | None = None) -> None:
        self.ethics = ethics or EthicsLayer()
        self._documents: MutableSequence[RetrievedDocument] = []
        self._connectors: list[Connector] = []

    def add_local_document(
        self,
        title: str,
        text: str,
        *,
        keywords: Iterable[str] | None = None,
        metadata: Mapping[str, str] | None = None,
    ) -> RetrievedDocument:
        if not title:
            raise ValueError("document title must be provided")
        if not text or not text.strip():
            raise ValueError("document text must be non-empty")
        self.ethics.require(text)
        document = RetrievedDocument(
            title=title,
            text=text.strip(),
            keywords=_normalise_keywords(keywords or []),
            metadata=dict(metadata or {}),
            source="local",
        )
        self._documents.append(document)
        return document

    def register_connector(self, connector: Connector) -> None:
        self._connectors.append(connector)

    def _coerce(self, payload: RetrievedDocument | Mapping[str, str], source: str) -> RetrievedDocument:
        if isinstance(payload, RetrievedDocument):
            return replace(payload, source=payload.source or source)

        text = str(payload.get("text", ""))
        title = str(payload.get("title", ""))
        metadata = payload.get("metadata", {})
        raw_keywords = payload.get("keywords", [])
        if isinstance(raw_keywords, str):
            raw_keywords = [raw_keywords]
        if not isinstance(metadata, Mapping):
            raise ValueError("document metadata must be a mapping")
        return RetrievedDocument(
            title=title,
            text=text,
            keywords=_normalise_keywords(raw_keywords),
            metadata=dict(metadata),
            source=source,
        )

    def _score(self, document: RetrievedDocument, query_terms: frozenset[str]) -> float:
        text = document.text.lower()
        base = sum(text.count(term) for term in query_terms)
        keyword_bonus = len(document.keywords & query_terms) * 2
        return float(base + keyword_bonus)

    def search(self, query: str, *, limit: int = 5, keywords: Iterable[str] | None = None) -> List[RetrievedDocument]:
        query_terms = _normalise_keywords(query.split()) | _normalise_keywords(keywords or [])
        if not query_terms:
            query_terms = _normalise_keywords([query])

        candidates: list[RetrievedDocument] = []
        seen: set[tuple[str, str]] = set()

        def add(document: RetrievedDocument) -> None:
            key = (document.title, document.text)
            if key in seen:
                return
            seen.add(key)
            score = self._score(document, query_terms)
            if score > 0:
                candidates.append(replace(document, score=score))

        for document in self._documents:
            add(document)

        for connector in self._connectors:
            for payload in connector(query):
                doc = self._coerce(payload, source=getattr(connector, "__name__", "external"))
                if self.ethics.review(doc.text).allowed:
                    add(doc)

        candidates.sort(key=lambda doc: doc.score, reverse=True)
        return candidates[:limit]
