---
name: dark-factory
description: Run the dark factory — the self-developing repository program. Everything is driven by darkfactory.json at the repo root; the only things a human supplies are the API key (as the env var named in the config) and any config edits. Use this skill to run a cycle, stand up the factory on GitHub, or read its receipts.
---

# dark-factory — the program

The dark factory is ONE program parameterized by ONE config. There is no
setup procedure: `darkfactory.json` pipes every value (players, rounds,
replicates, model, charter, caps) to its slot when the program runs.

## What the human supplies

1. **The API key** — exported as the env var named by `api_key_env` in
   `darkfactory.json` (default `MINIMAX_API_KEY`). Locally: export it. On
   GitHub: `gh secret set MINIMAX_API_KEY`.
2. **Config edits** (optional) — open `darkfactory.json`, change values.
   That's the whole interface.

## Run a cycle locally

```bash
pip install -r requirements.txt
python -m factory.world              # THE top-level World: JobWorld(CEO,
                                     # dev_world, live_world) from the config
python -m factory.run_cycle          # legacy runner (same loop, procedural)
```

## Stand it up on GitHub (fully autonomous)

```bash
gh repo create <owner>/<name> --private --source . --push
gh secret set MINIMAX_API_KEY --repo <owner>/<name>
gh api -X PUT repos/<owner>/<name>/actions/permissions/workflow \
  -f default_workflow_permissions=write -F can_approve_pull_request_reviews=true
```

Done. The workflows in `.github/workflows/` (already part of the program)
run it: daily cron heartbeat, `issues: opened` convenes the dev system,
self-kick on world-bugs (governed by `max_runs_per_day`). Delete the
`FACTORY_ON` file to pause.

## Read the receipts

- merged `[SHIP]` PRs = causally-proven improvements; closed PRs = the graveyard
- `LINEAGE.json` = every verdict; `world/game.json` = the continuing world
- `world/rules/` = the deity's accumulated lessons; `.claude/skills/` = the
  golden (shipped) skills

## Architecture target (v2, per Isaac 2026-08-08)

JobWorld instance on top: CEO (leader-deity) + TWO departments, each an agent
whose runtime IS a SkillcraftWorld (`world_as_agent` — dev_world, live_world);
dev pushes PRs; GitHub CI/CD gates (fresh test + race as PR checks) and
deploys. See `.claude/rules/om-mission-control.md` + DARK-FACTORY-DESIGN §1–§2.
