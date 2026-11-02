"""RuleBasedAnswerer (TASK-008, blueprint §6.7, ADR-001, CR-001).
Quotes the applied clause verbatim; never interprets document text as instructions."""

from app.domain.types import Answer, Document, Resolution, Source, Unit

NOT_FOUND = "Không tìm thấy quy định này trong các văn bản đã tải lên."
NO_CURRENT = "Hiện chưa có quy định đang áp dụng."


def _label(u: Unit) -> str:
    if not u.article_no:
        return f"trang {u.page}"
    return f"Điều {u.article_no}" + (f", khoản {u.clause_no}" if u.clause_no else "")


def _doc_name(d: Document) -> str:
    name = d.title or d.filename
    return f"{name} số {d.doc_number}" if d.doc_number else name


class RuleBasedAnswerer:
    def answer(self, question: str, resolution: Resolution, docs: dict[int, Document],
               siblings: list[Unit] | None = None) -> Answer:
        if resolution.not_found:
            return Answer(NOT_FOUND, False, [])
        sources: list[Source] = []

        def ref(u: Unit) -> int:
            for s in sources:
                if s.page == u.page and s.filename == docs[u.document_id].filename and s.article == (
                    f"Điều {u.article_no}" if u.article_no else None
                ) and s.clause == (f"khoản {u.clause_no}" if u.clause_no else None):
                    return s.ref
            d = docs[u.document_id]
            sources.append(Source(
                ref=len(sources) + 1, filename=d.filename, doc_title=d.title, doc_number=d.doc_number,
                effective_date=d.effective_date, article=f"Điều {u.article_no}" if u.article_no else None,
                clause=f"khoản {u.clause_no}" if u.clause_no else None, page=u.page,
            ))
            return len(sources)

        parts: list[str] = []
        p = resolution.primary
        if p is None:
            parts.append(NO_CURRENT)
        else:
            parts.append(f"{p.body} [{ref(p)}]")
            for s in siblings or []:  # CR-001: other relevant clauses of the same article
                parts.append(f"{s.body} [{ref(s)}]")
            for old in resolution.superseded:
                d = docs[old.document_id]
                parts.append(
                    f"Quy định này thay thế {_label(old)} của {_doc_name(d)} (trước đây: «{old.body}») [{ref(old)}]"
                )
        for up in resolution.upcoming:
            d = docs[up.document_id]
            when = d.effective_date.strftime("%d/%m/%Y") if d.effective_date else "ngày chưa xác định"
            parts.append(f"Lưu ý: {_label(up)} của {_doc_name(d)} sắp có hiệu lực từ {when}: «{up.body}» [{ref(up)}]")
        return Answer("\n\n".join(parts), True, sources)
