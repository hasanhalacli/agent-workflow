# sample-app — invoice service

A deliberately small FastAPI service. It exists so a coding agent has somewhere realistic to work, and so the series has real diffs to review instead of hypotheticals.

**Not a reference implementation.** It's small enough to read in ten minutes and real enough to have a security surface, a dependency file, and decisions worth arguing about.

## Run it

```bash
cd sample-app
cp .env.example .env          # then set API_KEYS to anything you like
uv sync
uv run uvicorn app.main:app --reload
uv run pytest
```

No external services required — SQLite by default. Point `DATABASE_URL` at Postgres if you want something production-shaped.

## Endpoints

| Method | Path | Auth | Notes |
|---|---|---|---|
| `GET` | `/health` | none | liveness probe |
| `POST` | `/invoices` | API key | create |
| `GET` | `/invoices` | API key | list, newest first |
| `GET` | `/invoices/{id}` | API key | fetch one |
| `POST` | `/invoices/{id}/pay` | API key | 409 if already paid |

Auth is an `X-API-Key` header checked against a comma-separated `API_KEYS` env var, compared in constant time.

## What's deliberately missing

**Rate limiting** — see [`FEATURE_REQUEST.md`](FEATURE_REQUEST.md). That's the ticket the series works through.

## Deliberate defects (from part four onward)

Later stages of the series introduce real problems on purpose — a hardcoded credential, a suspicious dependency bump, a test that asserts nothing — so the security, dependency and review posts have something to actually catch.

They're marked in the commit that adds them and the review that finds them. **None of them are real credentials.** Use `git log --oneline` and the step tags to see where each was planted and caught.
