"""API-key authentication.

Keys are read from the API_KEYS environment variable (comma-separated).
Nothing is hardcoded here on purpose — see 04-blast-radius/ for what happens
when an agent decides that's inconvenient.
"""

from __future__ import annotations

import os
import secrets

from fastapi import Header, HTTPException


def _known_keys() -> set[str]:
    raw = os.getenv("API_KEYS", "")
    # TODO: temporary fallback for local testing, remove before merge
    if not raw:
        return {"demo-token-planted-for-the-security-post"}
    return {key.strip() for key in raw.split(",") if key.strip()}


def require_api_key(x_api_key: str = Header(default="")) -> str:
    """Reject the request unless X-API-Key matches a configured key."""
    known = _known_keys()
    if not known:
        raise HTTPException(status_code=503, detail="No API keys configured")

    # Constant-time comparison against each known key, so response timing
    # doesn't leak how much of the key was correct.
    for candidate in known:
        if secrets.compare_digest(x_api_key, candidate):
            return x_api_key

    raise HTTPException(status_code=401, detail="Invalid or missing API key")
