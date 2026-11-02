"""Runtime settings, read from environment variables (TASK-001)."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    db_path: str = "data/tcqc.db"
    top_k: int = 8
    threshold: float = 2.0  # τ, blueprint §6.7; tuned on the golden set (TEST_REPORT)
    min_coverage: float = 0.5  # CR-001
    timeout_s: float = 30.0
    today: str | None = None  # TCQC_TODAY=yyyy-mm-dd overrides the clock (tests)
    max_files: int = 10
    max_bytes: int = 20 * 1024 * 1024
    max_pages: int = 300
    max_documents: int = 50


def get_settings() -> Settings:
    env = os.environ.get
    return Settings(
        db_path=env("TCQC_DB", "data/tcqc.db"),
        threshold=float(env("TCQC_THRESHOLD", "2.0")),
        min_coverage=float(env("TCQC_MIN_COVERAGE", "0.5")),
        today=env("TCQC_TODAY") or None,
    )
