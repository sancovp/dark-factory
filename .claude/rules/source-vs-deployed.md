# Rule — source vs deployed (which repo you are in, and what runs where)

Two repos, one codebase, different jobs (Isaac's ruling 2026-08-10: "we don't
wanna be self-mod on the source — we fork it and enable it"):

- **`sancovp/dark-factory`** = THE SOURCE. Clean code line. Its `factory.yml`
  and `kb-round.yml` workflows are **disabled** — nothing runs here. Code
  changes are developed here.
- **`sancovp/dark-factory-live`** = THE DEPLOYED INSTANCE (this rule ships in
  both; check your remote). Experimental, self-modifying, **on**: the factory
  beat, kb rounds, and the standardized heaven CI/CD all run HERE.

## The CI/CD gate on the deployed repo (adapted from sra-git's standardized set)

```
push (non-main)      → cicd-pr-on-push      → reviewer MODE=pr opens the PR
PR opened/updated    → cicd-review-on-pr    → deterministic gate (kbworld
                                              suite, code-touching PRs only)
                                              → heaven reviewer MODE=review
                                              → --approve / --request-changes
review == approved   → cicd-merge-on-approval → clean merge only; conflicts
                                              left open; cicd-rules/* EXCLUDED
                                              (maintainer-merge only)
weekly               → cicd-rule-harvest     → reviewer distills its own rules
```

The reviewer = `automation/cicd-reviewer/` (vendored 2026-08-10 from
`sanctuary-revolution-alpha/automation/cicd-reviewer` — re-sync from there
when the monorepo's copy changes; run direct on the runner because this
repo's tokens can't pull the private ghcr image). Its identity/rules/skills
live in `cicd_aios/.claude/` — edit THOSE to change how it reviews.

## Sync direction

Code improvements proven on the deployed line get PR'd back to SOURCE by a
human decision, never automatically. State (`kbworld/state/`, `LINEAGE.json`,
`world/`) NEVER flows back to source — the deployed line's history IS the
experiment.
