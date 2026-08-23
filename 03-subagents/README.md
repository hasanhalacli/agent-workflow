# 03 — Sub-agents

Companion to **[Delegating to Sub-Agents](https://www.halacli.com/26_2026-08-22-delegating-to-subagents.html)**.

A sub-agent is a fresh context window with a narrow brief. The definitions in [`agents/`](agents/) are drop-in Claude Code agents — copy them to `.claude/agents/` in your project. On tools without native sub-agents, replicate the effect manually: fresh chat, tight brief, bring back only the conclusion.

## The decision rule

| Delegate when | Stay single-threaded when |
|---|---|
| Tasks are independent and parallel | Steps depend on each other |
| The work is read-only recon/audit | The work edits shared files |
| You need a clean-context verdict | You need accumulated session nuance |
| The result is a summary, not a diff | The task is small (overhead > benefit) |

The economics are real: Anthropic's multi-agent research beat a single agent by ~90% — at ~15× the tokens. Great price for recon that prevents a wrong architecture; absurd price for renaming a function.

## What's here

| File | Job |
|---|---|
| [`agents/dependency-auditor.md`](agents/dependency-auditor.md) | Audits any proposed dependency change before it's accepted |
| [`agents/refuter.md`](agents/refuter.md) | Adversarial review of a finished change — never sees the author's reasoning |
| [`recon-fanout.md`](recon-fanout.md) | The parallel read-only recon prompt used before implementing |

## The line that matters

The refuter **improves what lands on your desk**. It does not replace you reading the diff. Two agents approving each other is a closed loop with no human in it — the merge decision stays with a person. See [part five](https://www.halacli.com/28_2026-09-05-review-before-you-push.html).
