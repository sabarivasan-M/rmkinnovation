import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ["DATABASE_URL"] = "sqlite:///./test_qshield.db"
os.environ["BLOCKCHAIN_ENABLED"] = "false"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models  # noqa: F401
from app.database.session import Base, get_db
from app.database.seed import seed_demo_data
from app.main import app

TEST_DB_PATH = Path(__file__).resolve().parent / "test_qshield.db"
TEST_ENGINE = create_engine(f"sqlite:///{TEST_DB_PATH}", connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)


@pytest.fixture(scope="session", autouse=True)
def _setup_test_db():
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
    Base.metadata.create_all(bind=TEST_ENGINE)
    db = TestSessionLocal()
    seed_demo_data(db)
    db.close()
    yield
    TEST_ENGINE.dispose()
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


def _override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture()
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client():
    from fastapi.testclient import TestClient

    with TestClient(app) as c:
        yield c
