# 01 — Planning

Companion to **[Plan Before You Prompt](https://www.halacli.com/24_2026-08-08-plan-before-you-prompt.html)**.

The input is [`sample-app/FEATURE_REQUEST.md`](../sample-app/FEATURE_REQUEST.md) — a one-line ticket: *"add rate limiting to the API."* The point of this directory is what happens between reading that ticket and writing any code.

## What's here

| File | What it is |
|---|---|
| [`prompts.md`](prompts.md) | The one-line prompt vs. the one I should have written, side by side |
| [`PLAN.template.md`](PLAN.template.md) | The blank plan template — six sections, copy it |
| [`PLAN.filled.md`](PLAN.filled.md) | The same template filled in for the rate-limiting ticket |

## The short version

An underspecified prompt doesn't produce nothing. It produces **confident guesses** — and the agent will never tell you it was guessing.

Three habits, in order:

1. **Make it interview you.** Ask for questions before code. Good questions are about constraint, intent and risk; if the agent has no questions on a non-trivial task, it hasn't understood it.
2. **Write the plan to a file, not into the chat.** A plan in a transcript dies with the session and can't be handed to anyone. A plan in a file is reviewable and diffable.
3. **Name what's out of scope.** This is the section everyone skips and the one that prevents drift.

## The rule worth stealing

> **Size every task to the diff you'll actually read.**

If a step produces a 900-line diff, be honest — you won't review it. You'll skim, see plausible code, and approve. Everything downstream of that is theatre.

## Review the plan, not just the diff

The cheapest review in the pipeline happens before a line of code exists. A wrong approach caught in a plan costs a five-minute conversation; caught in review it costs a day; caught in production it costs a weekend.
