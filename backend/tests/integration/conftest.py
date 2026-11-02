"""Integration fixtures: a real PostgreSQL + pgvector.

Uses TEST_DATABASE_URL if set (e.g. in CI with a service container), otherwise
starts a pgvector/pgvector:pg16 container with Testcontainers.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest
from sqlalchemy import text

from app.platform import db as db_module
from app.platform.config import get_settings

BACKEND_DIR = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def database_url():
    url = os.environ.get("TEST_DATABASE_URL")
    container = None
    if not url:
        from testcontainers.postgres import PostgresContainer

        container = PostgresContainer("pgvector/pgvector:pg16", username="tcqc", password="tcqc", dbname="tcqc")
        container.start()
        url = (
            f"postgresql+asyncpg://tcqc:tcqc@{container.get_container_host_ip()}:"
            f"{container.get_exposed_port(5432)}/tcqc"
        )
    os.environ["DATABASE_URL"] = url
    get_settings.cache_clear()
    subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=BACKEND_DIR,
        check=True,
        env={**os.environ, "DATABASE_URL": url},
    )
    yield url
    if container:
        container.stop()


@pytest.fixture
async def engine(database_url):
    """Fresh engine per test (pytest-asyncio uses a new event loop per test) and clean tables."""
    get_settings.cache_clear()
    db_module.get_engine.cache_clear()
    eng = db_module.get_engine()
    async with eng.begin() as conn:
        await conn.execute(text("TRUNCATE qa_log, chunks, ingestion_jobs, documents CASCADE"))
    yield eng
    await eng.dispose()
    db_module.get_engine.cache_clear()
