import pytest

from server import database as db


@pytest.fixture
def temporary_database(monkeypatch, tmp_path):
    database_path = tmp_path / "metrics.db"
    monkeypatch.setattr(db, "DATABASE_PATH", database_path)
    monkeypatch.setattr(db, "RETENTION_COUNT", 1000)
    db.create_metrics_table()
    return db
