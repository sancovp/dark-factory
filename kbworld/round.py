"""round.py — ONE TURN OF THE KB FACTORY (the reified full flow, §22).

Orchestration is REAL here; phase bodies marked TODO(fill) get implemented
per .claude/rules/kbworld.md. Steps are never skipped: a phase that cannot
run raises, and the round halts fail-closed with the report so far."""
from __future__ import annotations

import argparse
import asyncio
import json
import time
from pathlib import Path

from .host import FactoryKbcHost

HERE = Path(__file__).resolve().parent


async def phase_aim(host, cmds) -> list:
    """a. AIM — doors. Maintainer issues labeled `kb-door` FIRST (gh CLI;
    untrusted-issue gate applies); else worklist proposes: 1 warm region
    (activation) + 1 cold (unvisited — exploration pressure, UCB-style).
    TODO(fill §22.2): gh issue list + worklist read + explore pick."""
    raise NotImplementedError("fill: kbworld rule step 1")


async def phase_grow(host, kb, brain, doors) -> dict:
    """b. GROW — ee_v2.kbc.specialize.specialization_round over the doors
    (mint personas → deepen → prover admits). TODO(fill): thread budget."""
    raise NotImplementedError("fill: kbworld rule step 2")


async def phase_drain(host, kb, budget: int) -> dict:
    """c. DRAIN — work_session over define/connect/reconcile under the
    calendar budget. TODO(fill)."""
    raise NotImplementedError("fill: kbworld rule step 3")


async def phase_brain(host, kb, brain, grown: dict) -> dict:
    """d. BRAIN — grow gyri for strong new regions; teach on admitted
    (the prover is the teacher — rung-4). TODO(fill)."""
    raise NotImplementedError("fill: kbworld rule step 4")


async def phase_project(host, kb) -> dict:
    """e. PROJECT — project_library into kbworld/state/libraries/, in-repo.
    TODO(fill)."""
    raise NotImplementedError("fill: kbworld rule step 5")


async def phase_observe(host, kb, brain) -> dict:
    """f. OBSERVE — see observe.py: read own regions in use, note wrongness,
    file supersede-issues. TODO(fill)."""
    from .observe import observation_pass
    return await observation_pass(host, kb, brain)


async def phase_encapsulate(host, kb) -> dict:
    """g. ENCAPSULATE — see encapsulate.py: emit using-{subject} SKILL +
    plugin manifest (one universal way). TODO(fill)."""
    from .encapsulate import emit_module_skill
    return emit_module_skill(kb, HERE / "state")


async def run_round(subject: str, grade1: bool = True) -> dict:
    """THE ROUND. grade1=True → no auto-PR-merge; the round commits its
    delta on a branch and opens the PR for human eyes (reuse factory
    _publish/PR helpers — TODO(fill): import from factory.run_cycle)."""
    t0 = time.time()
    host = FactoryKbcHost()
    report = {"subject": subject, "phases": {}, "grade1": grade1}
    # TODO(fill): kb = KB(subject, state/kbs/<slug>).load(); brain = KbcBrain(...)
    kb = brain = None
    for name, phase, args in [
        ("aim", phase_aim, (host, None)),
        ("grow", phase_grow, (host, kb, brain, None)),
        ("drain", phase_drain, (host, kb, 100)),
        ("brain", phase_brain, (host, kb, brain, None)),
        ("project", phase_project, (host, kb)),
        ("observe", phase_observe, (host, kb, brain)),
        ("encapsulate", phase_encapsulate, (host, kb)),
    ]:
        report["phases"][name] = await phase(*args)   # never skipped (§22.3)
    report["secs"] = round(time.time() - t0, 1)
    out = HERE / "state" / f"round_{int(t0)}.json"
    out.write_text(json.dumps(report, indent=2))
    # TODO(fill): branch + commit state delta + open PR w/ report as body
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("subject")
    ap.add_argument("--grade1", action="store_true", default=True)
    a = ap.parse_args()
    print(json.dumps(asyncio.run(run_round(a.subject, a.grade1)), indent=2))
