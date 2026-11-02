"""Vector retrieval over chunks of READY documents (T-017; MVP: vector search only).
Each hit carries its article and the document's metadata so the answer can cite them."""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from app.ports.ai import RetrievedChunk

SEARCH_SQL = text(
    """
    SELECT d.filename, d.title, d.doc_number, d.effective_date,
           c.page_start, c.content, c.article, c.chapter,
           1 - (c.embedding <=> CAST(:qvec AS vector)) AS sim
      FROM chunks c
      JOIN documents d ON d.id = c.document_id
     WHERE d.status = 'ready'
     ORDER BY c.embedding <=> CAST(:qvec AS vector)
     LIMIT :top_n
    """
)


def to_pgvector(vec: list[float]) -> str:
    return "[" + ",".join(f"{x:.7f}" for x in vec) + "]"


class PgRetrieval:
    def __init__(self, conn: AsyncConnection) -> None:
        self._conn = conn

    async def search(self, qvec: list[float], top_n: int) -> list[RetrievedChunk]:
        await self._conn.execute(text("SET LOCAL hnsw.ef_search = 80"))
        rows = await self._conn.execute(SEARCH_SQL, {"qvec": to_pgvector(qvec), "top_n": top_n})
        return [
            RetrievedChunk(
                filename=r.filename,
                page_start=r.page_start,
                content=r.content,
                sim=float(r.sim),
                article=r.article,
                chapter=r.chapter,
                doc_title=r.title,
                doc_number=r.doc_number,
                effective_date=r.effective_date,
            )
            for r in rows
        ]
