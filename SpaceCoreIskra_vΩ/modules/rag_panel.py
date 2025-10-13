"""Retrieval augmented generation helpers."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Callable, Iterable, List, Mapping, MutableSequence

from common.ethics_core import is_allowed
from .veil import check as veil_check


def _normalise_keywords(keywords: Iterable[str]) -> frozenset[str]:
    return frozenset(keyword.strip().lower() for keyword in keywords if keyword.strip())


@dataclass(slots=True)
class Document:
    """Container for retrieved artefacts."""

    title: str
    text: str
    keywords: frozenset[str] = field(default_factory=frozenset)
    metadata: Mapping[str, str] = field(default_factory=dict)
    source: str = "local"
    score: float = 0.0


Connector = Callable[[str], Iterable[Document | Mapping[str, str]]]


class RAGPanel:
    """Collect documents and provide ranked retrieval results."""

    def __init__(self) -> None:
        self._documents: MutableSequence[Document] = []
        self._connectors: list[Connector] = []

    def add_document(
        self,
        title: str,
        text: str,
        *,
        keywords: Iterable[str] | None = None,
        metadata: Mapping[str, str] | None = None,
        source: str = "local",
    ) -> Document:
        if not title:
            raise ValueError("document title must be provided")
        if not text or not text.strip():
            raise ValueError("document text must be non-empty")
        if not veil_check(text):
            raise ValueError("document rejected by veil policy")
        if not is_allowed(text):
            raise ValueError("document rejected by ethics policy")

        document = Document(
            title=title,
            text=text.strip(),
            keywords=_normalise_keywords(keywords or []),
            metadata=dict(metadata or {}),
            source=source,
        )
        self._documents.append(document)
        return document

    def register_connector(self, connector: Connector) -> None:
        self._connectors.append(connector)

    def _score(self, document: Document, query_terms: frozenset[str]) -> float:
        haystack = document.text.lower()
        base_score = sum(haystack.count(term) for term in query_terms)
        keyword_bonus = len(document.keywords & query_terms) * 2
        return float(base_score + keyword_bonus)

    def _coerce_document(self, payload: Document | Mapping[str, str], *, source: str) -> Document:
        if isinstance(payload, Document):
            return replace(payload, source=payload.source or source)

        title = str(payload.get("title", ""))
        text = str(payload.get("text", "")).strip()
        raw_keywords = payload.get("keywords", [])
        if isinstance(raw_keywords, str):
            keywords = [raw_keywords]
        else:
            keywords = raw_keywords
        metadata = payload.get("metadata", {})
        if not isinstance(metadata, Mapping):
            raise ValueError("document metadata must be a mapping")
        return Document(
            title=title,
            text=text,
            keywords=_normalise_keywords(keywords),
            metadata=dict(metadata),
            source=source,
        )

    def search(
        self,
        query: str,
        *,
        limit: int = 5,
        keywords: Iterable[str] | None = None,
    ) -> List[Document]:
        query_terms = _normalise_keywords(query.split()) | _normalise_keywords(keywords or [])
        if not query_terms:
            query_terms = _normalise_keywords([query])

        candidates: list[Document] = []
        seen: set[tuple[str, str]] = set()

        def add_candidate(doc: Document) -> None:
            key = (doc.title, doc.text)
            if key in seen:
                return
            seen.add(key)
            score = self._score(doc, query_terms)
            if score > 0:
                candidates.append(replace(doc, score=score))

        for document in self._documents:
            add_candidate(document)

        for connector in self._connectors:
            for payload in connector(query):
                external = self._coerce_document(payload, source=getattr(connector, "__name__", "external"))
                if veil_check(external.text) and is_allowed(external.text):
                    add_candidate(external)

        candidates.sort(key=lambda doc: doc.score, reverse=True)
        return candidates[:limit]

