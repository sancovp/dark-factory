# 🌑🏭 dark-factory

> **World of Skillcraft improving World of Skillcraft — a game economy that
> develops its own skills, gated by a fresh-model test and a controlled trial
> between live worlds. Only proven skills enter the canon.**

This is [cave-teams](https://github.com/sancovp/cave-teams) acting the
dark-factory way. Everything running here is the real stack:
[World of Skillcraft](https://github.com/sancovp/world-of-skillcraft)'s agent
template (each agent is a directory with its full `.claude` loadout),
cave-teams' `SkillcraftWorld` (the WoS economy as a composable game world,
ported verb-for-verb from `execute.sh`), and
[HEAVEN](https://pypi.org/project/heaven-framework/) MiniMax agents in every
seat — tooled players that write real files, a deity adjudicator, and a fresh
test instance. All of it driven by a scheduled GitHub Action.

## One cycle

```
1. DEV-WORLD    a real SkillcraftWorld plays: MiniMax players (Bash + file
                tools, embodied in their agent dirs) craft real Claude Code
                skills, test them, TRADE them, do quests, audit for exploits;
                a deity narrates, applies selection pressure, validates bugs.

2. HARVEST      the candidate = the last skill somebody BOUGHT. A peer paid
                gold for it — the market gate. Self-praise is worth nothing.

3. GATE         WoS test_skill/test.sh, verbatim semantics: a FRESH instance
                (zero context) receives only the skill text + a test input
                and must follow it. Its run mints the independent test
                record. No output ⇒ dead.

4. RACETRACK    two LIVE SkillcraftWorlds, identical, one variable: in the
                treatment world every player OWNS the candidate skill.
                Fitness = the live economy's throughput (trades + quests +
                crafts). Replicated, strict-majority — live worlds are noisy.

5. SHIP         a causal win ⇒ the skill enters the canon: the world state
                and .claude/skills/<name>/ (golden, equippable), via a PR the
                factory merges itself. Anything else ⇒ the PR closes as a
                public receipt.
```

The repo's history is the lineage: merged `[SHIP]` PRs are skills that
provably made the live game better; closed PRs are the graveyard, verdicts
attached; [`LINEAGE.json`](LINEAGE.json) is the machine-readable record.

## Layout

| path | what |
|---|---|
| [`world/agents/`](world/agents/) | the agents — each dir seeded from WoS's `_template` with its full `.claude` loadout (test_skill, execute_in_game, skill_types, meta-PE, …). Crafted skills land in `<agent>/crafted/` with `.tests/` records |
| [`world/quests/`](world/quests/) | canonical quest files (rewards are grepped from these — players can't inject a reward) |
| [`.claude/skills/`](.claude/skills/) | **the golden set** — shipped, causally-proven skills, equippable by any Claude Code session |
| [`factory/wos_team.py`](factory/wos_team.py) | the team wiring, ported from cave-teams' live run (players + deity on HEAVEN MiniMax) |
| [`factory/gate.py`](factory/gate.py) | WoS `test.sh` as the factory's independent mint (same prompt, same record, same hash id) |
| [`factory/run_cycle.py`](factory/run_cycle.py) | the composition above + PR mechanics, path-guarded to `world/`, `.claude/skills/`, `LINEAGE.json` |
| [`.github/workflows/factory.yml`](.github/workflows/factory.yml) | daily cron + dispatch; keyless compose-check on PRs |
| `FACTORY_ON` | kill switch — delete to pause |

## Run it

```bash
pip install -r requirements.txt        # cave-teams (pinned) + heaven-framework

# keyless: the whole stack imports and composes
python -c "from factory import run_cycle; print('composes')"

# one real cycle (LLM worlds — needs the key)
MINIMAX_API_KEY=… HEAVEN_DATA_DIR=/tmp/heaven-data python -m factory.run_cycle
```

Tuning (env): `FACTORY_DEV_ROUNDS` (default 3), `FACTORY_LIVE_ROUNDS` (3),
`FACTORY_REPLICATES` (2), `CAVE_MINIMAX_MODEL`.

To run your own: fork, set the `MINIMAX_API_KEY` Actions secret, allow Actions
to create PRs (*Settings → Actions → General*), and the daily cron does the
rest. The agents, the economy, the deity, the gate are all library code —
this repo is just the world state plus the schedule.

## Why it's built this way

- **The market harvests, the gate mints, the race decides.** A skill must be
  peer-bought (someone paid gold), fresh-model-executable (a blank instance
  can follow it from its text alone), and **causally useful** (live worlds
  with it out-produce live worlds without it) before it touches the canon.
  Three independent gates; none of them is anyone's opinion of their own work.
- **The fresh-model test record is minted by the factory's own run**, not the
  crafter's claim — closing the forgeable-test loophole that WoS's own deity
  once filed as a bug.
- **Replicated verdicts** because LLM-driven worlds are stochastic: a lucky
  single race can lie in both directions; strict-majority replication
  converges.
- **Containment:** the runner writes `world/`, `.claude/skills/`, and
  `LINEAGE.json` — nothing else. It cannot modify its own code or workflow.

MIT.
