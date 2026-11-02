from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import insert

from app.api.deps import get_embedder, get_llm
from app.modules.documents.adapters import sql_repo
from app.modules.qa.adapters.pg_retrieval import PgRetrieval
from app.modules.qa.application.ask import NoReadyDocuments, QuestionInvalid, ask
from app.modules.qa.ports import EmbeddingPort, LLMPort
from app.platform.config import get_settings
from app.platform.db import get_engine
from app.platform.db_schema import qa_log
from app.platform.errors import AppError

router = APIRouter(tags=["ask"])


class AskRequest(BaseModel):
    question: str


async def _log(outcome) -> None:
    # Separate transaction: the usage log must be written even when the request fails.
    async with get_engine().begin() as conn:
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


@router.post("/ask")
async def ask_question(
    body: AskRequest,
    embedder: EmbeddingPort = Depends(get_embedder),
    llm: LLMPort = Depends(get_llm),
) -> dict:
    settings = get_settings()
    async with get_engine().begin() as conn:
        try:
            outcome = await ask(
                body.question,
                ready_documents=await sql_repo.ready_count(conn),
                embedder=embedder,
                retriever=PgRetrieval(conn),
                llm=llm,
                top_n=settings.qa_top_n,
            )
        except QuestionInvalid as exc:
            raise AppError("question_invalid") from exc
        except NoReadyDocuments as exc:
            raise AppError("no_documents") from exc

    await _log(outcome)
    if outcome.status != "ok":
        raise AppError("ai_unavailable")
    return {
        "answer": outcome.answer,
        "latency_ms": outcome.latency_ms,
        "sources": [s.as_dict() for s in outcome.sources],
    }
