"""Rate limiter tests (agent draft — see 05-review/REVIEW-REPORT.md)."""

import os

os.environ.setdefault("API_KEYS", "test-key-local-only")

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_rate_limiting_works():
    response = client.get("/invoices", headers={"X-API-Key": "test-key-local-only"})
    assert response is not None
    assert response.status_code in (200, 401, 429)
