# OM mission-control layer — HOW IT WAS DONE (⚠ STATUS: UNVERIFIED v1)

> **⚠ WE ARE NOT SURE THIS IS RIGHT YET.** Laid 2026-08-08 from the canon docs
> only — never yet validated against a running OM daemon. Everything below
> states exactly what was done and what must be verified before trusting it.
> The next agent working this repo (the devdir-set agent) owns validating and
> correcting it.

## The intent (Isaac)

Use **OnionMorph as Isaac's mission control**: run the OM daemon with its cwd
inside this repo → the factory renders as a *world of places* (OM's
dirs-are-places, DESIGN.md §20/§22) — chat embodies per-place; `game.json` /
`LINEAGE.json` / the PR graveyard are the live world state around you; filing
an issue from OM chat convenes the dev system (the `issues:` trigger). OM + a
human viewing the dark-factory *in world*.

## What was laid (v1, metadata-only — no art)

### 1. `.onionmorph` places — six dirs got `.onionmorph/onion/place_metadata.json`

| place dir | name | domain |
|---|---|---|
| `.` (repo root) | The Dark Factory | factory |
| `world/` | The World | world |
| `world/agents/agent_001/` | Chamber of agent_001 | agent |
| `world/agents/agent_002/` | Chamber of agent_002 | agent |
| `world/rules/` | The Deity's Library | rules |
| `.claude/skills/` | The Golden Vault | skills |

Shape used: `{name, desc, domain}` only — the documented fields from
DESIGN.md §22.1 ("`place_metadata.json` (`{name?, desc?, domain?, …}`)").
No `bg_img.*` yet (metadata-only places render per §22.1's and/or).

### 2. `.heaven/agents/` roster — three entries

`agent_001`, `agent_002`, `deity` as the **canonical nested shape** from
HEAVEN-DOTDIR-SPEC.md §3.1: `agents/{name}/{name}_config.py` containing
`agent_config = HeavenAgentConfig(...)` — copied field-for-field from the
spec's own `minimax_default` example. These are the **dispatch/Automations
roster** (who OM can talk to) — NOT the factory's runtime: the factory
constructs its own richer prompts in `factory/wos_team.py`; the roster stubs
must never replace them.

## The canon this was derived from (read before changing anything)

- `~/repo/onionmorph-src/HEAVEN-DOTDIR-SPEC.md` — `.heaven` = dir-relative
  context + agent ROSTER + skill POOL; §3.1 the on-disk agent shape.
- `~/repo/onionmorph-src/DESIGN.md` §22.0 — **the boundary ruling** (Isaac
  2026-07-01): a file is `.heaven` iff a heaven loader reads it; `.onionmorph`
  iff only the OM app renders it. §22.1 — the place mechanic (BUILT +
  live-verified in OM): nearest-ancestor walk from daemon cwd,
  `_place_assets()` reads `.onionmorph/onion/`.
- `~/repo/onionmorph-src/onionmorph/server.py` ~:197–206 — the actual reader.

## ⚠ What is NOT verified / known risks (the devdir agent's checklist)

1. **No OM daemon has been pointed at this repo.** Verify: `GET /api/place`
   resolves each place; chat embodiment switches on cwd change; metadata-only
   (imageless) places behave as §22.1 claims.
2. **`place_metadata.json` field expectations** — the `…` in the documented
   shape may imply fields OM wants that we omitted (e.g. `skilltree` lens).
3. **The D4 loader bug** (HEAVEN-DOTDIR-SPEC §3.1): nested `agent_config`
   loads via NEITHER `use_hermes` by-name branch — direct import only — until
   Isaac's fix lands in `heaven_base`. The roster may be invisible to
   by-name dispatch today.
4. **`.heaven` is a SPEC, partially built** — the roster/pool discovery
   (cwd ∪ `~/.heaven` union) may not be implemented in the OM build in use.
5. **`.cave` was NOT examined or laid** — its contract is unread; do not
   invent it. Read cave/cave-teams' actual loader first.
6. **HOST_ROOT jailing** (§22.1): the OM daemon's place walk is jailed —
   confirm the repo checkout lives under the daemon's HOST_ROOT.
7. The factory's path-guard (`factory/run_cycle.py:_guard`) deliberately
   CANNOT write `.onionmorph`/`.heaven` — the factory must never modify its
   own presentation/roster. Keep it that way.

## Propagation queue (AgentDir landed in cave-teams @ a018991, 2026-08-08)

The library now has the devdir as a class (`cave_teams.agentdir.AgentDir` +
`scaffold_agents`, with the REAL WoS `_template` vendored). Adopt it here:
1. replace `factory/run_cycle._seed_world`'s hand glue with `scaffold_agents`
   (+ `equip_skill`/`equip_rule` for loadout+rules install);
2. embody `WoSPlayer` runtimes via `AgentDir.embody()` (heaven carries the
   dir; claude_parity autoloads .claude) instead of prompt-carried paths;
3. re-pin requirements to cave-teams @ a018991 (or later);
4. the already-briefed swap: CI runs `python -m factory.world` (the one
   DarkFactoryWorld object) instead of the legacy run_cycle.
Vendored-template sync rule: `cave_teams/wos_template/` is a VERBATIM copy of
world-of-skillcraft `agents/_template` — when the origin changes, re-vendor;
never fork the copy.

## Handoff

v1 (this layer + the factory itself) was built in the CEO session of
2026-08-07/08. **The devdir-set agent takes over dark-factory code work from
here** — start with the checklist above; correct this rule as findings land
(it is the map, keep it true).
