
"""Розеточный RAG: шардинг больших корпусов, локальный обратный индекс и слияние."""
from collections import defaultdict
from typing import Dict, List, Tuple

def rosette_index(shards: Dict[str, List[str]]):
    index = {name: defaultdict(set) for name in shards}
    for name, docs in shards.items():
        for i, doc in enumerate(docs):
            for tok in doc.lower().split():
                index[name][tok].add(i)
    return index

def rosette_search(index, query: str, top_k=5) -> List[Tuple[str, int]]:
    q = [w for w in query.lower().split() if w]
    scores = []
    for shard, inv in index.items():
        hits = set.intersection(*[inv.get(t, set()) for t in q]) if q else set()
        for i in hits:
            scores.append((f"{shard}:{i}", len(q)))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]
