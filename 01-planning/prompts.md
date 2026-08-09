# Prompts: the one I typed vs. the one I should have

## ❌ What I typed the first time

```
add rate limiting to the API
```

Nine words. The agent produced a middleware, a Redis dependency nobody approved, a config module, and a test file that asserts almost nothing.

The output wasn't *wrong*. It was a correct answer to a different question than the one I meant — because I never said which question I meant.

---

## ✅ What I should have typed

```
We need rate limiting on the public API.

Constraints:
- Per API key, not per IP — we're behind a load balancer
- 100 req/min standard, 1000 for partner keys
- We run 3 replicas, so the counter has to be shared
- On breach: 429 with Retry-After. Never queue.
- Internal service-to-service calls are exempt

Out of scope:
- Don't touch the auth middleware
- Don't add infrastructure without asking me first
- Don't reformat files you only needed to read

Done when:
- tests/test_rate_limit.py passes
- the 101st request within a minute returns 429
- docker compose up still boots clean

Before you write any code: tell me what's ambiguous here,
and what you'd change about this approach.
```

Ninety seconds to write.

---

## What changed, line by line

| Section | What it buys you |
|---|---|
| **Constraints** | The five decisions the agent was about to make silently are now made by me. "3 replicas, shared counter" is the line that surfaces the Redis question *as a question*. |
| **Out of scope** | Fences off drift. Agents "improve" adjacent code; naming the boundary converts that from something you find in review into something you agreed on in advance. |
| **Done when** | A command that runs. Without it, the agent's default bar is "the code exists and imports." |
| **The last line** | Keeps the interview alive. I might be wrong too — better to find out before it starts typing. |

## The one people leave out

The closing line. It's tempting to drop it once you've written good constraints — you've done the thinking, why invite argument?

Because a plan that can't be challenged isn't a plan, it's an instruction. The whole point of a [well-configured agent](https://github.com/hasanhalacli/agent-harness) is that it pushes back when it has a reason to. Give it the chance while changing course is still free.

## Anti-patterns

- **Adjectives instead of specifics.** "Make it robust / clean / production-ready" means nothing. "Returns 429 with Retry-After" means something.
- **Stacking requests.** One prompt, one outcome. Bundled asks produce bundled diffs, and bundled diffs don't get read.
- **Answering your own open question.** If you don't know whether the counter should be shared, say so and ask. Don't guess in the prompt and inherit your own guess as a requirement.
