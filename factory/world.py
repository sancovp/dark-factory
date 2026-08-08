"""THE TOP-LEVEL WORLD — imported from the library, configured here, deployed.

    from cave_teams.darkfactory import DarkFactoryWorld

This module is ONLY wiring: darkfactory.json pipes into every param of the
one object; the two departments' runtimes ARE SkillcraftWorlds (the existing
run_cycle world helpers); the judge seat is the existing gate + race + ship
glue. Run:  python -m factory.world
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import tempfile
from pathlib import Path

from cave_teams.darkfactory import DarkFactoryWorld

from .config import CFG, CHARTER, PLAYERS
from . import run_cycle as rc


class LiveWorldRuntime:
    """.run(spec) → boot the CONTINUING live SkillcraftWorld (world/game.json),
    play, persist back, return telemetry. An agent that IS a world."""

    def __init__(self, ci: bool = False):
        self.ci = ci
        self.workdir = Path(tempfile.mkdtemp(prefix="df-live-"))

    async def run(self, spec: str):
        agents_root, quests, loadout = rc._seed_world(
            self.workdir, "live", rc.WORLD / "quests", rc.WORLD / "loadout")
        note = (f"You have these loadout skills EQUIPPED (in your "
                f".claude/skills/): {loadout} — apply them." if loadout else "")
        board, _ = await rc._run_world(agents_root, quests, rc.LIVE_ROUNDS,
                                       name="live", extra_note=note,
                                       start_board=rc._load_board())
        rc._persist_live(board, agents_root, self.ci)
        rc._file_world_bugs(board, self.ci)
        return rc._telemetry(board)


class DevWorldRuntime:
    """.run(spec) → convene the dev SkillcraftWorld under the charter+telemetry
    in `spec`, harvest the peer-valued skill, APPLY it to a package checkout,
    return {diff, change, patch_dir, implementer_dir}. An agent that IS a world."""

    def __init__(self):
        self.workdir = Path(tempfile.mkdtemp(prefix="df-dev-"))

    async def run(self, spec: str):
        # Department sends {"task_id","goal_id","description"}; the CEO put
        # the charter/telemetry JSON in the task DESCRIPTION (the real shape).
        outer = json.loads(spec) if spec.strip().startswith("{") else {}
        desc = outer.get("description", spec)
        try:
            task = json.loads(desc) if desc.strip().startswith("{") else {}
        except (ValueError, AttributeError):
            task = {}
        aim = (f"{task.get('charter', CHARTER)}\n"
               f"THE LIVE GAME'S TELEMETRY: {json.dumps(task.get('telemetry'))}."
               + (f"\nOPEN ISSUES: {json.dumps(task['issues'])}"
                  if task.get("issues") else ""))
        dev_agents, dev_quests, _ = rc._seed_world(
            self.workdir, "dev", rc.WORLD / "quests", rc.WORLD / "loadout")
        board, players = await rc._run_world(dev_agents, dev_quests,
                                             rc.DEV_ROUNDS, name="dev-world",
                                             extra_note=aim,
                                             bulletin=task.get("charter", CHARTER))
        # harvest the candidate skill (the market's vote, else top-gold newest)
        gold = {a: v.get("gold", 0) for a, v in board.get("agents", {}).items()}
        impl_name = max(gold, key=gold.get)
        trades = board.get("trade_history", [])
        skill_src = None
        if trades:
            sale = trades[-1]
            impl_name = sale["buyer"]
            skill_src = Path(dev_agents) / sale["seller"] / sale["skill_path"]
        else:
            crafted = sorted((Path(dev_agents) / impl_name / "crafted").glob("*.md"),
                             key=lambda p: p.stat().st_mtime)
            skill_src = crafted[-1] if crafted else None
        if skill_src is None or not skill_src.exists():
            return {"candidate": None, "why": "no skill crafted"}
        # APPLY: the implementer executes the skill against the package checkout
        patch = self.workdir / "patch"
        if patch.exists():
            shutil.rmtree(patch)
        shutil.copytree(rc.WORLD / "quests", patch / "quests")
        shutil.copytree(rc.WORLD / "loadout", patch / "loadout")
        out = await players[impl_name].rt.run(
            f"You are now the IMPLEMENTER — APPLY the skill to the target.\n\n"
            f"THE SKILL (your instrument — follow its procedure):\n"
            f"{skill_src.read_text()}\n\n"
            f"THE TARGET — the package checkout at {patch}: quests/ (each .md "
            f"a quest; its '## Reward N gold' line IS an economy rule) and "
            f"loadout/ (skills EVERY player owns at boot).\n"
            f"EXECUTE the skill's procedure against the target with your file "
            f"tools; you may install the skill itself as "
            f"loadout/{skill_src.stem}.md. Then reply ONLY JSON: "
            f'{{"change":"<one line>","files":["..."]}}')
        from .wos_team import last_json
        prop = last_json(out if isinstance(out, str) else str(out),
                         keys=("change", "files"), default={})
        return {"candidate": skill_src.stem,
                "change": str(prop.get("change", ""))[:200],
                "diff": rc._diff(patch), "patch_dir": str(patch),
                "implementer_dir": str(Path(dev_agents) / impl_name)}


def make_judge(ci: bool = False):
    """The CEO's review seat for the dev department: gate + race + ship —
    the existing glue, injected into the library object."""

    async def judge(candidate: dict, board: dict):
        if not candidate or not candidate.get("diff"):
            return {"verdict": "NO_DIFF"}
        patch = Path(candidate["patch_dir"])
        g = await rc._gate_package(patch, candidate["diff"],
                                   candidate["implementer_dir"])
        if not g["alive"]:
            return {"verdict": "DEAD_AT_GATE", "cause": g["cause"]}
        workdir = Path(tempfile.mkdtemp(prefix="df-race-"))
        kind = rc._live_kind(workdir, patch)
        from cave_teams.darkfactory import Championship, racetrack
        pair = ({"package": "current"}, {"package": "patched"})
        gate = (Championship(*pair, str(workdir), replicates=rc.REPLICATES,
                             kind=kind) if rc.REPLICATES > 1
                else racetrack(*pair, str(workdir), kind=kind))
        race = await gate.execute({})
        v = race.context["verdict"]
        out = {"verdict": v, "change": candidate.get("change", ""),
               "diff": candidate["diff"],
               "fitness_current": race.context["race"]["control"].get("fitness"),
               "fitness_patched": race.context["race"]["treatment"].get("fitness")}
        if "tally" in race.context:
            out["tally"] = race.context["tally"]
        now = __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc).isoformat(timespec="seconds")
        entry = {"at": now, **{k: out[k] for k in
                               ("verdict", "change", "diff",
                                "fitness_current", "fitness_patched")}}
        if ci:                              # the CI/CD half: PR per verdict
            branch = (f"factory/{rc._slug(out['change']) or 'change'}"[:60]
                      + f"-{now.replace(':', '').replace('+', 'Z')}")
            base = rc._sh("git", "rev-parse", "--abbrev-ref", "HEAD")
            rc._sh("git", "checkout", "-b", branch)
            # the candidate rides the PR for BOTH verdicts — a closed PR must
            # SHOW the rejected change (the receipt); merge keeps it, close
            # discards it with the branch
            for d in candidate["diff"]:
                src = patch / d["file"]
                dst = rc._guard(rc.WORLD / d["file"])
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(src, dst)
            rc._sh("git", "add", "-A")
            rc._sh("git", "commit", "-m",
                   f"factory: {out['change'][:60]} — {v}")
            rc._sh("git", "push", "-u", "origin", branch)
            body = "```json\n" + json.dumps(entry, indent=2) + "\n```\n"
            rc._sh("gh", "pr", "create", "--title",
                   f"[{v}] {out['change'][:70]}: "
                   f"{out['fitness_current']}→{out['fitness_patched']}",
                   "--body", body, "--base", base, "--head", branch)
            if v == "SHIP":
                rc._sh("gh", "pr", "merge", branch, "--squash",
                       "--delete-branch")
            else:
                rc._sh("gh", "pr", "close", branch, "--comment",
                       f"verdict: {v} — the patched org did not causally "
                       f"out-produce the current one.", "--delete-branch")
            rc._sh("git", "checkout", base)
            rc._sh("git", "pull", "--rebase")
            rc._record(entry)               # lineage lives on MAIN, always
            rc._publish(f"factory: lineage — {v} ({out['change'][:50]})",
                        rc.LINEAGE)
        else:
            if v == "SHIP":
                for d in candidate["diff"]:
                    src = patch / d["file"]
                    dst = rc._guard(rc.WORLD / d["file"])
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(src, dst)
            rc._record(entry)
        return out

    return judge


def build(ci: bool = False) -> DarkFactoryWorld:
    """darkfactory.json → every param of the ONE top-level World."""
    return DarkFactoryWorld(
        dict(CFG),
        dev_world_runtime=DevWorldRuntime(),
        live_world_runtime=LiveWorldRuntime(ci=ci),
        judge=make_judge(ci=ci))


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--ci", action="store_true")
    args = ap.parse_args()
    ci = args.ci or os.environ.get("CI") == "true"
    from .config import have_key
    if not (rc.ROOT / "FACTORY_ON").exists():
        print("FACTORY_ON absent — the org stays down.")
        return 0
    if not have_key():
        print("SKIP — the worlds are LLM-driven; set the key named by "
              "api_key_env in darkfactory.json")
        return 0
    world = build(ci=ci)
    print(world.describe())

    async def _run():
        res = await world.execute({})
        s = res.context["store"]
        for t in s.get("tasks", {}).values():
            print(f"  {t['dept']}: {t['status']}"
                  + (f" — {json.dumps(t.get('review'))[:120]}"
                     if t.get("review") else ""))
        # the deity's cross-cycle seat: rules + season + THE CALENDAR
        dev = next((t for t in s.get("tasks", {}).values()
                    if t["dept"] == "dev_world"), None)
        entry = {"verdict": (dev or {}).get("status"),
                 "review": (dev or {}).get("review"),
                 "day": s.get("day")}
        await rc._deity_retrospective(entry, ci)

    asyncio.run(_run())
    import sys
    sys.stdout.flush()
    os._exit(0)


if __name__ == "__main__":
    main()
