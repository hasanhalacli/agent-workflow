# Plan: rate-limit the public API per API key

Worked example — the template filled in for [`FEATURE_REQUEST.md`](../sample-app/FEATURE_REQUEST.md).
Note how much of this is *decisions*, not *code*.

## Goal

A client that exceeds its request allowance gets a `429` with a `Retry-After`
header instead of being served, and the allowance is enforced consistently no
matter which replica handles the request.

## Constraints

Answers from the interview. Every one of these is something the agent would
otherwise have decided on its own.

- **Per API key**, not per IP — the service sits behind a load balancer, so
  source IP is the balancer for most traffic and useless as an identity.
- **100 req/min** for standard keys, **1000 req/min** for partner keys. The
  tier lives on the key, so the limiter has to resolve the key first.
- **3 replicas** in production ⇒ an in-process counter would give each client
  3× its real allowance. The counter must be shared.
- **On breach: 429 + `Retry-After`.** Never queue — queuing turns a rate
  problem into a latency problem and hides it from the caller.
- **Internal service-to-service calls are exempt.** They authenticate with a
  separate key class.
- `/health` stays unauthenticated **and** unlimited — it's a liveness probe.

## Files to touch

- `app/limiter.py` — new; the limiting logic
- `app/main.py` — wire the dependency into the invoice routes
- `app/auth.py` — expose the key's tier (read-only change, no auth logic edits)
- `tests/test_rate_limit.py` — new
- `pyproject.toml` — only if we agree on a shared backend
- `.env.example` — document any new configuration

## Approach

1. Resolve the tier for an API key in `auth.py` and return it alongside the key.
   No change to how authentication decides yes/no.
2. Add `app/limiter.py` with a fixed-window counter behind a small interface,
   plus an in-memory implementation. Interface first so the backend is a
   swap, not a rewrite.
3. Wire it into the invoice routes as a FastAPI dependency. `/health` excluded.
4. Tests: under the limit passes, over the limit returns 429, `Retry-After` is
   present and sane, tiers are enforced independently, exempt keys bypass.
5. **Decision point — shared backend.** Bring the options back to me with the
   trade-offs; do not add infrastructure unilaterally.

## Out of scope

- **Don't touch the auth middleware's decision logic.** Reading the tier is
  fine; changing how keys are validated is not.
- **Don't add any infrastructure dependency without asking.** If the answer is
  Redis, that's a conversation, not a commit.
- **Don't reformat files you only needed to read.**
- No per-endpoint limits, no burst allowance, no admin override UI. Later, if
  ever.

## Verification

```bash
uv run pytest tests/test_rate_limit.py
uv run pytest                 # nothing else broke
uv run uvicorn app.main:app   # still boots
```

Done when the 101st request from a standard key inside one minute returns
`429` with a `Retry-After` header, the 101st from a partner key is served (`200`),
and the full suite is green.

## Open questions

- **Shared counter backend.** Redis is the obvious answer and the expensive
  one — it's a new production dependency to run, monitor and secure for a
  feature that is not, today, business-critical. Worth checking whether the
  load balancer or API gateway can already do per-key limiting before we own
  another service. **Blocking step 5.**
- Fixed window is simpler; sliding window is fairer at the boundary. Starting
  fixed unless the burst behaviour at minute boundaries turns out to matter.
