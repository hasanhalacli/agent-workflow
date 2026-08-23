"""Invoice service — a deliberately small FastAPI app.

This exists so a coding agent has somewhere realistic to work. It is not a
reference implementation; see FEATURE_REQUEST.md for what's missing.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.auth import require_api_key
from app.limiter import require_rate_limit
from app.db import Invoice, get_db, init_db
from app.schemas import InvoiceCreate, InvoiceOut


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(
    title="Invoice Service",
    description="Sample application for the agent-workflow series.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    """Unauthenticated liveness probe."""
    return {"status": "ok"}


@app.post("/invoices", response_model=InvoiceOut, status_code=201)
def create_invoice(
    payload: InvoiceCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key),
) -> Invoice:
    invoice = Invoice(
        customer=payload.customer,
        amount_cents=payload.amount_cents,
        currency=payload.currency,
        status="open",
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


@app.get("/invoices", response_model=list[InvoiceOut])
def list_invoices(
    limit: int = 50,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key),
    _rate: None = Depends(require_rate_limit),
) -> list[Invoice]:
    return db.query(Invoice).order_by(Invoice.id.desc()).limit(limit).all()


@app.get("/invoices/{invoice_id}", response_model=InvoiceOut)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key),
) -> Invoice:
    invoice = db.get(Invoice, invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@app.post("/invoices/{invoice_id}/pay", response_model=InvoiceOut)
def pay_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key),
) -> Invoice:
    invoice = db.get(Invoice, invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if invoice.status == "paid":
        raise HTTPException(status_code=409, detail="Invoice already paid")
    invoice.status = "paid"
    db.commit()
    db.refresh(invoice)
    return invoice
