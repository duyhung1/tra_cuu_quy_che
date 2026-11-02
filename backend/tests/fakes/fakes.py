"""In-memory fakes for ports, used across tests."""

import hashlib
import io
import math
from typing import IO

from app.modules.qa.ports import (
    EmbeddingUnavailable,
    LLMResult,
    LLMUnavailable,
    RetrievedChunk,
)
from app.platform.db_schema import EMBEDDING_DIM


class FakeStorage:
    def __init__(self) -> None:
        self.objects: dict[str, bytes] = {}

    async def put_stream(self, key: str, fileobj: IO[bytes]) -> str:
        data = fileobj.read()
        self.objects[key] = data
        return hashlib.sha256(data).hexdigest()

    async def get_bytes(self, key: str) -> bytes:
        return self.objects[key]

    async def delete(self, key: str) -> None:
        self.objects.pop(key, None)


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
    def __init__(self, answer: str = "Câu trả lời mẫu.", fail: bool = False) -> None:
        self.answer_text = answer
        self.fail = fail
        self.last_chunks: list[RetrievedChunk] = []
        self.last_question = ""

    async def answer(self, question: str, chunks: list[RetrievedChunk]) -> LLMResult:
        self.last_question = question
        self.last_chunks = chunks
        if self.fail:
            raise LLMUnavailable("down")
        return LLMResult(self.answer_text, input_tokens=100, output_tokens=20)


class FakeUpload:
    """Mimics starlette UploadFile.read()."""

    def __init__(self, filename: str, data: bytes) -> None:
        self.filename = filename
        self._buf = io.BytesIO(data)

    async def read(self, size: int = -1) -> bytes:
        return self._buf.read(size)
