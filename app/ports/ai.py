"""Ports of the Q&A module. The use case depends only on these protocols, so the
LLM / embedding providers can be swapped without touching it."""

from typing import Protocol

from app.domain import LLMResult, RetrievedChunk


class LLMUnavailable(Exception):
    """The LLM provider failed or timed out; the request may be retried."""


class EmbeddingUnavailable(Exception):
    """The embedding service failed or timed out."""


class EmbeddingPort(Protocol):
    async def embed(self, texts: list[str]) -> list[list[float]]: ...


class LLMPort(Protocol):
    async def answer(self, question: str, chunks: list[RetrievedChunk]) -> LLMResult: ...
