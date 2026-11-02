"""Effective-date resolution (TASK-007, blueprint §6.5, BRU-001/002/003)."""

from datetime import date

from app.domain.text import content_terms
from app.domain.types import Amendment, Document, Hit, Resolution, Unit
from app.ports import Retriever

MAX_CHAIN = 5
UNLINKED_RATIO = 0.8


def _norm_title(u: Unit) -> str:
    return " ".join((u.article_title or "").lower().split())


def coverage(question: str, unit: Unit) -> tuple[int, float]:
    q = set(content_terms(question))
    if not q:
        return 0, 0.0
    matched = q & set(content_terms(unit.text))
    return len(matched), len(matched) / len(q)


def resolve(
    question: str,
    hits: list[Hit],
    units: list[Unit],
    amendments: list[Amendment],
    docs: dict[int, Document],
    today: date,
    retriever: Retriever,
    threshold: float,
    min_coverage: float,
) -> Resolution:
    if not hits:
        return Resolution(None, not_found=True)
    by_id = {u.id: u for u in units}

    def doc(u: Unit) -> Document:
        return docs[u.document_id]

    def in_force(u: Unit) -> bool:
        return doc(u).eff <= today

    def targets(u: Unit) -> list[Unit]:
        out = []
        for a in amendments:
            if a.source_unit_id != u.id:
                continue
            for t in units:
                d = doc(t)
                if d.doc_number == a.target_doc_number and t.article_no == a.target_article_no and (
                    a.target_clause_no is None or t.clause_no == a.target_clause_no
                ):
                    out.append(t)
        return out

    def amenders(t: Unit) -> list[Unit]:
        num = doc(t).doc_number
        return [
            by_id[a.source_unit_id]
            for a in amendments
            if a.source_unit_id in by_id
            and a.target_doc_number == num
            and a.target_article_no == t.article_no
            and (a.target_clause_no is None or a.target_clause_no == t.clause_no)
        ]

    # 1. threshold on the original best hit (R1, A8)
    h0 = hits[0]
    matched, cov = coverage(question, h0.unit)
    res = Resolution(None, found_score=h0.score, coverage=cov, matched_terms=matched)
    if h0.score < threshold or matched < 2 or cov < min_coverage:
        res.not_found = True
        return res

    # 2. base (R2)
    tg = targets(h0.unit)
    if tg:
        base = max(tg, key=lambda t: (retriever.score(question, t), -t.id))
    elif in_force(h0.unit):
        base = h0.unit
    else:
        current = [h for h in hits if in_force(h.unit)]
        if not current:
            res.upcoming = [h0.unit]
            return res
        base = current[0].unit
    future = [h.unit for h in hits if not in_force(h.unit)]

    # 4. newest in-force amendment, chains (A1, A2, R3)
    applied, superseded = base, []
    for _ in range(MAX_CHAIN):
        cands = [a for a in amenders(applied) if in_force(a) and doc(a).eff > doc(applied).eff]
        if not cands:
            break
        cands.sort(key=lambda a: (doc(a).eff, doc(a).signed_date or date.min, a.id), reverse=True)
        superseded.append(applied)
        superseded.extend(c for c in cands[1:] if c not in superseded)
        applied = cands[0]

    # 5. upcoming (never primary)
    upcoming = [a for a in amenders(applied) + amenders(base) if not in_force(a)]
    upcoming += [u for u in future if u not in upcoming and _norm_title(u) == _norm_title(applied) and u.id != applied.id]
    upcoming = sorted({u.id: u for u in upcoming}.values(), key=lambda u: doc(u).eff)

    # 6. unlinked conflicts (BRU-001)
    seen = {applied.document_id}
    for h in hits:
        u = h.unit
        if u.document_id in seen or not in_force(u) or _norm_title(u) != _norm_title(applied):
            continue
        if h.score < UNLINKED_RATIO * h0.score or u in superseded:
            continue
        seen.add(u.document_id)
        if doc(u).eff > doc(applied).eff and not doc(u).eff_unknown:
            superseded.append(applied)
            applied = u
        else:
            superseded.append(u)

    res.primary, res.superseded, res.upcoming = applied, superseded, upcoming
    return res
