# dark-factory

**A repository that improves its own contents — and only merges a change it can
prove made things better.**

Here is the whole loop, concretely:

1. This repo contains small **skills** — a task spec, a document, and an
   implementation (see [`garage/`](garage/)). Each skill has a fixed **test
   battery**: inputs with known-correct outputs.
2. Once a day, a GitHub Action wakes up and asks an AI (the **dev seat**) to
   improve a skill. The AI is shown the skill and the inputs it currently
   fails — **never the expected outputs**, so it can't just memorize answers.
3. The proposal is executed for real in a sandbox (**the gate**). If it can't
   run — syntax error, crash, timeout — it's dead on arrival: rejected, and
   the AI is told why.
4. If it runs, it races the current version **head-to-head on the same
   battery** — a controlled A/B test. Strictly more correct outputs → the
   Action opens a PR and **merges it**, score in the title. Tie or worse → the
   PR is **closed** with the verdict as a comment.

That's it. No human review in the loop, and no vibes either: `main` only
moves when treatment beat control, same test, same day.

## It already happened

On the repo's first unattended run:

- [**PR #1**](../../pull/1) `[SHIP] extract-emails gen1: 4→6` — **merged by the
  bot.** The seeded skill had a case-sensitivity bug (scored 4/6). The AI was
  shown the two failing inputs, wrote the fix (`re.IGNORECASE` + normalize),
  it survived the sandbox, and won the race 6-to-4. Merged, no human.
- [**PR #2**](../../pull/2) `[REVERT] extract-emails-prose gen1: 3.0→3.0` —
  **closed by the bot.** A plausible rewrite of the prose skill passed the
  sandbox but tied its race (0 wins in 3 replicates). Ties don't merge.

One run, both outcomes: a real improvement shipped itself, and a
plausible-but-worthless change left a public receipt instead of landing.
Every closed PR in this repo is one of those receipts.

## Why bother

Most "AI improves the code" setups merge on plausibility: the diff looks
good, the tests still pass, ship it. The failure mode is confident nonsense —
and we've watched it happen: in one live run, the dev seat read a *bug* as
*intent* and rewrote it to be more rigorously wrong, with a clear
justification. It passed the sandbox. The A/B race measured it: worse than
the incumbent. Closed.

The claim this repo demonstrates is small but sharp: **you don't need the
proposer to be right; you need the selection structure to be sound.** Gate on
"does it run," then gate on "did it measurably beat what we had, under
controlled conditions." Everything else — including a wrong, confident AI —
is survivable input.

## Reading the repo

| where | what |
|---|---|
| `garage/<skill>/skill.md` | the artifact under evolution (the document/implementation) |
| `garage/<skill>/battery.json` | its test battery — held by the factory, not the skill: a thing can't grade itself |
| `garage/<skill>/car.json` | name, kind, generation counter |
| [`LINEAGE.json`](LINEAGE.json) | machine-readable history: every verdict, death, and score |
| merged PRs titled `[SHIP]` | proven improvements, score in the title |
| closed PRs | proposals that died in the sandbox or lost the race |
| [`factory/`](factory/) | the runner + the two AI seats (plain HTTP calls, no agent framework) |
| [`.github/workflows/factory.yml`](.github/workflows/factory.yml) | the daily schedule; delete `FACTORY_ON` to pause |

Two kinds of skill, two kinds of judge:

- **`code` skills** carry a fenced ```python block. The judge is a sandboxed
  interpreter — deterministic, so one race decides.
- **`prose` skills** are pure instructions. The judge is a **fresh AI session
  per test case** — it gets only the document and one input, and must follow
  the document literally. Fresh sessions are noisy, so the race is **replicated
  and decided by strict majority** (a lucky single race can lie in both
  directions; replication converges).

## The guardrails

- The runner is **path-guarded**: it can write `garage/` and `LINEAGE.json`,
  nothing else — it cannot edit its own code, the workflow, or this README.
  No self-modifying CI.
- The AI seats are toolless HTTP calls. They see exactly what the prompt
  contains (skill + failing inputs) and return text. They cannot browse the
  repo — which matters, because the batteries are public here. The claim is
  about the selection structure, not about trusting the model.
- A skill at max score is marked **saturated** in the lineage and skipped —
  no daily churn of pointless proposals against a solved problem.
- `python -m factory.run_cycle --selftest` proves the gate/race machinery
  keyless, on fixtures, in CI, on every PR.

## Run your own

```bash
pip install -r requirements.txt
python -m factory.run_cycle --selftest              # no key needed
MINIMAX_API_KEY=… python -m factory.run_cycle       # one real cycle, locally
```

Fork it, drop your own `skill.md` + `battery.json` in `garage/`, add a
`MINIMAX_API_KEY` Actions secret (or point `factory/seats.py` at any
Anthropic-compatible endpoint), and your repo develops itself too.

## The design, one level up (optional reading)

Internally the artifact is called the **car**, after a claim about Formula 1:
the sport is not about the drivers or the pit crew — everything is an effect
of the car's fitness. The escalation used here is a ladder:

```
market opinion → directed R&D → controlled trial (A/B) → replicated trials
```

Each rung makes it strictly harder for a bad change to survive; this factory
runs at the trial rungs, where verdicts are causal rather than plausible. The
constructors (`Formula1Stable` = propose+gate loop, `Racetrack` = the A/B
split, `Championship` = replicated splits) live in
[`cave-teams`](https://github.com/sancovp/cave-teams) and are ordinary
composable objects — the "improve the improver" tower they form is, for the
mathematically inclined, the function-space tower `D_{n+1} = [D_n → D_n]`
whose limit is Scott's `D∞ ≅ [D∞ → D∞]`; a finite, exhaustively-tested
proof-object for that construction lives in
[`sancovp/lfpoop`](https://github.com/sancovp/lfpoop) (`lfpoop/dinfinity.py`).
None of that is needed to use the factory. MIT.
