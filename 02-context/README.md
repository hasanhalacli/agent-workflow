# 02 — Context

Companion to **[Prompting Is Context Engineering](https://www.halacli.com/25_2026-08-15-prompting-is-context-engineering.html)**.

Prompting is 10% phrasing and 90% deciding what the model can see. The pairs in [`prompt-pairs.md`](prompt-pairs.md) show the same task prompted badly and well, and what each produced.

## The four feeding rules

1. **Point at files, never paraphrase them.** `@app/auth.py` beats your memory of it. Paraphrase loses the detail that key comparison uses `secrets.compare_digest` — and the agent reintroduces a timing side-channel.
2. **The failing test is the best prompt.** If the requirement fits in an assertion, write the assertion. The spec becomes executable and the agent can no longer grade its own homework.
3. **Show the pattern to copy.** Agents are excellent mimics. Name the exemplar ("follow how `require_api_key` is wired") or inherit an invented pattern.
4. **Negative constraints are context.** "Don't add a dependency. Don't touch auth. Don't reformat files you only read."

## The withholding rules

- **Relevance beats volume.** Could you justify every file in the prompt to a colleague? If not, it's noise competing with signal.
- **Start fresh more often than feels natural.** When the agent reintroduces something you rejected an hour ago, the transcript — not the model — is the problem.
- **Don't hand it your uncertainty as a requirement.** Guess "use Redis" in the prompt and you'll review an implementation of a decision nobody made.
