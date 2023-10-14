import pytest
from fastapi.testclient import TestClient

from ..application import app


@pytest.fixture
def client():
    yield TestClient(app, base_url="http://127.0.0.1:8000")


@pytest.fixture(autouse=True)
async def clear_db():
    yield
    await app.container.db().drop_database()
    await app.container.db().create_database()
