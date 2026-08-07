# dark-factory

**A repository that develops itself — and only merges what it can causally prove.**

Every commit on `main` that touches `garage/` was proposed by an AI dev seat,
survived a quarantine gate, and **strictly beat the incumbent in a controlled
split test** (a real RCT, replicated when the judge is noisy). Everything that
*failed* is here too: the closed PRs are the graveyard of plausible-but-wrong
ideas, each with its measured verdict. The git history is the lineage.

```
  ┌────────────────────────────────────────────────────────────────────┐
  │            World() → Formula1Stable() → Racetrack() → Championship()│
  │  selection:  market      R&D loop          RCT         replicated   │
  │  rigor:     opinion  → directed evol. →  CAUSAL   →   meta-science  │
  └────────────────────────────────────────────────────────────────────┘
```

## What is actually running

A scheduled GitHub Action runs one **factory cycle** per car in `garage/`:

1. **ORDER 0 — telemetry.** The incumbent artifact runs against its task
   battery. Fitness = correct outputs. The dev seat is shown the **failing
   inputs only — never the expected outputs** (it can see *what* broke, it
   cannot memorize answers it hasn't earned).
2. **ORDER 1 — the stable.** The dev seat (an LLM, one conversation) proposes
   an edited artifact. The **quarantine gate** materializes the candidate in a
   sandbox and executes it for real; a candidate that cannot execute **dies**
   — the lineage is extinct, and the seat is re-asked with the cause of death.
   The gate is code. Its word is the only test record that exists.
3. **ORDER 2/3 — the race.** The survivor races the incumbent: identical
   conditions, one variable (the artifact). `code` cars use a deterministic
   sandboxed interpreter (zero-noise: one race suffices). `prose` cars are
   executed by a **fresh model per case** — a brand-new session that sees only
   the document and one input — which is stochastic, so the race is **replicated
   and decided by strict majority** (a lucky single race can lie in *both*
   directions; replication converges — see the receipts below).
4. **The verdict is the merge.** SHIP ⇒ the factory's own PR is merged with
   the tally in the title. REVERT/tie ⇒ the PR is closed with the verdict as a
   comment. Ties never ship — change has cost, and correlation never ships a
   car.

So: **`main` advances only on causal proof.** Not "the metrics moved after we
shipped" — *treatment beat control, same track, same day, N replicates.*

## How to read this repo

| where | what it is |
|---|---|
| `garage/<car>/skill.md` | the artifact — **the car**. The genome is the text |
| `garage/<car>/battery.json` | the task battery (the track). Held by the factory, not the car — a car cannot grade itself |
| `LINEAGE.json` | machine-readable history: every verdict, every death, every tally |
| closed PRs | proposals that died at the gate or lost the race — the receipts |
| merged PRs titled `[SHIP]` | causally-proven improvements, tally included |
| `factory/` | the runner + the two LLM seats (thin HTTP clients, toolless) |
| `.github/workflows/factory.yml` | the schedule. `FACTORY_ON` at repo root is the kill switch |

## The containment (stated as a feature)

The runner is **path-guarded**: it can write `garage/` and `LINEAGE.json`,
nothing else. It cannot modify its own code, the workflow, or this README —
no self-modifying CI. The dev seat is a toolless HTTP call: it receives
exactly the artifact + failing inputs, and returns text. The judge seat is a
fresh call per case with zero history. Autonomy here means *the loop runs
unattended*, not *the loop is unconstrained*.

Honest boundary: the batteries are public in this repo, so a tool-using agent
could read the answers. That is exactly why the seats are **not** agents. The
claim this repo makes is about the *selection structure*, not about seat
virtue — a confidently wrong proposal is expected input, and the machinery is
what stops it (it already has: see the lineage).

## Why the ladder (the one-paragraph theory)

Each order wraps the one below and optimizes it: a Stable is a map
*cars → cars*; a Racetrack judges those maps; a Championship judges the
judgments. In domain-theoretic terms the tower is `D_{n+1} = [D_n → D_n]` —
Scott's inverse-limit construction, whose limit `D∞ ≅ [D∞ → D∞]` is the space
where an element *is* a function on elements, including itself. The finite
proof-object for that math (embedding-projection pairs, exhaustively verified)
lives in [`sancovp/lfpoop`](https://github.com/sancovp/lfpoop)
(`lfpoop/dinfinity.py`). This repo is the same tower with the arrows running:
the artifact is the point, the seats are the functions, and the polymorphic
judge slot is the embedding.

The selection ladder is the point: **market opinion → directed evolution →
controlled trial → replicated trials.** The higher the order, the harder it is
for a bad change to survive. This factory runs at Championship order for noisy
judges and Racetrack order for deterministic ones — always at the order where
its verdicts are *sound*, never merely *plausible*.

## Receipts (from the build, before this repo went autonomous)

- **The gate kills:** a syntax-broken proposal died in quarantine
  ("artifact cannot execute"); a lineage-extinction, not an exception trace.
- **Ties never ship:** a cosmetic rewrite raced 4 vs 4 → REVERT.
- **A real fix ships:** the case-sensitivity fix raced 4 vs 6 → SHIP, strict.
- **The structure survives a wrong seat:** live, the dev seat once *doubled
  down* on a seeded bug — rewrote it more rigorously, confidently, plausibly.
  The RCT measured 3 vs 2 against it → REVERT. A correlational gate ships that
  PR; this one closed it.
- **Replication corrects single-race lies, both directions:** under an explicit
  noise table, one race wrong-reverted a truly-better change (unlucky 7v5) and
  wrong-shipped a worthless one (lucky 4v6); 7 replicates fixed both (4–3
  SHIP, 1–6 REVERT). `test_championship.py` in
  [`sancovp/cave-teams`](https://github.com/sancovp/cave-teams).

## Run your own

```bash
pip install -r requirements.txt
python -m factory.run_cycle --selftest      # keyless: proves the machinery
MINIMAX_API_KEY=… python -m factory.run_cycle    # one real cycle, locally
```

Fork it, put your own artifact + battery in `garage/`, set the
`MINIMAX_API_KEY` secret (or point `factory/seats.py` at any
Anthropic-compatible endpoint), and your repo develops itself too.

Built on [`cave-teams`](https://github.com/sancovp/cave-teams)
(`cave_teams.darkfactory` — the orders as constructors; `cave_teams.skillcar`
— the artifact car). MIT.
