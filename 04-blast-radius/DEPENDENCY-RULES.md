# Dependency rules (the Ask layer)

```markdown
## Dependencies
- Pin exact versions. Never ranges. Lockfile is committed.
- No new dependency and no upgrade without my explicit approval.
- Before adding any package: verify it exists on the official
  registry AND has a matching release in its source repo.
```

## Why the verification line exists: hallucinated packages

Agents suggest plausible-sounding libraries that don't exist. Attackers
register those names on PyPI/npm preloaded with malware — the attack is
called **slopsquatting**. An agent that installs its own hallucination is
a supply-chain compromise you typed one prompt to get.

Mechanical version of the check: the
[`dependency-auditor`](../03-subagents/agents/dependency-auditor.md)
sub-agent — registry entry AND matching source-repo release, or reject.

## Why "no ranges"

A range (`>=`, `~=`, `^`) delegates your dependency choice to whoever
publishes next. With agents in the loop this gets worse: a range loosened
in a busy diff looks like housekeeping and reads as nothing in review.
This repo's open demo PR smuggles exactly that change — and the CI gate
catches it, because the gate doesn't get tired.
