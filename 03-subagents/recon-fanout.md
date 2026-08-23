# Parallel recon before implementing

Run before touching the rate limiter. Three independent, read-only tasks;
three clean contexts; the main session stays lean for the implementation.

```
Spawn three agents in parallel, read-only:
1. Map how @app/auth.py resolves API keys and where a "tier" would
   attach. Return: the function to extend + its callers.
2. Audit @tests/ conventions: fixtures, naming, how env vars are set.
   Return: a pattern summary I can hand to an implementer.
3. Search the repo and git history for any existing rate-limit or
   throttle logic. Return: file paths or "none".
```

Rules that make fan-outs safe:

- **Read-only tools for recon agents.** The `tools:` line is the
  permission boundary — an agent that cannot write cannot be
  prompt-injected into writing.
- **Evidence with file paths, not just conclusions.** Claims you can
  spot-check beat claims you must trust — cascaded summaries otherwise
  bury an early misreading three layers deep.
- **Disjoint targets.** Parallel agents never edit the same files.
  Read-only recon parallelizes perfectly; shared mutable state does not.
