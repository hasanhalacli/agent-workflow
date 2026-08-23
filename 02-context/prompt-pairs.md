# Prompt pairs: same task, different feeding

Task: implement the rate limiter planned in [`01-planning/PLAN.filled.md`](../01-planning/PLAN.filled.md).

---

## Pair 1 — description vs. reference

### ❌ Weak
```
Add rate limiting to the invoice endpoints. We check API keys from an
env var and return 401 if invalid. Make it production-ready.
```

### ✅ Strong
```
Add per-API-key rate limiting to the invoice endpoints in @app/main.py.
Follow the dependency pattern used for auth — see how require_api_key
is injected in @app/auth.py. Same shape.
```

**What changed in the output:** the weak prompt produced a standalone middleware class with its own key-parsing logic (duplicating `auth.py`, minus the constant-time comparison). The strong prompt produced a `require_rate_limit` dependency mirroring the existing wiring — reviewable in one pass because it looks like the code around it.

---

## Pair 2 — prose spec vs. failing test

### ❌ Weak
```
Requests over the limit should be rejected with an appropriate error
and the client should know when to retry.
```

### ✅ Strong
```
Make @tests/test_rate_limit.py pass. Don't modify the assertions.
```
…where the test file already pins the behavior:
```python
def test_101st_request_in_a_minute_is_rejected(client, standard_key):
    for _ in range(100):
        assert client.get("/invoices", headers=standard_key).status_code == 200
    blocked = client.get("/invoices", headers=standard_key)
    assert blocked.status_code == 429
    assert "Retry-After" in blocked.headers
```

**What changed in the output:** "appropriate error" came back as a bare 400 with a prose message. The test-first version came back as 429 + `Retry-After` — because there was exactly one way to be done.

---

## Pair 3 — open uncertainty vs. inherited guess

### ❌ Weak
```
Use Redis for the shared counter across replicas.
```
(written while the Redis decision was still open)

### ✅ Strong
```
We need a counter shared across 3 replicas. List the options with what
each costs to run and operate. Don't implement yet.
```

**What changed in the output:** the weak prompt yields a full Redis integration — new dependency, docker-compose service, connection pooling — implementing a decision nobody made. The strong prompt yields a half-page comparison (Redis vs. gateway-level limiting vs. sticky sessions) and the decision stays where it belongs: with you.
