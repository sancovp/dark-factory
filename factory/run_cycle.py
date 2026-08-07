"""The factory runner — one autonomous cycle per car, path-guarded.

    python -m factory.run_cycle             # local: cycle every car, print verdicts
    python -m factory.run_cycle --ci        # in Actions: PR per proposal, merge on SHIP
    python -m factory.run_cycle --selftest  # keyless: fixture candidate through the
                                            # full gate+championship machinery

CONTAINMENT (v1, non-negotiable):
  * every write goes through _guarded_write, which refuses any path outside
    garage/ or LINEAGE.json — the factory cannot touch .github/, its own
    runner, or anything else (no self-modifying CI);
  * the autonomous path runs only while the FACTORY_ON file exists;
  * prose cars are skipped cleanly when MINIMAX_API_KEY is absent.
"""
from __future__ import annotations

import argparse
import asyncio
import datetime
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from cave_teams.darkfactory import DarkFactory, proposer_from_fn
from cave_teams.skillcar import skill_kind, new_skill_car

from . import seats

ROOT = Path(__file__).resolve().parent.parent
GARAGE = ROOT / "garage"
LINEAGE = ROOT / "LINEAGE.json"


def _guarded_write(path: Path, text: str) -> None:
    """THE containment: refuse any write outside garage/ or LINEAGE.json."""
    p = path.resolve()
    if not (str(p).startswith(str(GARAGE.resolve()) + os.sep)
            or p == LINEAGE.resolve()):
        raise PermissionError(f"factory may not write outside garage/: {p}")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _load_car(car_dir: Path) -> dict:
    meta = json.loads((car_dir / "car.json").read_text())
    car = new_skill_car((car_dir / "skill.md").read_text(),
                        name=meta["name"])
    car["kind"] = meta["kind"]
    car["generation"] = meta.get("generation", 0)
    return car


def _battery(car_dir: Path) -> list:
    return json.loads((car_dir / "battery.json").read_text())


def _kind_for(car: dict, battery: list, replicates_hint: dict):
    if car["kind"] == "prose":
        async def judge(a, t, w):
            return await asyncio.to_thread(seats.fresh_judge, a, t, w)
        replicates_hint["n"] = int(os.environ.get("FACTORY_REPLICATES", "3"))
        return skill_kind(battery, executor=judge, require_block=False,
                          name="prose-car")
    replicates_hint["n"] = 1                 # subprocess judge is deterministic
    return skill_kind(battery, name="code-car")


def _record(entry: dict) -> None:
    log = json.loads(LINEAGE.read_text()) if LINEAGE.exists() else []
    log.append(entry)
    _guarded_write(LINEAGE, json.dumps(log, indent=2) + "\n")


def _apply_ship(car_dir: Path, factory: DarkFactory) -> None:
    _guarded_write(car_dir / "skill.md", factory.car["artifact"])
    meta = json.loads((car_dir / "car.json").read_text())
    meta["generation"] = factory.car["generation"]
    _guarded_write(car_dir / "car.json", json.dumps(meta, indent=2) + "\n")


def _sh(*cmd: str) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed: {r.stderr[-400:]}")
    return r.stdout.strip()


async def cycle_car(car_dir: Path, ci: bool) -> dict:
    car = _load_car(car_dir)
    if car["kind"] == "prose" and not seats.have_key():
        print(f"  [{car['name']}] SKIP — prose car needs MINIMAX_API_KEY")
        return {"car": car["name"], "verdict": "SKIPPED_NO_KEY"}
    if not seats.have_key():
        print(f"  [{car['name']}] SKIP — dev seat needs MINIMAX_API_KEY "
              f"(the gate machinery is exercised keyless by --selftest)")
        return {"car": car["name"], "verdict": "SKIPPED_NO_KEY"}

    hint: dict = {}
    kind = _kind_for(car, _battery(car_dir), hint)
    with tempfile.TemporaryDirectory() as td:
        factory = DarkFactory(car, workdir=td, max_attempts=2, kind=kind,
                              replicates=hint["n"])
        seat = seats.DevSeat()
        rep = await factory.cycle(proposer_from_fn(
            lambda ctx: seat.propose(ctx.get("car", {}),
                                     ctx.get("telemetry", {}),
                                     ctx.get("gate_feedback"))))
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    entry = {"at": now, "car": car["name"], "kind": car["kind"],
             "verdict": rep["verdict"],
             "incumbent_fitness": rep["telemetry"]["fitness"],
             "cases": rep["telemetry"]["cases"],
             "extinct": rep.get("extinct", [])}
    if rep.get("race"):
        entry["race"] = {"control": rep["race"]["control"].get("fitness"),
                         "treatment": rep["race"]["treatment"].get("fitness")}
    if rep.get("tally"):
        entry["tally"] = rep["tally"]
    print(f"  [{car['name']}] incumbent {entry['incumbent_fitness']}/"
          f"{entry['cases']} → {entry['verdict']}"
          + (f" (race {entry['race']['control']} vs "
             f"{entry['race']['treatment']})" if "race" in entry else "")
          + (f" tally {entry['tally']['ships']}–{entry['tally']['reverts']}"
             if "tally" in entry else ""))

    if not ci:
        if rep["verdict"] == "SHIP":
            _apply_ship(car_dir, factory)
        _record(entry)
        return entry

    # ── CI: the proposal is a real PR; the verdict merges or closes it ──
    branch = f"factory/{car['name']}-gen{factory.car['generation']}-" \
             f"{now.replace(':', '').replace('+', 'Z')}"
    if rep.get("candidate"):
        base = _sh("git", "rev-parse", "--abbrev-ref", "HEAD")
        _sh("git", "checkout", "-b", branch)
        _guarded_write(car_dir / "skill.md", rep["candidate"]["artifact"])
        meta = json.loads((car_dir / "car.json").read_text())
        meta["generation"] = rep["candidate"]["generation"]
        _guarded_write(car_dir / "car.json", json.dumps(meta, indent=2) + "\n")
        _record(entry)
        _sh("git", "add", "-A")
        _sh("git", "commit", "-m",
            f"factory proposal: {car['name']} gen{rep['candidate']['generation']}")
        _sh("git", "push", "-u", "origin", branch)
        body = ("Autonomous factory proposal.\n\n```json\n"
                + json.dumps(entry, indent=2) + "\n```\n")
        pr = _sh("gh", "pr", "create", "--title",
                 f"[{entry['verdict']}] {car['name']} gen"
                 f"{rep['candidate']['generation']}: "
                 f"{entry.get('race', {}).get('control')}→"
                 f"{entry.get('race', {}).get('treatment')}",
                 "--body", body, "--base", base, "--head", branch)
        if rep["verdict"] == "SHIP":
            _sh("gh", "pr", "merge", branch, "--squash", "--delete-branch")
            print(f"  [{car['name']}] PR merged: {pr}")
        else:
            _sh("gh", "pr", "close", branch, "--comment",
                f"verdict: {rep['verdict']} — the change did not causally "
                f"beat the incumbent. The closed PR is the receipt.",
                "--delete-branch")
            print(f"  [{car['name']}] PR closed (receipt): {pr}")
        _sh("git", "checkout", base)
    else:                                     # every lineage died at the gate
        _record(entry)
        _sh("git", "add", str(LINEAGE))
        _sh("git", "commit", "-m",
            f"factory: {car['name']} — all lineages extinct at the gate")
        _sh("git", "push")
    return entry


async def selftest() -> None:
    """Keyless proof of the whole machinery: a FIXTURE candidate is pushed
    through the real quarantine + championship against the live garage car."""
    from cave_teams.darkfactory import Championship, racetrack
    from cave_teams.skillcar import apply_artifact_delta
    car_dir = GARAGE / "extract-emails"
    car = _load_car(car_dir)
    kind = _kind_for(car, _battery(car_dir), {})
    fix = json.loads((ROOT / "tests" / "fixtures.json").read_text())
    with tempfile.TemporaryDirectory() as td:
        dead = await kind.viability(
            apply_artifact_delta(car, {"artifact": fix["broken"]}), td)
        assert not dead["alive"], "broken fixture must die at the gate"
        good = apply_artifact_delta(car, {"artifact": fix["better"]})
        alive = await kind.viability(good, td)
        assert alive["alive"], "better fixture must survive the gate"
        race = await racetrack(car, good, td, kind=kind).execute({})
        v = race.context["verdict"]
        f_c = race.context["race"]["control"]["fitness"]
        f_t = race.context["race"]["treatment"]["fitness"]
        assert v == "SHIP" and f_t > f_c, f"fixture must strictly win ({f_c} vs {f_t})"
        champ = await Championship(car, good, td, replicates=3,
                                   kind=kind).execute({})
        assert champ.context["verdict"] == "SHIP"
    print(f"SELFTEST PASS — gate kills the broken fixture, the better fixture "
          f"ships {f_c}→{f_t} on the racetrack and 3-replicate championship. "
          f"The machinery is live; only the seats need a key.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ci", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--car", default="all")
    args = ap.parse_args()
    if args.selftest:
        asyncio.run(selftest())
        return 0
    if not (ROOT / "FACTORY_ON").exists():
        print("FACTORY_ON absent — autonomous cycles are paused.")
        return 0
    dirs = sorted(d for d in GARAGE.iterdir() if (d / "car.json").exists())
    if args.car != "all":
        dirs = [d for d in dirs if d.name == args.car]
    print(f"dark factory — {len(dirs)} car(s), ci={args.ci}")
    for d in dirs:
        asyncio.run(cycle_car(d, ci=args.ci))
    return 0


if __name__ == "__main__":
    sys.exit(main())
