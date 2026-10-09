# 04 — Blast radius

Companion to **[Rules for the Blast Radius](https://www.halacli.com/27_2026-08-29-rules-for-the-blast-radius.html)**.

A rule the agent can ignore is a request. Rules come in three layers, and only the first is a request:

| Layer | What it is | Who enforces it |
|---|---|---|
| **Ask** | Rules file — [`SECURITY-RULES.md`](SECURITY-RULES.md), [`DEPENDENCY-RULES.md`](DEPENDENCY-RULES.md) | The model, statistically |
| **Check** | [`hooks/`](hooks/) + [`.pre-commit-config.yaml`](.pre-commit-config.yaml) | Your machine, deterministically |
| **Block** | [`../.github/workflows/gates.yml`](../.github/workflows/gates.yml) + branch protection | The repo, absolutely |

## The proof, not the promise

This repo contains **deliberately planted defects** on the branch `feature/rate-limiting-agent-draft` (left as an open PR on purpose):

1. A hardcoded fallback token in `app/auth.py` — added "temporarily" to make tests pass
2. A dependency pin loosened to a version range, smuggled into an unrelated feature commit
3. A test that executes the code path but asserts nothing

The CI gates fail that PR — on the loosened pin. Open it and look at the red X: that's the Block layer doing what the Ask layer can't guarantee. Look closer, too: the secrets scan passes the planted token, because the token matches no known key format. A block stops only what its patterns know; the review in `05-review/` catches the rest.

## The one-liner that summarizes the post

> The model can be talked out of a rule. It cannot be talked out of an exit code.
