import math
import re
from collections import Counter

TOK = re.compile(r'[\w\-]+', re.UNICODE)


def tok(text):
    return [x.lower() for x in TOK.findall(text or '')]


def _norm(vector):
    return math.sqrt(sum(v * v for v in vector.values()))


class TfIdf:
    def __init__(self):
        self.docs = []
        self.df = Counter()
        self.N = 0

    def add(self, doc_id, text):
        tf = Counter(tok(text))
        if not tf:
            return
        self.docs.append((doc_id, tf))
        for token in tf:
            self.df[token] += 1
        self.N += 1

    def idf(self, token):
        d = self.df.get(token, 0)
        return 0 if d == 0 else math.log(1 + self.N / d)

    def vec(self, tf):
        return {token: (1 + math.log(freq)) * self.idf(token) for token, freq in tf.items() if freq > 0}

    def score(self, query, top_k=10):
        if not self.docs:
            return []
        q_vec = self.vec(Counter(tok(query)))
        if not q_vec:
            return []
        q_norm = _norm(q_vec)
        results = []
        for doc_id, tf in self.docs:
            d_vec = self.vec(tf)
            if not d_vec:
                continue
            d_norm = _norm(d_vec)
            if d_norm == 0:
                continue
            common = set(q_vec).intersection(d_vec)
            score = sum(q_vec[t] * d_vec[t] for t in common) / (q_norm * d_norm)
            if score > 0:
                results.append((doc_id, score))
        results.sort(key=lambda item: item[1], reverse=True)
        return results[:top_k]
