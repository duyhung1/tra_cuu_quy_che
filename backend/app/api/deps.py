"""Dependency providers. Tests override these with fakes via app.dependency_overrides."""

from functools import lru_cache

from app.modules.qa.adapters.anthropic_llm import AnthropicLLM
from app.modules.qa.adapters.tei_embedding import TEIEmbedding
from app.modules.qa.ports import EmbeddingPort, LLMPort
from app.platform.config import get_settings
from app.platform.storage import ObjectStoragePort, S3Storage


@lru_cache
def _storage() -> S3Storage:
    return S3Storage()


@lru_cache
def _embedder() -> TEIEmbedding:
    return TEIEmbedding(get_settings().tei_url, timeout_s=10.0)


@lru_cache
def _llm() -> AnthropicLLM:
    s = get_settings()
    return AnthropicLLM(s.anthropic_api_key, s.llm_model, s.llm_timeout_s, s.llm_max_tokens)


def get_storage() -> ObjectStoragePort:
    return _storage()


def get_embedder() -> EmbeddingPort:
    return _embedder()


def get_llm() -> LLMPort:
    return _llm()
