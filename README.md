# agent-workflow

**How to actually ship with a coding agent** — planning, context, delegation, guardrails, and review. A worked example on a small but real codebase.

This is the companion repo to a five-part series on working with coding agents like a professional. Its sibling, [**agent-harness**](https://github.com/hasanhalacli/agent-harness), covers *how the agent behaves* — the rules, skills and memory that stop it agreeing with your worst idea. This repo covers *how you work with it*.

> **The thesis:** the agent writes the code. You own the decision.

---

## The series

| # | Post | Directory | What it demonstrates |
|---|------|-----------|----------------------|
| 1 | Plan Before You Prompt | [`01-planning/`](01-planning/) | Turning a vague ticket into a scoped, reviewable plan |
| 2 | Prompting Is Context Engineering | [`02-context/`](02-context/) | Weak vs. strong prompts, with the real output of each |
| 3 | Delegating to Sub-Agents | [`03-subagents/`](03-subagents/) | When a second agent pays for itself — and when it burns tokens |
| 4 | Rules for the Blast Radius | [`04-blast-radius/`](04-blast-radius/) | Security and dependency policy an agent can't route around |
| 5 | Review Before You Push | [`05-review/`](05-review/) | The review procedure — the part a human still owns |

There is one **deliberately defective pull request left open** — an agent-written rate-limiter draft with three planted problems. The CI gates fail it, and [`05-review/REVIEW-REPORT.md`](05-review/REVIEW-REPORT.md) is the human review that catches all three. That PR is the whole thesis in one artifact.

## The sample app

[`sample-app/`](sample-app/) is a small FastAPI invoice service — a few endpoints, API-key auth, a database. It's deliberately incomplete: it has no rate limiting, which is the [feature request](sample-app/FEATURE_REQUEST.md) the whole series works through.

It's intentionally small enough to read in ten minutes, and real enough to have a security surface, a dependency file, and decisions worth arguing about.

```bash
cd sample-app
uv sync
uv run uvicorn app.main:app --reload
uv run pytest
```

## How to read this repo

Each directory maps to one post and stands alone. If you only read one, read `05-review/` — it's the part everyone skips and the part that decides whether any of the rest mattered.

The git history is part of the material: tags mark each stage of the worked example, so you can `git diff` between them and see exactly what changed at each step rather than taking my word for it.

## A note on the planted defects

From part four onward this repo contains **deliberately introduced problems** — a hardcoded credential, a suspicious dependency bump, an over-engineered abstraction. They exist so the security, dependency and review posts have something real to catch.

They are clearly marked, obviously fake, and none of them are real credentials. Don't copy those files into anything.

## License

[MIT](LICENSE) — take what's useful.

---

**Hasan Halacli** — AI Solution Architect & Technical Lead

[Portfolio](https://www.halacli.com/) · [Blog](https://www.halacli.com/blog.html) · [LinkedIn](https://www.linkedin.com/in/hasan-h-326b5a171/) · [GitHub](https://github.com/hasanhalacli)

> Related: [**agent-harness**](https://github.com/hasanhalacli/agent-harness) — the rules, skills and memory that turn a sycophantic coding agent into an expert.
