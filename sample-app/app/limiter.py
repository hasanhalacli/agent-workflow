"""Naive fixed-window rate limiter (agent draft — see the open PR review)."""

from __future__ import annotations

import os
import time

from fastapi import Header, HTTPException

_WINDOW = 60.0
_counts: dict[str, tuple[float, int]] = {}


def require_rate_limit(x_api_key: str = Header(default="")) -> None:
    limit = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))
    now = time.monotonic()
    window_start, count = _counts.get(x_api_key, (now, 0))
    if now - window_start >= _WINDOW:
        window_start, count = now, 0
    count += 1
    _counts[x_api_key] = (window_start, count)
    if count > limit:
        retry_after = int(_WINDOW - (now - window_start)) or 1
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(retry_after)},
        )
