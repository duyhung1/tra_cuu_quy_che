"""Alembic environment. Migrations run with the synchronous psycopg driver;
the application itself uses asyncpg."""

from alembic import context
from sqlalchemy import create_engine, pool

from app.platform.config import get_settings


def _sync_url() -> str:
    return get_settings().database_url.replace("+asyncpg", "+psycopg")


def run_migrations_offline() -> None:
    context.configure(url=_sync_url(), literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(_sync_url(), poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
