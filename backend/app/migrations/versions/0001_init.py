"""MVP schema: documents, ingestion_jobs, chunks, qa_log (task T-004).

Revision ID: 0001_init
Revises:
"""

from alembic import op

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute("CREATE TYPE document_status AS ENUM ('queued','processing','ready','failed')")
    op.execute("CREATE TYPE job_state AS ENUM ('queued','running','retrying','succeeded','failed')")

    op.execute(
        """
        CREATE TABLE documents (
          id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
          filename     text NOT NULL UNIQUE CHECK (length(filename) BETWEEN 1 AND 255),
          size_bytes   bigint NOT NULL CHECK (size_bytes > 0),
          pages        integer CHECK (pages IS NULL OR pages >= 1),
          status       document_status NOT NULL DEFAULT 'queued',
          error_code   text,
          storage_key  text NOT NULL UNIQUE,
          uploaded_at  timestamptz NOT NULL DEFAULT now(),
          ready_at     timestamptz,
          doc_number   text,
          title        text,
          effective_date date,
          CONSTRAINT documents_failed_has_code CHECK (status <> 'failed' OR error_code IS NOT NULL)
        )
        """
    )
    op.execute("CREATE INDEX documents_status_idx ON documents (status)")

    op.execute(
        """
        CREATE TABLE ingestion_jobs (
          id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
          document_id   uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
          state         job_state NOT NULL DEFAULT 'queued',
          attempt       smallint NOT NULL DEFAULT 0,
          error         text,
          created_at    timestamptz NOT NULL DEFAULT now(),
          next_run_at   timestamptz NOT NULL DEFAULT now(),
          started_at    timestamptz,
          finished_at   timestamptz,
          processing_ms integer
        )
        """
    )
    op.execute(
        "CREATE INDEX ingestion_jobs_pick_idx ON ingestion_jobs (next_run_at) "
        "WHERE state IN ('queued','retrying')"
    )
    op.execute("CREATE INDEX ingestion_jobs_running_idx ON ingestion_jobs (started_at) WHERE state = 'running'")

    op.execute(
        """
        CREATE TABLE chunks (
          id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
          document_id  uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
          chunk_index  integer NOT NULL CHECK (chunk_index >= 0),
          page_start   integer NOT NULL CHECK (page_start >= 1),
          page_end     integer NOT NULL,
          content      text NOT NULL,
          token_count  integer NOT NULL CHECK (token_count >= 1),
          article      text,
          chapter      text,
          embedding    vector(1024) NOT NULL,
          CONSTRAINT chunks_page_range CHECK (page_end >= page_start),
          CONSTRAINT chunks_document_index_uq UNIQUE (document_id, chunk_index)
        )
        """
    )
    op.execute(
        "CREATE INDEX chunks_embedding_hnsw_idx ON chunks "
        "USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64)"
    )

    # Usage log for the pilot. Deliberately stores NO question or answer text.
    op.execute(
        """
        CREATE TABLE qa_log (
          id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
          created_at    timestamptz NOT NULL DEFAULT now(),
          status        text NOT NULL CHECK (status IN ('ok','error')),
          latency_ms    integer,
          input_tokens  integer,
          output_tokens integer,
          chunk_count   integer,
          cited_count   integer
        )
        """
    )
    op.execute("CREATE INDEX qa_log_created_idx ON qa_log (created_at)")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS qa_log")
    op.execute("DROP TABLE IF EXISTS chunks")
    op.execute("DROP TABLE IF EXISTS ingestion_jobs")
    op.execute("DROP TABLE IF EXISTS documents")
    op.execute("DROP TYPE IF EXISTS job_state")
    op.execute("DROP TYPE IF EXISTS document_status")
