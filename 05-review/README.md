# 05 — Review

Companion to **[Review Before You Push](https://www.halacli.com/28_2026-09-05-review-before-you-push.html)** — the part the other four exist to make possible.

| File | What it is |
|---|---|
| [`REVIEW-CHECKLIST.md`](REVIEW-CHECKLIST.md) | The blast-radius-order procedure as a paste-able checklist |
| [`REVIEW-REPORT.md`](REVIEW-REPORT.md) | A real filled-in review of this repo's defective demo PR — what was caught and how |
| [`../.github/pull_request_template.md`](../.github/pull_request_template.md) | PR template with AI-involvement disclosure + "what I personally verified" |

Want the checklist tailored to your stack and risk level? Use the
[PR Review Checklist generator](https://www.halacli.com/pr-review-checklist.html) —
client-side, nothing leaves your browser.

## The two rules everything else hangs on

1. **Read the diff in blast-radius order, not file order** — dependencies → config/secrets → auth → error handling → feature code → tests last, with the question "what do they NOT assert?"
2. **The merge decision stays human.** Automate every mechanical check; never delegate the judgment. An agent writing code and an agent approving it is self-certification with extra steps.
