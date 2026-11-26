import os
import tempfile

os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.mkdtemp()}/test.db"

from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_crud_flow():
    with TestClient(app) as client:
        res = client.post("/notes", json={"title": "first", "content": "hello"})
        assert res.status_code == 201
        note = res.json()
        assert note["title"] == "first"

        res = client.get("/notes")
        assert res.status_code == 200
        assert len(res.json()) == 1

        res = client.get(f"/notes/{note['id']}")
        assert res.status_code == 200

        res = client.patch(f"/notes/{note['id']}", json={"content": "updated"})
        assert res.status_code == 200
        assert res.json()["content"] == "updated"

        res = client.delete(f"/notes/{note['id']}")
        assert res.status_code == 204

        res = client.get(f"/notes/{note['id']}")
        assert res.status_code == 404


def test_validation_rejects_empty_title():
    with TestClient(app) as client:
        res = client.post("/notes", json={"title": "", "content": "x"})
    assert res.status_code == 422
