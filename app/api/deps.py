"""Dependency providers. Tests override these with fakes via app.dependency_overrides."""

from functools import lru_cache

from app.core import wiring
from app.core.config import get_settings
from app.ports.ai import EmbeddingPort, LLMPort
from app.ports.storage import ObjectStoragePort


@lru_cache
def get_storage() -> ObjectStoragePort:
    return wiring.build_storage(get_settings())


@lru_cache
def get_embedder() -> EmbeddingPort:
    return wiring.build_embedder(get_settings(), timeout_s=10.0)


@lru_cache
def get_llm() -> LLMPort:
    return wiring.build_llm(get_settings())
