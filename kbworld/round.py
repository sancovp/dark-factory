"""round.py — ONE TURN OF THE KB FACTORY (the reified full flow, §22).

Steps are never skipped; a phase that cannot run raises and the round halts
fail-closed with the report so far. All machinery imports from ee_v2.kbc.
Deps (gh, git, seats) are injectable → the whole round runs deterministically
in tests; defaults are the real thing."""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
import time
from collections import Counter
from pathlib import Path

from .host import FactoryKbcHost

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BOOTSTRAP_THRESHOLD = 30          # fewer concepts than this → dump first


def _slug(x: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", x.strip().lower()).strip("_")[:48]


class Deps:
    """Injectable boundary: gh + git + host. Tests script these."""

    def __init__(self, host=None, issue_lister=None, issue_filer=None,
                 pr_opener=None):
        self.host = host or FactoryKbcHost()
        self.issue_lister = issue_lister or self._gh_issues
        self.issue_filer = issue_filer or self._gh_file
        self.pr_opener = pr_opener or self._git_pr

    @staticmethod
    def _gh_issues(label: str) -> list:
        r = subprocess.run(["gh", "issue", "list", "--label", label,
                            "--state", "open", "--json", "title,number"],
                           capture_output=True, text=True, cwd=ROOT)
        return json.loads(r.stdout) if r.returncode == 0 and r.stdout else []

    @staticmethod
    def _gh_file(title: str, body: str, label: str) -> str:
        r = subprocess.run(["gh", "issue", "create", "--title", title,
                            "--body", body, "--label", label],
                           capture_output=True, text=True, cwd=ROOT)
        return r.stdout.strip()

    @staticmethod
    def _git_pr(branch: str, title: str, body: str, paths: list) -> str:
        """The factory's publish pattern, PR-flavored: branch, add state,
        commit, push -u, PR. grade1: NEVER merges."""
        def sh(*cmd):
            r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
            if r.returncode != 0:
                raise RuntimeError(f"{' '.join(cmd)}: "
                                   f"{(r.stderr or r.stdout)[-300:]}")
            return r.stdout.strip()
        sh("git", "checkout", "-b", branch)
        sh("git", "add", *[str(p) for p in paths])
        sh("git", "commit", "-m", title)
        sh("git", "push", "-u", "origin", branch)
        r = subprocess.run(["gh", "pr", "create", "--title", title,
                            "--body", body], capture_output=True, text=True,
                           cwd=ROOT)
        sh("git", "checkout", "main")
        return r.stdout.strip()


# ── the phases ───────────────────────────────────────────────────────────────
async def phase_aim(kb, brain, deps) -> dict:
    """a. AIM — doors human-first: open `kb-door` issues naming a concept
    outrank everything; else 1 WARM (highest activation among gyri) + 1 COLD
    (highest-degree concept with no gyrus — exploration pressure, §22.2)."""
    doors, source = [], "worklist"
    for issue in deps.issue_lister("kb-door"):
        for tok in re.findall(r"[a-z][a-z0-9_]+", issue["title"].lower()):
            if tok in kb.concepts and tok not in doors:
                doors.append(tok)
                source = "human"
    if not doors:
        deg = Counter()
        for s, t in kb.relations:
            deg[s] += 1
            deg[t] += 1
        regions = brain.regions()
        if regions:
            amp = {}
            for r_ in regions:
                q = brain.graph.conn.execute(
                    "MATCH (c:Concept {name: $n}) RETURN c.amplitude",
                    {"n": r_})
                amp[r_] = q.get_next()[0] if q.has_next() else 0.0
            doors.append(max(regions, key=lambda r_: amp[r_]))       # warm
        cold = sorted((c for c in kb.concepts
                       if c not in brain.regions() and deg[c] >= 2
                       and c not in doors), key=lambda c: -deg[c])
        while cold and len(doors) < 2:                               # cold
            doors.append(cold.pop(0))
    mode = ("bootstrap" if len(kb.concepts) < BOOTSTRAP_THRESHOLD
            else "deepen")
    return {"mode": mode, "doors": doors[:2], "source": source}


async def phase_grow(kb, brain, aim, deps) -> dict:
    """b. GROW — bootstrap: dump the subject's space first, re-aim on real
    content. Then ensure each door is a gyrus and run specialization_round
    over the doors (mint → deepen → prover admits; teach on admitted)."""
    from ee_v2.kbc.compiler import compile as kbc_compile
    from ee_v2.kbc.specialize import specialization_round
    out = {}
    if aim["mode"] == "bootstrap":
        v = await kbc_compile(kb, kb.subject, "dump", deps.host.seat_factory,
                              lib=_slug(kb.subject))
        out["bootstrap"] = {"concepts": v["n_concepts"],
                            "relations": v["n_relations"]}
        re_aim = await phase_aim(kb, brain, deps)
        aim["doors"], aim["source"] = re_aim["doors"], re_aim["source"]
    for door in aim["doors"]:
        if door not in brain.regions():
            await brain.grow(door, deps.host.named_seat_factory)
    if aim["doors"]:
        sp = await specialization_round(
            kb, aim["doors"], deps.host.named_seat_factory,
            deps.host.state_root / "personas_out", brain,
            log=lambda *_: None)
        out["specialize"] = {"basis_after": sp["basis_after"]["overlap"],
                             "new": [(r["region"], r["new_concepts"],
                                      r["new_relations"])
                                     for r in sp["rounds"]]}
    return out


async def phase_drain(kb, deps, budget: int) -> dict:
    """c. DRAIN — define first (saves relations), then connect, under the
    calendar budget."""
    from ee_v2.kbc.kb_tool import work_session
    r1 = await work_session(kb, deps.host.seat_factory, budget=budget,
                            do=("define",))
    r2 = await work_session(kb, deps.host.seat_factory,
                            budget=max(10, budget // 3), do=("connect",))
    return {"define": r1["did"], "connect": r2["did"], "after": r2["after"]}


async def phase_brain(kb, brain, deps) -> dict:
    """d. BRAIN — grow at most one NEW strong region from this round's
    accretion (degree ≥ 3, no gyrus yet). Teach already ran on admitted."""
    deg = Counter()
    for s, t in kb.relations:
        deg[s] += 1
        deg[t] += 1
    fresh = [c for c in kb.concepts
             if c not in brain.regions() and deg[c] >= 3]
    if not fresh:
        return {"grew": None}
    pick = max(fresh, key=lambda c: deg[c])
    await brain.grow(pick, deps.host.named_seat_factory)
    return {"grew": pick}


async def phase_project(kb, deps) -> dict:
    """e. PROJECT — the understand-* library, in-repo."""
    from ee_v2.kbc.projector import project_library
    out, n = project_library(kb, deps.host.state_root / "libraries"
                             / _slug(kb.subject))
    return {"library": str(out), "skills": n}


async def phase_observe(kb, brain, deps) -> dict:
    """f. OBSERVE — observation replaces control (§22.4)."""
    from .observe import observation_pass
    return await observation_pass(kb, brain, deps)


async def phase_encapsulate(kb, deps) -> dict:
    """g. ENCAPSULATE — the module ships its own manual (§23)."""
    from .encapsulate import emit_module_skill
    return emit_module_skill(kb, deps.host.state_root / "modules")


async def run_round(subject: str, grade1: bool = True, deps: Deps = None,
                    budget: int = 60, open_pr: bool = True) -> dict:
    deps = deps or Deps()
    host = deps.host
    t0 = time.time()
    from ee_v2.kbc import KB
    from ee_v2.kbc.brain import KbcBrain
    from ee_v2.kbc.kb_tool import derive_worklist
    from ee_v2.kbc.specialize import basis
    slug = _slug(subject)
    kb = KB(subject, host.state_root / "kbs" / slug).load()
    brain = KbcBrain(kb, host.state_root / "brains" / slug)
    wl0 = derive_worklist(kb)
    report = {"subject": subject, "grade1": grade1, "phases": {}}

    aim = await phase_aim(kb, brain, deps)
    report["phases"]["aim"] = aim
    report["phases"]["grow"] = await phase_grow(kb, brain, aim, deps)
    report["phases"]["drain"] = await phase_drain(kb, deps, budget)
    report["phases"]["brain"] = await phase_brain(kb, brain, deps)
    report["phases"]["project"] = await phase_project(kb, deps)
    report["phases"]["observe"] = await phase_observe(kb, brain, deps)
    report["phases"]["encapsulate"] = await phase_encapsulate(kb, deps)

    kb.save()
    wl1 = derive_worklist(kb)
    report["telemetry"] = {
        "kb": f"{wl1['n_concepts']}c/{wl1['n_relations']}r",
        "worklist": {"before": {"define": len(wl0["define"]),
                                "connect": len(wl0["connect"])},
                     "after": {"define": len(wl1["define"]),
                               "connect": len(wl1["connect"])}},
        "basis": (basis(kb, brain.regions())["overlap"]
                  if len(brain.regions()) >= 2 else None),
        "secs": round(time.time() - t0, 1)}
    stamp = int(t0)
    (host.state_root / f"round_{stamp}.json").write_text(
        json.dumps(report, indent=2))
    host.emit({"type": "kb_round", "subject": subject,
               "telemetry": report["telemetry"]})
    if open_pr:
        report["pr"] = deps.pr_opener(
            f"kbworld/round-{stamp}",
            f"kbworld round: {subject} ({report['telemetry']['kb']})",
            json.dumps(report["telemetry"], indent=2),
            [host.state_root])
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("subject")
    ap.add_argument("--grade1", action="store_true", default=True)
    ap.add_argument("--budget", type=int, default=60)
    ap.add_argument("--no-pr", action="store_true")
    a = ap.parse_args()
    rep = asyncio.run(run_round(a.subject, a.grade1, budget=a.budget,
                                open_pr=not a.no_pr))
    print(json.dumps(rep["telemetry"], indent=2))
