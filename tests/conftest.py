import pytest

from app.config import Settings
from tests.fixtures.make_pdfs import HERE, write_all

TODAY = "2026-11-02"


@pytest.fixture(scope="session")
def pdfs():
    write_all()
    return HERE


@pytest.fixture
def settings(tmp_path):
    return Settings(db_path=str(tmp_path / "t.db"), today=TODAY)


@pytest.fixture
def built(settings, pdfs):
    from app import wiring

    store, ingestor, ask = wiring.build(settings)
    ingestor.ingest_batch([(p.name, p.read_bytes()) for p in sorted((pdfs / "sample").glob("*.pdf"))])
    return store, ingestor, ask
