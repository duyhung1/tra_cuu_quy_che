from typing import Protocol

from app.domain import RetrievedChunk


class RetrievalPort(Protocol):
    async def search(self, qvec: list[float], top_n: int) -> list[RetrievedChunk]: ...
