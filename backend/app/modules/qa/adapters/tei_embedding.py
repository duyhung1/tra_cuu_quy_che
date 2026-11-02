"""Embedding adapter for Hugging Face Text Embeddings Inference running
BAAI/bge-m3 (self-hosted, so document text never leaves our infrastructure)."""

import httpx

from app.modules.qa.ports import EmbeddingUnavailable

BATCH_SIZE = 32


class TEIEmbedding:
    def __init__(self, base_url: str, timeout_s: float = 30.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout_s

    async def embed(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                for i in range(0, len(texts), BATCH_SIZE):
                    resp = await client.post(
                        f"{self._base_url}/embed",
                        json={"inputs": texts[i : i + BATCH_SIZE], "normalize": True, "truncate": True},
                    )
                    resp.raise_for_status()
                    vectors.extend(resp.json())
        except (httpx.HTTPError, ValueError) as exc:
            raise EmbeddingUnavailable(str(exc)) from exc
        if len(vectors) != len(texts):
            raise EmbeddingUnavailable(f"expected {len(texts)} vectors, got {len(vectors)}")
        return vectors
