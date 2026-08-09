"""Tests for the invoice service.

Note what these do and don't cover — part five uses this file as an example of
tests that pass without proving very much.
"""

from __future__ import annotations

import os
from pathlib import Path

TEST_DB = Path("./test_invoices.db")
os.environ.setdefault("API_KEYS", "test-key-local-only")
os.environ.setdefault("DATABASE_URL", f"sqlite:///{TEST_DB}")

import pytest
from fastapi.testclient import TestClient

from app.db import init_db
from app.main import app

AUTH = {"X-API-Key": "test-key-local-only"}


@pytest.fixture(scope="module", autouse=True)
def _fresh_database() -> None:
    """Start every run from an empty database, and don't leave one behind."""
    TEST_DB.unlink(missing_ok=True)
    init_db()
    yield
    TEST_DB.unlink(missing_ok=True)


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


def test_health_needs_no_auth(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_invoice_requires_api_key(client: TestClient) -> None:
    response = client.post("/invoices", json={"customer": "Acme", "amount_cents": 1000})
    assert response.status_code == 401


def test_create_and_fetch_invoice(client: TestClient) -> None:
    created = client.post(
        "/invoices",
        json={"customer": "Acme GmbH", "amount_cents": 12500, "currency": "EUR"},
        headers=AUTH,
    )
    assert created.status_code == 201
    invoice_id = created.json()["id"]

    fetched = client.get(f"/invoices/{invoice_id}", headers=AUTH)
    assert fetched.status_code == 200
    assert fetched.json()["customer"] == "Acme GmbH"
    assert fetched.json()["status"] == "open"


def test_paying_twice_conflicts(client: TestClient) -> None:
    created = client.post(
        "/invoices", json={"customer": "Beta Ltd", "amount_cents": 500}, headers=AUTH
    )
    invoice_id = created.json()["id"]

    assert client.post(f"/invoices/{invoice_id}/pay", headers=AUTH).status_code == 200
    assert client.post(f"/invoices/{invoice_id}/pay", headers=AUTH).status_code == 409


def test_unknown_invoice_returns_404(client: TestClient) -> None:
    assert client.get("/invoices/999999", headers=AUTH).status_code == 404


@pytest.mark.parametrize("amount", [0, -1])
def test_rejects_non_positive_amounts(client: TestClient, amount: int) -> None:
    response = client.post(
        "/invoices", json={"customer": "Acme", "amount_cents": amount}, headers=AUTH
    )
    assert response.status_code == 422
