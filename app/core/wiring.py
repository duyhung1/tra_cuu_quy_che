"""Pick the adapters (real or fake) for each port. Only this file imports app.adapters."""

from app.adapters.ai_anthropic import AnthropicLLM
from app.adapters.ai_fake import FakeEmbedder, FakeLLM
from app.adapters.embedding_tei import TEIEmbedding
from app.adapters.storage_s3 import S3Storage
from app.core.config import Settings
from app.ports.ai import EmbeddingPort, LLMPort
from app.ports.storage import ObjectStoragePort


def build_storage(settings: Settings) -> ObjectStoragePort:
    return S3Storage(settings)


def build_embedder(settings: Settings, timeout_s: float = 10.0) -> EmbeddingPort:
    if settings.embedding_provider == "fake":
        return FakeEmbedder()
    if settings.embedding_provider == "tei":
        return TEIEmbedding(settings.tei_url, timeout_s=timeout_s)
    raise NotImplementedError(settings.embedding_provider)


def build_llm(settings: Settings) -> LLMPort:
    if settings.ai_provider == "fake":
        return FakeLLM()
    if settings.ai_provider == "anthropic":
        return AnthropicLLM(
            settings.anthropic_api_key, settings.llm_model, settings.llm_timeout_s, settings.llm_max_tokens
        )
    raise NotImplementedError(settings.ai_provider)
