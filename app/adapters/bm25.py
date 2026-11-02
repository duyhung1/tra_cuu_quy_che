"""BM25 retriever over clause units (TASK-006, blueprint §6.4, ADR-003)."""

import math
from collections import Counter

from app.domain.text import tokenize
from app.domain.types import Hit, Unit

K1, B = 1.5, 0.75


class Bm25Retriever:
    def __init__(self) -> None:
        self.rebuild([])

    def rebuild(self, units: list[Unit]) -> None:
        self.units = units
        self.tf = {u.id: Counter(tokenize(u.text)) for u in units}
        self.len = {u.id: sum(c.values()) for u, c in zip(units, self.tf.values(), strict=True)}
        n = len(units)
        self.avglen = (sum(self.len.values()) / n) if n else 1.0
        df: Counter[str] = Counter()
        for c in self.tf.values():
            df.update(c.keys())
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}

    def score(self, question: str, unit: Unit) -> float:
        tf = self.tf.get(unit.id)
        if tf is None:
            return 0.0
        norm = K1 * (1 - B + B * self.len[unit.id] / self.avglen)
        return sum(self.idf.get(t, 0.0) * tf[t] * (K1 + 1) / (tf[t] + norm) for t in set(tokenize(question)) if t in tf)

    def search(self, question: str, k: int) -> list[Hit]:
        hits = [Hit(u, self.score(question, u)) for u in self.units]
        hits = [h for h in hits if h.score > 0]
        hits.sort(key=lambda h: (-h.score, h.unit.id))
        return hits[:k]
