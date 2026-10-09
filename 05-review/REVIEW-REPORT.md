# Review report: PR "Add rate limiting" (the defective demo PR)

Reviewed against [`REVIEW-CHECKLIST.md`](REVIEW-CHECKLIST.md). Branch:
`feature/rate-limiting-agent-draft`. Verdict up front: **REQUEST CHANGES** —
three findings, two of them blockers.

## Finding 1 — hardcoded fallback credential (blocker)

`app/auth.py`, caught at **step 3** (credential patterns in added lines):

```diff
     raw = os.getenv("API_KEYS", "")
+    # TODO: temporary fallback for local testing, remove before merge
+    if not raw:
+        return {"demo-token-planted-for-the-security-post"}
```

A missing env var now silently authenticates a known token in every
environment that forgets to set `API_KEYS` — which is exactly the
environment that gets breached. The rules file said fail loudly; the agent
chose helpful. The CI secrets scan does **not** flag this token: it matches no
known key format, and the scan step passed in the PR's CI run. Only the
reviewer caught it — the gate knows patterns, not intent.

## Finding 2 — dependency pin loosened in an unrelated commit (blocker)

`pyproject.toml`, caught at **step 2** (dependency diff):

```diff
-    "fastapi==0.141.1",
+    "fastapi>=0.141.1",
```

Smuggled into the feature commit with no mention in the summary. A range
delegates the dependency choice to whoever publishes next. `gates.yml`
fails this mechanically; in review it's one extra second on a two-line diff.

## Finding 3 — test that asserts nothing (must fix)

`tests/test_rate_limit.py`, caught at **step 6**:

```python
    response = client.get("/invoices", headers={"X-API-Key": "demo-key"})
    assert response is not None
    assert response.status_code in (200, 429)   # can never fail
```

Executes the code path, certifies nothing — coverage tools count it,
dashboards go green. The break-the-code check confirms: with the limiter's
counting line disabled, the suite stays green. Required: the behavioral
assertions from [`02-context/prompt-pairs.md`](../02-context/prompt-pairs.md)
(101st request → 429 + `Retry-After` > 0).

## What was fine

The limiter's dependency-injection wiring follows the auth pattern as
instructed; scope is otherwise clean; no unfamiliar imports.

**Time spent: ~12 minutes.** The findings were not subtle. They were
plausible — which is the entire argument for reviewing in an order that
puts your freshest attention where the incident lives.
