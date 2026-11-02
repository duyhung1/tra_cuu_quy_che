"""Fake AI adapters: deterministic, no network. Used by tests and by local runs
with EMBEDDING_PROVIDER=fake / AI_PROVIDER=fake (no TEI, no API key)."""

import hashlib
import math

from app.domain import LLMResult, RetrievedChunk
from app.models.tables import EMBEDDING_DIM
from app.modules.answer.prompt import NOT_FOUND_ANSWER
from app.ports.ai import EmbeddingUnavailable, LLMUnavailable


def bag_of_words_vector(text: str) -> list[float]:
    """Deterministic pseudo-embedding: hashed bag of words, L2-normalised.
    Texts sharing words get a high cosine similarity, which is enough to test retrieval."""
    vec = [0.0] * EMBEDDING_DIM
    for word in text.lower().split():
        h = int(hashlib.md5(word.strip(".,:;!?()").encode()).hexdigest(), 16)
        vec[h % EMBEDDING_DIM] += 1.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


class FakeEmbedder:
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.calls = 0

    async def embed(self, texts: list[str]) -> list[list[float]]:
        self.calls += 1
        if self.fail:
            raise EmbeddingUnavailable("tei down")
        return [bag_of_words_vector(t) for t in texts]


class FakeLLM:
    """With `answer=None` (local runs) it quotes the best excerpt and cites it as [1]."""

    def __init__(self, answer: str | None = None, fail: bool = False) -> None:
        self.answer_text = answer
        self.fail = fail
        self.last_chunks: list[RetrievedChunk] = []
        self.last_question = ""

    async def answer(self, question: str, chunks: list[RetrievedChunk]) -> LLMResult:
        self.last_question = question
        self.last_chunks = chunks
        if self.fail:
            raise LLMUnavailable("down")
        if self.answer_text is not None:
            return LLMResult(self.answer_text, input_tokens=100, output_tokens=20)
        if not chunks:
            return LLMResult(NOT_FOUND_ANSWER)
        excerpt = " ".join(chunks[0].content.split()[:60])
        return LLMResult(f"(Câu trả lời giả lập) {excerpt} [1]", input_tokens=100, output_tokens=20)
