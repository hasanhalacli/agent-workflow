"""Request and response models."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InvoiceCreate(BaseModel):
    customer: str = Field(min_length=1, max_length=200)
    amount_cents: int = Field(gt=0, description="Amount in minor units")
    currency: str = Field(default="EUR", min_length=3, max_length=3)


class InvoiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer: str
    amount_cents: int
    currency: str
    status: str
    created_at: datetime
