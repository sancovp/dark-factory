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
        task = json.loads(spec) if spec.strip().startswith("{") else {"charter": spec}
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
        out = {"verdict": v,
               "fitness_current": race.context["race"]["control"].get("fitness"),
               "fitness_patched": race.context["race"]["treatment"].get("fitness")}
        if v == "SHIP":
            for d in candidate["diff"]:
                src, dst = patch / d["file"], rc._guard(rc.WORLD / d["file"])
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(src, dst)
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
    from .config import have_key
    if not have_key():
        print("SKIP — the worlds are LLM-driven; set the key named by "
              "api_key_env in darkfactory.json")
        return 0
    world = build(ci=os.environ.get("CI") == "true")
    print(world.describe())
    res = asyncio.run(world.execute({}))
    b = res.context["board"]
    for t in b["tasks"]:
        print(f"  {t['dept']}: {t['status']}"
              + (f" — {t['review']}" if t.get("review") else ""))
    import sys
    sys.stdout.flush()
    os._exit(0)


if __name__ == "__main__":
    main()
