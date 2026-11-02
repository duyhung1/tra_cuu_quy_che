"""Ask use case (T-020). Pure orchestration over ports: no FastAPI, no SDKs.
The answer comes back with the sources (articles) it cites."""

import time
from dataclasses import dataclass, field

from app.modules.qa.application.citations import Source, build_sources, strip_invalid_markers
from app.modules.qa.ports import (
    EmbeddingPort,
    EmbeddingUnavailable,
    LLMPort,
    LLMUnavailable,
    RetrievalPort,
)

MAX_QUESTION_CHARS = 2000


class QuestionInvalid(Exception):
    pass


class NoReadyDocuments(Exception):
    pass


class AiUnavailable(Exception):
    pass


@dataclass(frozen=True)
class AskOutcome:
    status: str  # ok | error
    answer: str | None
    latency_ms: int
    input_tokens: int = 0
    output_tokens: int = 0
    chunk_count: int = 0
    sources: list[Source] = field(default_factory=list)


def validate_question(question: str) -> str:
    q = (question or "").strip()
    if not 1 <= len(q) <= MAX_QUESTION_CHARS:
        raise QuestionInvalid()
    return q


async def ask(
    question: str,
    *,
    ready_documents: int,
    embedder: EmbeddingPort,
    retriever: RetrievalPort,
    llm: LLMPort,
    top_n: int,
) -> AskOutcome:
    """Raises QuestionInvalid / NoReadyDocuments before any external call.
    External failures are returned as an outcome with status='error' so the caller
    can log them, then raise AiUnavailable."""
    q = validate_question(question)
    if ready_documents == 0:
        raise NoReadyDocuments()

    start = time.perf_counter()
    try:
        [qvec] = await embedder.embed([q])
        chunks = await retriever.search(qvec, top_n)
        result = await llm.answer(q, chunks)
    except (EmbeddingUnavailable, LLMUnavailable):
        return AskOutcome("error", None, round((time.perf_counter() - start) * 1000))

    answer = strip_invalid_markers(result.text, len(chunks))
    return AskOutcome(
        status="ok",
        answer=answer,
        latency_ms=round((time.perf_counter() - start) * 1000),
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        chunk_count=len(chunks),
        sources=build_sources(answer, chunks),
    )
