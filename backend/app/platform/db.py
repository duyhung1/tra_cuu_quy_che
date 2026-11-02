from collections.abc import AsyncIterator
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from app.platform.config import get_settings


@lru_cache
def get_engine() -> AsyncEngine:
    settings = get_settings()
    return create_async_engine(settings.database_url, pool_size=5, pool_pre_ping=True)


async def get_db() -> AsyncIterator[AsyncConnection]:
    """FastAPI dependency: one connection + one transaction per request."""
    async with get_engine().begin() as conn:
        yield conn
