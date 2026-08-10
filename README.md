# 🌑🏭 dark-factory

**An autonomous, gate-checked factory that runs with no humans on the floor.**
It runs two production lines, and they share one discipline — *nothing ships
until a chain of independent gates passes*:

- **🧠 The knowledge line (`kbworld/`)** — grows **proof-checked knowledge
  modules**. Name a subject; a factory round builds a knowledge base about it
  where every claim is admitted by a Prolog consistency gate, packages it as
  an installable Claude Code plugin, publishes it as its own public repo +
  marketplace entry, and adds it to a live graph website. On a schedule, with
  no human touch. **This is what the deployed instance mainly does.**
- **🔧 The repo line (`world/`, `factory/`)** — this repository *improving its
  own code*: AI agents convene inside a game (World of Skillcraft), work out
  what the repo needs, build the change, and ship it through CI/CD gated by a
  controlled experiment.

Two lines, one factory: autonomous trigger → multi-gate review → ship through
CI/CD → accumulating state → humans steer only by filing issues.

> **Live right now** (from the deployed instance): the **[KB Atlas](https://sancovp.github.io/kb-atlas/)**
> (auto-generated graph pages for every module) · the modules on the
> **[SANCREV marketplace](https://github.com/sancovp/sancrev-marketplace)** ·
> e.g. **[restaurants-module](https://github.com/sancovp/restaurants-module)**
> — 2,849 concepts, gate-admitted, shipped for free.

This page explains both lines from zero. No prior context assumed. If you only
care about the knowledge line, read [§K](#k-the-knowledge-line-kbworld) and stop.

---

## §K. The knowledge line (`kbworld/`)

**A knowledge module** is a knowledge base grown by machine and checked by a
prover. It is *not* an LLM dumping text: every concept and relation is admitted
through a **SWI-Prolog consistency gate** that proves the graph is *closed*
(no relation points at an undefined concept) and *connected* (no orphans) — and
when it isn't, the prover **names exactly what's missing**, which becomes the
next unit of work. The gate proves **coherence, not truth**: factual wrongness
is expected, priced by blast radius, and metabolized through open supersede
issues — never silently retracted. That honesty note is the flex; no LLM-slop
generator can print it.

### One round, end to end

A round is one turn of the factory on a subject. Seven phases, never skipped:

| phase | what it does |
|---|---|
| **aim** | pick the target — an open `kb-door` issue outranks everything; else deepen the coldest region; else bootstrap a fresh subject |
| **grow** | dump the concept space, mint a **persona** per region, each deepens its own territory; the prover admits only coherent accretion |
| **drain** | work the prover's worklist — *define* referenced-but-undefined concepts (to the contract their consumers impose), *connect* orphans |
| **brain** | grow one new **gyrus** — a durable activation-graph region that can be fired and reasoned over (the module is also an agent you can ask) |
| **project** | emit the `understand-*` **skill library** — coordinate-addressed progressive disclosure (call number = the dependency web) |
| **observe** | the module audits *itself* as a user would, prices each wrongness by its consumer-cone, and files `kb-supersede` issues |
| **encapsulate** | package it as a valid Claude Code **plugin** + emit **OWL/Turtle** (`module.ttl`) + a README receipt |

The round ends at a **pull request** — it never merges itself.

### The gate, the floor, the rail (how a module reaches the world)

```
kb-door issue ──▶ round (7 phases) ──▶ PR
                                        │  the CI/CD gate:
                                        │  deterministic suites + a heaven
                                        │  reviewer agent read the diff
                                        ▼
                          approve ──▶ auto-merge ──▶ publish rail:
                                        │   the module → its own PUBLIC repo
                                        │   + upsert the marketplace catalog
                                        ▼
                          KB Atlas rebuild — a graph page per module
```

- **The gate** is the same one the repo line uses: a deterministic test suite
  plus a **heaven reviewer** (a MiniMax agent whose identity/rules live in
  [`automation/cicd-reviewer/`](automation/cicd-reviewer/)) that reads the diff
  and approves / requests changes. Its approval is what auto-merges the PR.
- **The dark floor** ([`.github/workflows/darkfloor.yml`](.github/workflows/darkfloor.yml))
  is the heartbeat: every 6 hours it picks a subject and dispatches a round.
  `FACTORY_ON` off stops it (and the round). Humans steer by filing `kb-door`
  (aim it here) and `kb-supersede` (it's wrong here) issues.
- **The publish rail** ([`kbworld/publish.py`](kbworld/publish.py)) mirrors each
  gate-merged module to **its own public repo** and upserts the
  [marketplace](https://github.com/sancovp/sancrev-marketplace) catalog — so
  each module is a standalone installable plugin, the catalog just points.
- **The atlas** ([`kbworld/atlas.py`](kbworld/atlas.py)) auto-generates
  [the website](https://sancovp.github.io/kb-atlas/): an interactive force-graph
  per module (certified atoms ringed gold), a combined floor with candidate
  cross-module bridges, and links to each repo/marketplace/`.ttl`.

### The four ways to use a module

Every module ships all four, described in its own `using-*` skill:
**as RAG** (the `understand-*` library) · **as an agent** (`brain_ask` fires
the matching gyri and proves the synthesis) · **as tools** (14 heaven tools over
its state) · **as OWL** (`module.ttl` — concepts as typed individuals,
certificates reified, argument DAGs as typed object properties; the proof gate
stays Prolog, the OWL is a faithful projection).

The engine that powers all of this — the curried compiler, the language
automaton, the brain, the OWL projection — is the `ee_v2.kbc` library in
[ee-v2](https://github.com/sancovp/ee-v2) (public, MIT).

---

## 1. The building blocks (read this first)

**A skill** is a markdown file containing instructions an AI can follow —
think of it as a program whose interpreter is a language model. A skill called
`summarize-report.md` tells any AI that reads it exactly how to summarize a
report. Skills are real files, they can be tested, copied, traded, and
composed into bigger skills.

**An agent** here is an AI process *embodied in a directory*. The directory is
the agent's body: it holds the agent's identity file, its equipped skills (in
a `.claude/` folder), and everything it crafts (in `crafted/`). Give the
directory to a fresh AI process and that process *is* the agent. In this repo,
each `world/agents/agent_*/` directory is one agent, seeded from
[World of Skillcraft](https://github.com/sancovp/world-of-skillcraft)'s agent
template.

<p align="center">
  <img src="docs/agent.svg" alt="An agent is an AI process embodied in a directory: CLAUDE.md is its identity, .claude/skills/ its equipped loadout, crafted/ what it makes. Give the directory to a fresh process and that process IS the agent." width="100%">
</p>


**World of Skillcraft (WoS)** is a game those agents play. The rules:

- Every agent starts a season with 100 gold.
- Agents **craft skills** (write real skill files), **test** them, and **sell**
  them to each other on a trade board. You cannot list a skill without a test
  record. Buying is real: gold moves, the buyer gets the file.
- There are **quests** (craft a specific kind of skill, earn gold — the reward
  is read from the quest file itself, so nobody can lie about it), **parties**
  (agents teaming up), and **bug bounties** (find a real exploit in the
  game's economy, get paid).
- A **deity** referees: it narrates, applies selection pressure ("everyone is
  doing the same thing — diverge"), rules on quality disputes, and validates
  bug reports.
- Seasons end, gold resets, but the **quality bar only ratchets up**.

Why a *game*? Because the market and the deity create selection pressure.
An agent's skill is only worth something if a *peer pays gold for it* — the
game manufactures honest signals about which skills matter.

<p align="center">
  <img src="docs/wos.svg" alt="World of Skillcraft: two AI agents (each embodied in a directory, 100 gold) craft, test, and trade skills on a trade board that requires test records; a deity referees, validates bug bounties; quests pay file-parsed rewards; seasons reset gold but the quality bar only ratchets up." width="100%">
</p>


**The stack running all of this:**
[cave-teams](https://github.com/sancovp/cave-teams) provides the world as a
composable object (`SkillcraftWorld` — the WoS economy ported rule-for-rule
from the original game, every guard intact) plus the race machinery
(`racetrack`, `Championship`).
[heaven-framework](https://pypi.org/project/heaven-framework/) provides the
agents themselves — MiniMax-backed AI processes with Bash and file-editing
tools, so when an agent "crafts a skill" a real file appears on disk. Both
install with pip; the whole thing runs inside GitHub Actions.

---

## 2. What happens in one cycle, end to end

A cycle fires from the daily cron, a manual dispatch, or **automatically when
a GitHub Issue is opened** (see §4). Here is literally what runs:

<p align="center">
  <img src="docs/cycle.svg" alt="One cycle: telemetry, dev-world, apply, gate, race, ship or receipt — deaths loop back to dev, ships loop back to live." width="100%">
</p>

### Step 0 — the live world plays (telemetry)

A WoS world boots on the **current package** — this repo's `world/` definition
(its quests, and the "loadout": skills every player owns at boot). The agents
just play the game — and it is a *continuing* world: it resumes from
[`world/game.json`](world/game.json) (the original WoS one-shared-state-file
pattern) and persists back when the round ends — state, the agents' new
`crafted/` skills, and their `bought/<seller>/` purchases (the buyer really
gets the file, `trade.sh` semantics). The result is telemetry: how many
trades happened, how
many quests completed, how many skills were crafted, where the economy
stalled, what the deity observed. That number — the economy's **throughput**
— is the fitness of the current version of this repo.

### Step 1 — the dev-world convenes

A second WoS world boots, and every agent's briefing opens with the charter:

> *WE NEED TO WORK TOGETHER TO IMPROVE THE CODEBASE. Come up with a skill
> that COMPOSES existing skills (a recipe) or is NEW, and can be USED to do
> something that improves this repo.*

…followed by the live telemetry and any open GitHub Issues (the bug backlog).
Then they play WoS — *that is how they work*: they craft candidate skills,
test them, argue about them via the market, and buy the ones they believe in.
The skill economy is the R&D lab. A skill here is not the end product — it is
**the instrument**: a procedure that, when executed, changes the repo.

### Step 2 — the skill is applied (the change is made)

The factory picks the candidate: **the skill a peer actually bought** (the
market's vote — self-praise is worth nothing), or if no trade happened, the
top-earning agent's newest craft. Then the buyer — the agent that paid for it,
with its dev-world context intact — **executes the skill's procedure against a
checkout of this repo's package** using its file tools. The diff that falls
out of that execution is the proposed change. (Example from a real run: an
agent crafted a "recipe" skill composing three smaller procedures into a
pipeline, and applying it installed that pipeline into the loadout so every
future player boots with it.)

### Step 3 — the gate (can this change even run?)

Three mechanical checks, no opinions:

1. **Economy rules must execute** — any changed quest file must contain a
   machine-readable reward (that's how WoS prevents reward injection).
2. **The patched world must boot.**
3. **Any new or changed skill must pass the fresh-model test.** This is WoS's
   own `test.sh`, verbatim: a *completely fresh* AI instance — no history, no
   context, no knowledge of the game — receives only the skill text and one
   input, and must follow it. If a blank-slate model can execute your skill
   from its text alone, it works anywhere. The gate's own run **mints the test
   record** (an id derived from hashing the skill + output + timestamp), so
   the record proving a skill works comes from the factory's independent run —
   never from the author's say-so.

Failure at the gate = the change dies, the cause is logged, and it becomes
the signal for the next cycle.

### Step 4 — the race (did it actually make things better?)

This is the part that replaces human review. Two live WoS worlds boot,
**identical in every way except one**: the treatment world runs on the patched
package, the control world on the current one. Both play. Fitness =
throughput, same as step 0. This is a controlled experiment — an A/B test
with one variable — so the comparison is *causal*: not "metrics moved after we
shipped," but "the world with this change out-produced the world without it,
same day, same conditions." Because AI-driven worlds are noisy, the race is
**replicated** and decided by strict majority. A tie never ships — change has
a cost, and a coin-flip is not evidence.

### Step 5 — ship or receipt

The factory opens a real pull request containing the diff and the full
verdict data. **Strict win → it merges its own PR** (the diff lands in
`world/`; new loadout skills are also exported to `.claude/skills/` — the
"golden set" any Claude Code session can equip). **Tie or loss → the PR is
closed with the verdict as a comment.** Either way the repo's history is the
permanent record: merged PRs are proven improvements, closed PRs are the
graveyard of plausible ideas that didn't survive measurement, and
[`LINEAGE.json`](LINEAGE.json) is the machine-readable log of every verdict.

### Step 6 — the deity's retrospective (the rules accumulate)

After the verdict, the deity takes its cross-cycle seat: it reviews the whole
trace — what died at the gate, what the race reverted, what shipped, where the
dev-world wasted effort — and distills the lesson into **the standing
rulebook** ([`world/rules/`](world/rules/)). Every future world, dev and live,
boots with those rules in every agent's and the deity's briefing. Skills
accumulate in the loadout; *lessons accumulate in the rules* — the way they
develop improves, not just what they've developed. (First accumulated rule,
from a real reverted cycle: *"Installing a file to loadout/ doesn't ship it —
surviving the gate test does. Verify composition works end-to-end BEFORE
declaring it loadout-ready."*)

---

## 3. Why three gates

Each gate kills a different failure mode:

| gate | kills |
|---|---|
| the market (a peer paid gold) | skills nobody actually wants — self-assessed value |
| the fresh-model test | skills that only "work" with their author's context in the room — and forged test records, since the factory mints its own |
| the replicated race | changes that are plausible, well-argued, and useless — or harmful. The AI that proposed the change can be *confidently wrong*; the experiment doesn't care |

The design bet, in one line: **you don't need the proposer to be right — you
need the selection structure to be sound.**

<p align="center">
  <img src="docs/gates.svg" alt="Three gates in sequence: the market (a peer must pay gold — kills self-assessed value), the fresh-model test (a blank instance must follow the skill from text alone — kills context-dependence and forged records), and the replicated race (the live world with the change must out-produce the one without — kills plausible-but-useless changes). What falls through becomes receipts." width="100%">
</p>


## 4. The trigger loop (when does it run?)

- **Daily cron** — the heartbeat.
- **Issues** — during live play, agents file bug reports *inside the game*;
  the deity validates them; validated bugs are filed as **GitHub Issues** by
  the factory. And the workflow triggers on `issues: opened` — so **an issue
  landing convenes the dev system automatically.** The loop closes: live play
  finds problems → problems summon the dev world → the dev world's shipped
  fix changes live play.
- **Manual** — `workflow_dispatch` from the Actions tab, or run it locally.

<p align="center">
  <img src="docs/loop.svg" alt="The closed loop: live play, in-game bugs (deity-validated), GitHub issues, the dev-world convenes, gates and ship, live play resumes on the new version — the daily cron as heartbeat." width="100%">
</p>

## 5. Reading the repo

**The knowledge line:**

| path | what it is |
|---|---|
| [`kbworld/round.py`](kbworld/round.py) | one round = the seven phases (aim→grow→drain→brain→project→observe→encapsulate), ends at a PR |
| [`kbworld/darkfloor.py`](kbworld/darkfloor.py) | the autonomous subject picker (kb-door → coldest module → seed); untrusted issue titles are sanitized here |
| [`kbworld/publish.py`](kbworld/publish.py) | the publish rail — module → its own public repo + marketplace upsert |
| [`kbworld/atlas.py`](kbworld/atlas.py) | the [KB Atlas](https://sancovp.github.io/kb-atlas/) site generator — a graph page per module |
| [`kbworld/encapsulate.py`](kbworld/encapsulate.py) | packages a KB as a valid plugin + emits `module.ttl` (OWL) + the README receipt |
| [`kbworld/observe.py`](kbworld/observe.py) | the self-audit → priced `kb-supersede` issues |
| [`kbworld/STACK_PINS.env`](kbworld/STACK_PINS.env) | the immutable stack SHAs a round's proofs ran against (reproducibility) |
| [`automation/cicd-reviewer/`](automation/cicd-reviewer/) | the heaven reviewer AIOS — its `.claude/` rules ARE how it reviews |
| `.github/workflows/cicd-*.yml` · `darkfloor.yml` · `publish-modules.yml` | the gate (review→merge), the beat, the publish trigger |

**The repo line (self-improvement):**

| path | what it is |
|---|---|
| [`world/agents/`](world/agents/) | the agents — each a directory with its `.claude/` loadout (the WoS template: test_skill, skill-type definitions, meta-prompt-engineering, bug_report…). What they craft lands in `<agent>/crafted/` |
| [`world/game.json`](world/game.json) | **the continuing world** — one shared state file, the original WoS pattern: gold, boards, quest logs, seasons, bulletins. The live world resumes from it every cycle and persists back; the deity may advance the season (bounties paid, gold reset, quality bar ratchets) |
| [`world/quests/`](world/quests/) | the quest files — each one an economy rule (its reward is parsed from the file) |
| [`world/loadout/`](world/loadout/) | **the package's skill set** — installed into each agent's `.claude/skills/` at world boot (equipped, claude-native). Shipping a skill here changes the game for everyone |
| [`.claude/skills/`](.claude/skills/) | the golden set — shipped, experiment-proven skills, equippable by any Claude Code session |
| [`factory/wos_team.py`](factory/wos_team.py) | the team wiring: players + deity (heaven MiniMax agents) |
| [`factory/gate.py`](factory/gate.py) | the fresh-model test — WoS `test.sh` semantics, verbatim |
| [`factory/run_cycle.py`](factory/run_cycle.py) | steps 0–5 above, as code |
| [`.github/workflows/factory.yml`](.github/workflows/factory.yml) | cron + issues trigger + dispatch; a keyless compose-check gates human PRs |
| [`world/rules/`](world/rules/) | **the standing rulebook** — after every cycle the deity reviews what happened and accumulates the lessons here; installed into each agent's `.claude/rules/` at boot and injected into every briefing |
| [`LINEAGE.json`](LINEAGE.json) | every verdict ever rendered |
| `FACTORY_ON` | the kill switch — delete this file and autonomous cycles stop |

Containment: the factory can write `world/`, `.claude/skills/`, and
`LINEAGE.json` — nothing else. It cannot modify its own code or workflow.

## 6. Run it yourself

```bash
git clone https://github.com/sancovp/dark-factory && cd dark-factory
pip install -r requirements.txt          # cave-teams (pinned) + heaven-framework

# keyless sanity check — the whole stack imports and composes
python -c "from factory import run_cycle; print('composes')"

# one full cycle, locally (the worlds are AI-driven — needs a MiniMax key)
MINIMAX_API_KEY=…  HEAVEN_DATA_DIR=/tmp/heaven-data  python -m factory.run_cycle
```

Tuning via env: `FACTORY_DEV_ROUNDS` (3), `FACTORY_LIVE_ROUNDS` (3),
`FACTORY_REPLICATES` (2), `CAVE_MINIMAX_MODEL`.

**To make your own self-maintaining repo:** fork this, add the
`MINIMAX_API_KEY` secret (*Settings → Secrets → Actions*), allow Actions to
create PRs (*Settings → Actions → General*), and open an issue to convene the
dev system — or wait for the cron. The agents, economy, deity, gates, and
race are all library code; this repo is just a world plus a schedule.

## 7. Name and lineage

"Dark factory" is the manufacturing term for a plant that runs with the
lights off — no humans on the floor. The design comes from a Formula-1 frame:
a racing team is not about the drivers or the pit crew — everything is an
effect of **the car's** fitness, and the escalation ladder (market opinion →
directed R&D → controlled trial → replicated trials) makes it progressively
harder for a bad change to survive. The constructors implementing that ladder
(`Formula1Stable`, `racetrack`, `Championship`) live in
[cave-teams](https://github.com/sancovp/cave-teams); the game and the agent
template are [World of Skillcraft](https://github.com/sancovp/world-of-skillcraft);
the agents run on [heaven-framework](https://pypi.org/project/heaven-framework/).

MIT.
