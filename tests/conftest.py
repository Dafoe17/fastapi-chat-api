import pytest
from fastapi.testclient import TestClient

from src.core.database import Base, Session_local_test, engine_test
from src.main import app


@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine_test)
    with TestClient(app) as client:
        yield client
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def db_session():
    db = Session_local_test()
    try:
        yield db
    finally:
        db.close()
