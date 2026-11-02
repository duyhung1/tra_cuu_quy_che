from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration, read from environment variables / .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://tcqc:tcqc@localhost:5432/tcqc"

    s3_bucket: str = "tcqc-documents-local"
    s3_endpoint_url: str | None = None  # set only for local S3Mock
    s3_region: str = "ap-southeast-1"
    s3_use_kms: bool = False  # True on AWS (SSE-KMS), False locally

    tei_url: str = "http://tei:80"

    anthropic_api_key: str = ""
    llm_model: str = "claude-opus-5-5"
    llm_timeout_s: float = 60.0
    llm_max_tokens: int = 2048

    qa_top_n: int = 12
    upload_max_mb: int = 20
    upload_max_files: int = 10
    pdf_max_pages: int = 300
    collection_max_docs: int = 50

    worker_poll_s: float = 2.0
    worker_stale_job_minutes: int = 10
    ingest_max_attempts: int = 3

    log_level: str = "INFO"

    @property
    def upload_max_bytes(self) -> int:
        return self.upload_max_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
