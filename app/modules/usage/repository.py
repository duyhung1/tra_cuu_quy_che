"""Usage log (qa_log). Stores numbers only, never question or answer text."""

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncConnection

from app.models.tables import qa_log
from app.modules.answer.service import AskOutcome


async def log_ask(conn: AsyncConnection, outcome: AskOutcome) -> None:
    await conn.execute(
        insert(qa_log).values(
            status=outcome.status,
            latency_ms=outcome.latency_ms,
            input_tokens=outcome.input_tokens,
            output_tokens=outcome.output_tokens,
            chunk_count=outcome.chunk_count,
            cited_count=len(outcome.sources),
        )
    )
