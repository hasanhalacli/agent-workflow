# Feature request

> add rate limiting to the API

---

That's it. That's the whole ticket.

This is not a strawman — it's the shape of most real tickets, and it's the input the series starts from. Part one is about what happens when you hand this to an agent unchanged, and what to do instead.

Five decisions are missing from that one line. An agent will make all five for you, silently, in about four seconds:

1. Rate limit **per what** — IP, API key, user, tenant?
2. **What limits**, and are they the same for every endpoint?
3. **In-process or shared** across replicas? (This one decides whether you acquire a new infrastructure dependency.)
4. What happens on breach — 429, queue, drop?
5. Does this apply to internal service-to-service calls too?

See [`../01-planning/`](../01-planning/) for the plan that answers them.
