"""SQLAlchemy Core tables mirroring migrations/versions/0001_init.py.

The four MVP tables (see docs/Thiet_ke_luong.md §5):
documents, ingestion_jobs, chunks, qa_log.
"""

import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    SmallInteger,
    Table,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

EMBEDDING_DIM = 1024

metadata = MetaData()

DOCUMENT_STATUSES = ("queued", "processing", "ready", "failed")
JOB_STATES = ("queued", "running", "retrying", "succeeded", "failed")

document_status = Enum(*DOCUMENT_STATUSES, name="document_status", create_type=False)
job_state = Enum(*JOB_STATES, name="job_state", create_type=False)

documents = Table(
    "documents",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("filename", Text, nullable=False, unique=True),
    Column("size_bytes", BigInteger, nullable=False),
    Column("pages", Integer),
    Column("status", document_status, nullable=False, server_default="queued"),
    Column("error_code", Text),
    Column("storage_key", Text, nullable=False, unique=True),
    Column("uploaded_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column("ready_at", DateTime(timezone=True)),
    # Detected from the text at ingestion; NULL when not found
    Column("doc_number", Text),
    Column("title", Text),
    Column("effective_date", Date),
)

ingestion_jobs = Table(
    "ingestion_jobs",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("document_id", UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False),
    Column("state", job_state, nullable=False, server_default="queued"),
    Column("attempt", SmallInteger, nullable=False, server_default="0"),
    Column("error", Text),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column("next_run_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column("started_at", DateTime(timezone=True)),
    Column("finished_at", DateTime(timezone=True)),
    Column("processing_ms", Integer),
)

chunks = Table(
    "chunks",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("document_id", UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False),
    Column("chunk_index", Integer, nullable=False),
    Column("page_start", Integer, nullable=False),
    Column("page_end", Integer, nullable=False),
    Column("content", Text, nullable=False),
    Column("token_count", Integer, nullable=False),
    Column("article", Text),  # "Điều 5"
    Column("chapter", Text),
    Column("embedding", Vector(EMBEDDING_DIM), nullable=False),
    UniqueConstraint("document_id", "chunk_index"),
)

qa_log = Table(
    "qa_log",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column("status", Text, nullable=False),  # ok | error
    Column("latency_ms", Integer),
    Column("input_tokens", Integer),
    Column("output_tokens", Integer),
    Column("chunk_count", Integer),
    Column("cited_count", Integer),
)
