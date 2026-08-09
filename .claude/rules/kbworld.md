# RULE — kbworld fill-out plan (scaffold 2026-08-10; design = aios-research/EE-NEUROSYMBOLIC-DESIGN.md §18–§23)

The scaffold is COMPLETE STRUCTURE, stub bodies. Fill in THIS order; each step
has a PASS criterion. Import everything from `ee_v2.kbc` (mount, specialize,
brain, projector, kb_tool, heaven_tools) — write NO parallel machinery.
Deity laws in `kbworld/deity_rules.md` bind every step. RULE 2 binds all
debugging: boundaries teach; never soften a gate; never drop repairable input.

1. **round.run_round state init** — KB(subject, state/kbs/<slug>).load() +
   KbcBrain(kb, state/brains/<slug>). PASS: two rounds on the same subject
   reuse state (dir is the memo).
2. **phase_aim** — gh issue list --label kb-door (maintainer-only; the
   untrusted-issue gate stands) → else derive_worklist + pick 1 warm
   (activation ranks) + 1 cold (region never deepened — read round history).
   PASS: deterministic test with a fake issue list + a scripted KB.
3. **phase_grow** — specialization_round(kb, doors, named_seat_factory,
   state/personas_out, brain). PASS: personas emitted under state/, atoms
   accreted, report captured.
4. **phase_drain** — work_session per bucket under budget. PASS: backlog
   shrinks or halts named.
5. **phase_brain** — brain.grow for new regions w/ degree ≥ threshold; teach
   on admitted only. PASS: amplitudes rise only for admitted regions.
6. **phase_observe (observe.py)** — gather round reports + events tail; one
   seat names concrete wrongness w/ atom ids; price each via
   relative_root(consumers); file kb-supersede issues via gh. PASS:
   deterministic test w/ scripted seat files N issues (mock gh).
7. **phase_encapsulate (encapsulate.py)** — render USING_SKILL_TEMPLATE from
   the KB; write state/plugin/skills/using-<slug>/SKILL.md + manifest.
   **READ sancovp/garage's marketplace/plugin manifest shape FIRST — do not
   invent the schema.** PASS: plugin dir validates against garage's format.
8. **PR mechanics** — reuse factory.run_cycle._publish pattern: branch
   kbworld/round-<ts>, commit state delta, PR body = round report JSON +
   basis + meter. grade1: NEVER auto-merge. PASS: dry-run locally with
   git plumbing mocked or a scratch branch.
9. **converter (in ee-v2)** — ee_v2/kbc/convert.py heaven_tools_to_skills:
   walk tool classes (name/description/args_schema.arguments) → SKILL.md per
   tool + one bundle skill w/ invocation recipe. PASS: generated skill for
   kb_work names its zero args and shows the python call.
10. **first live round** — workflow_dispatch on a SMALL subject, both humans
    watching (grade 1). PASS assertions: full report written, all 7 phases
    ran, PR opened not merged, spend within budget. Only after ≥3 clean
    supervised rounds may the deity PROPOSE calendar entries (a human merges).

CI note: runner gets NATIVE swipl (apt) — no emulation; verify heaven pip
pin + langchain coherence on first dispatch (fresh installs should be clean;
the container's lcshim2 was local history, not upstream).
