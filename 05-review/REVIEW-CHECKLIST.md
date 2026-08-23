# Review checklist for agent-written changes

Copy into the PR or run down it live. Order is deliberate: read where the
incident lives first, while attention is fresh.

## 1. Shape (before opening any file)
- [ ] `git diff main --stat` — size, spread, and **what got deleted**
- [ ] Every touched file is in the plan's "files to touch" — extras are
      justified out loud or reverted (scope drift)

## 2. Dependencies
- [ ] `git diff main -- pyproject.toml uv.lock` (or package.json / lockfile)
- [ ] No new dependency without explicit approval
- [ ] No pin loosened to a range
- [ ] New package verified: registry entry AND matching source-repo release

## 3. Config, secrets, pipelines
- [ ] `git diff main -- '.env*' '**/settings*' '**/config*' '.github/**'`
- [ ] No credential patterns in any added line
- [ ] No CI gate weakened, no check removed

## 4. Trust boundaries
- [ ] `git diff main -- '**/auth*' '**/security*'`
- [ ] Removed lines read with MORE suspicion than added ones
      (silent weakening: relaxed validation, swallowed exceptions)

## 5. Feature code
- [ ] Any import/method you don't recognize → 30 seconds against the real
      docs (hallucinated APIs compile in prose and die at runtime)
- [ ] One unhappy path traced end-to-end by hand

## 6. Tests — last, with the right question
- [ ] "What do these tests NOT assert?"
- [ ] No assertion-free tests (`is not None`, `status in (200, 429)`)
- [ ] Break-the-code check: disable the core line, suite must go red
- [ ] Assertions describe behavior, not implementation

## 7. Run it
- [ ] The change demonstrated locally, by you, end to end
- [ ] "What I personally verified" filled in the PR — a claim you signed
