"""POST /api/v1/ask: answer with cited sources (T-306)."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_embedder, get_llm
from app.core.config import get_settings
from app.core.db import get_engine
from app.core.errors import AppError
from app.modules.answer.service import AskOutcome, NoReadyDocuments, QuestionInvalid, ask
from app.modules.documents import repository as doc_repo
from app.modules.retrieval.queries import PgRetrieval
from app.modules.usage import repository as usage_repo
from app.ports.ai import EmbeddingPort, LLMPort

router = APIRouter(tags=["ask"])


class AskRequest(BaseModel):
    question: str


async def _log(outcome: AskOutcome) -> None:
    # Separate transaction: the usage log must be written even when the request fails.
    async with get_engine().begin() as conn:
        await usage_repo.log_ask(conn, outcome)


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
                ready_documents=await doc_repo.ready_count(conn),
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
