"""The dark factory — cave-teams acting the dark-factory way (DESIGN §1–§3:
the product is THE PACKAGE — the game itself. WoS improves WoS).

  0. TELEMETRY   the live-world plays on the CURRENT package (the repo's
                 world/ definition). Its numbers — throughput, stalls, where
                 the economy converges — are the spec that aims dev.
  1. DEV-WORLD   a real SkillcraftWorld (MiniMax players + deity, agent dirs
                 seeded from world-of-skillcraft's _template with full .claude
                 loadouts) plays WoS aimed at that telemetry: agents trade
                 skills to get BETTER AT THINKING about the change (the skill
                 economy = the dev substrate, not the product).
  2. IMPLEMENT   ONE agent — the market's most successful (top gold) — writes
                 THE DIFF: a change to the package (a quest = an economy rule,
                 or a loadout skill every player owns at boot).
  3. GATE        the changed package must EXECUTE: quests must carry a
                 grep-able reward (the anti-injection economy rule), the
                 patched world must seed, and any new/changed skill file must
                 pass the fresh-model test (WoS test_skill/test.sh verbatim —
                 factory/gate.py; the gate's run mints the independent
                 record). Failure = the implementer's lineage dies; the cause
                 is the next cycle's signal.
  4. RACETRACK   live world on the CURRENT package vs live world on the
                 PATCHED package — identical, one variable. Fitness = the
                 live economy's throughput. Replicated (Championship): live
                 worlds are stochastic. [cave_teams.darkfactory]
  5. SHIP        a strict causal win ⇒ the diff merges into world/ (+ shipped
                 loadout skills → .claude/skills/, golden + equippable) via a
                 PR the factory merges itself. Anything else ⇒ the PR closes
                 as a receipt. dev → PR → CI/CD → live → telemetry → dev.

Containment: writes only world/, .claude/skills/, LINEAGE.json. FACTORY_ON is
the kill switch.
"""
from __future__ import annotations

import argparse
import asyncio
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from cave_teams.skillcraft import (SkillcraftWorld, initial_state,
                                   post_bulletin, _grep_reward,
                                   skillcraft_advance)
from cave_teams.darkfactory import CarKind, Championship, racetrack

from .wos_team import WoSPlayer, WoSDeity, last_json
from .gate import fresh_test

ROOT = Path(__file__).resolve().parent.parent
WORLD = ROOT / "world"
GOLDEN = ROOT / ".claude" / "skills"
LINEAGE = ROOT / "LINEAGE.json"
PLAYERS = ["agent_001", "agent_002"]

CHARTER = ("WE NEED TO WORK TOGETHER TO IMPROVE THE CODEBASE. Come up with "
           "a skill that COMPOSES existing skills (a recipe) or is NEW, and "
           "can be USED to do something that improves this repo. Craft it, "
           "test it, trade it — the best one gets APPLIED to the repo and "
           "shipped through CI/CD if it passes every gate.")

DEV_ROUNDS = int(os.environ.get("FACTORY_DEV_ROUNDS", "3"))
LIVE_ROUNDS = int(os.environ.get("FACTORY_LIVE_ROUNDS", "3"))
REPLICATES = int(os.environ.get("FACTORY_REPLICATES", "2"))
MAX_RUNS_PER_DAY = int(os.environ.get("FACTORY_MAX_RUNS_PER_DAY", "4"))
RULES = WORLD / "rules"
GAME = WORLD / "game.json"           # THE CONTINUING WORLD (WoS's game.json)
MAX_RULES = int(os.environ.get("FACTORY_MAX_RULES", "12"))


def _guard(path: Path) -> Path:
    p = path.resolve()
    ok = (str(p).startswith(str(WORLD.resolve()) + os.sep)
          or str(p).startswith(str(GOLDEN.resolve()) + os.sep)
          or p == LINEAGE.resolve())
    if not ok:
        raise PermissionError(f"factory may not write outside world/, "
                              f".claude/skills/, LINEAGE.json: {p}")
    return p


def _record(entry: dict) -> None:
    log = json.loads(LINEAGE.read_text()) if LINEAGE.exists() else []
    log.append(entry)
    _guard(LINEAGE).write_text(json.dumps(log, indent=2) + "\n")


def _load_board() -> dict:
    """The continuing live world — world/game.json, exactly WoS's pattern
    (one shared state file at the game dir's root). Born fresh only once."""
    if GAME.exists():
        return json.loads(GAME.read_text())
    board = initial_state(PLAYERS)
    post_bulletin(board, "The world is born. Test before you list. "
                         "Diverge — quests and audits pay.")
    return board


def _persist_live(board: dict, agents_root: str, ci: bool) -> None:
    """The live world CONTINUES: its board becomes world/game.json and the
    agents' crafted/ + bought/ merge back into the repo's agent dirs —
    seasons, lore, gold, and artifacts accumulate like the original repo."""
    _guard(GAME).write_text(json.dumps(board, indent=2) + "\n")
    for a in PLAYERS:
        for sub in ("crafted", "bought"):
            src = Path(agents_root) / a / sub
            if src.is_dir():
                dst = _guard(WORLD / "agents" / a / sub)
                shutil.copytree(src, dst, dirs_exist_ok=True)
    if ci:
        _sh("git", "pull", "--rebase")
        _sh("git", "add", str(WORLD))
        _sh("git", "commit", "-m",
            f"live: the world continues (season "
            f"{board.get('season', {}).get('number')}, tick +{LIVE_ROUNDS})")
        _sh("git", "push")


def _load_rules() -> str:
    """The standing rulebook, as one briefing block (name: text per rule)."""
    if not RULES.is_dir():
        return ""
    parts = []
    for f in sorted(RULES.glob("*.md")):
        if f.name == "README.md":
            continue
        parts.append(f"- [{f.stem}] " + " ".join(f.read_text().split())[:400])
    return "\n".join(parts)


async def _deity_retrospective(entry: dict, ci: bool) -> list:
    """THE DEITY'S CROSS-CYCLE JOB: watch what happened, help them with it.
    After each cycle the deity reviews the full trace and accumulates the
    standing rules — the lessons every future world boots with. Additions
    and amendments only (same name replaces); capped at MAX_RULES."""
    from cave_teams.examples import MiniMaxRuntime
    from .wos_team import MPE, last_json
    existing = _load_rules()
    deity = MiniMaxRuntime(name="deity_retro", tools=[], system_prompt=(
        "You are the DEITY of World of Skillcraft in your CROSS-CYCLE seat: "
        "after each factory cycle you review what actually happened and "
        "accumulate THE STANDING RULES — the lessons every future dev-world "
        "and live-world boots with. Rules must be short, operational, and "
        "earned from THIS cycle's evidence (never speculative). Amend by "
        "reusing a rule's name; add sparingly.\n\n" + MPE))
    out = await deity.run(
        f"THE CYCLE THAT JUST HAPPENED:\n{json.dumps(entry, indent=1)[:3000]}\n\n"
        f"THE CURRENT STANDING RULES ({MAX_RULES} max):\n"
        f"{existing or '(none yet)'}\n\n"
        "What did this cycle teach? A death at the gate, a reverted race, a "
        "wasted dev-world, a shipped win — each may earn a rule that makes "
        "the NEXT cycle develop better. Reply ONLY JSON: "
        'You also hold deity-season.sh: set "advance_season": true ONLY '
        "when the live season has run its course (stagnant economy, lessons "
        "absorbed) — it pays bounties, resets gold to the floor, and RATCHETS "
        "the quality bar. Reply ONLY JSON: "
        '{"rules":[{"name":"<snake_case>","text":"<one operational rule, '
        '<=60 words>"}],"advance_season":false,"reasoning":"<one line>"} — '
        "an empty rules list is a valid answer if nothing was earned.")
    o = last_json(out if isinstance(out, str) else str(out),
                  keys=("rules",), default={})
    written = []
    current = [f for f in RULES.glob("*.md") if f.name != "README.md"]
    for r in (o.get("rules") or [])[:3]:              # ≤3 new lessons per cycle
        name = re.sub(r"[^a-z0-9_]+", "_", str(r.get("name", "")).lower()).strip("_")
        text = str(r.get("text", "")).strip()
        if not name or not text:
            continue
        path = RULES / f"{name}.md"
        if not path.exists() and len(current) + len(written) >= MAX_RULES:
            print(f"  deity: rulebook full ({MAX_RULES}) — '{name}' skipped")
            continue
        _guard(path).write_text(f"# {name}\n\n{text}\n")
        written.append(name)
    if written:
        print(f"  deity accumulated rule(s): {written}")
        if ci:
            _sh("git", "pull", "--rebase")
            _sh("git", "add", str(RULES))
            _sh("git", "commit", "-m",
                f"deity: standing rule(s) accumulated — {', '.join(written)}")
            _sh("git", "push")
    if o.get("advance_season") and GAME.exists():
        board = json.loads(GAME.read_text())
        nxt = skillcraft_advance()(board, board.get("season", {})
                                   .get("number", 1) + 1)
        _guard(GAME).write_text(json.dumps(nxt, indent=2) + "\n")
        print(f"  deity ADVANCED THE SEASON → {nxt['season']['number']} "
              f"(bounties paid, gold reset, ratchet carried)")
        if ci:
            _sh("git", "pull", "--rebase")
            _sh("git", "add", str(GAME))
            _sh("git", "commit", "-m",
                f"deity: season advanced → {nxt['season']['number']}")
            _sh("git", "push")
    return written


# ── the package: world/quests (economy rules) + world/loadout (boot skills) ──
def _seed_world(workdir: Path, tag: str, quests_src: Path,
                loadout_src: Path) -> tuple:
    """A fresh world instance ON A GIVEN PACKAGE: agent dirs from the repo's
    world (each with its _template .claude loadout), the package's quests,
    and the package's loadout skills copied into every player's crafted/."""
    root = workdir / tag
    agents_root = root / "agents"
    for a in PLAYERS:
        shutil.copytree(WORLD / "agents" / a, agents_root / a)
    quests = root / "quests"
    shutil.copytree(quests_src, quests)
    loadout = sorted(p for p in loadout_src.glob("*.md")
                     if p.name != "README.md")
    rules = sorted(p for p in (WORLD / "rules").glob("*.md")
                   if p.name != "README.md") if (WORLD / "rules").is_dir() else []
    for a in PLAYERS:
        adir = agents_root / a
        # EQUIPPED loadout skills → the agent's .claude/skills/ (claude-native:
        # a Claude Code process embodying this dir auto-loads them; crafted/
        # stays what the agent MAKES)
        for sk in loadout:
            d = adir / ".claude" / "skills" / sk.stem
            d.mkdir(parents=True, exist_ok=True)
            shutil.copy(sk, d / "SKILL.md")
        # STANDING RULES → the agent's .claude/rules/ (claude-native home;
        # prompt injection remains the MiniMax adapter)
        if rules:
            rdir = adir / ".claude" / "rules"
            rdir.mkdir(parents=True, exist_ok=True)
            for r in rules:
                shutil.copy(r, rdir / r.name)
    return str(agents_root), str(quests), [s.stem for s in loadout]


async def _run_world(agents_root: str, quests_root: str, rounds: int,
                     name: str, extra_note: str = "",
                     bulletin: str = "", start_board: dict = None) -> tuple:
    """One SkillcraftWorld game (players + deity). Returns (board, players) —
    the players' runtimes persist so the implementer can keep its context."""
    state = (json.loads(json.dumps(start_board)) if start_board
             else initial_state(PLAYERS))
    if bulletin:
        post_bulletin(state, bulletin)
    elif not start_board:
        post_bulletin(state, "Test before you list. Diverge — quests "
                             "and audits pay.")
    rules_text = _load_rules()
    players = {a: WoSPlayer(a, agents_root, quests_root, extra_note=extra_note,
                            rules_text=rules_text)
               for a in PLAYERS}
    world = SkillcraftWorld(
        agents=players, agents_root=agents_root, quests_root=quests_root,
        deity=WoSDeity(rules_text=rules_text), rounds=rounds, seasons=1,
        name=name)
    res = await world.execute({"board": state})
    return res.context["board"], players


def _throughput(board: dict) -> int:
    """Live fitness: the economy's output — completed trades + completed
    quests + skills crafted (the board's own counters)."""
    return (len(board.get("trade_history", []))
            + sum(a.get("quests_completed", 0)
                  for a in board.get("agents", {}).values())
            + sum(a.get("skills_crafted", 0)
                  for a in board.get("agents", {}).values()))


def _telemetry(board: dict) -> dict:
    return {"throughput": _throughput(board),
            "trades": len(board.get("trade_history", [])),
            "quests_completed": sum(a.get("quests_completed", 0)
                                    for a in board.get("agents", {}).values()),
            "skills_crafted": sum(a.get("skills_crafted", 0)
                                  for a in board.get("agents", {}).values()),
            "gold": {a: v.get("gold")
                     for a, v in board.get("agents", {}).items()},
            "bulletins": [x["message"]
                          for x in board.get("deity_bulletin", [])][-3:]}


def _delta_throughput(after: dict, before: dict) -> int:
    return _throughput(after) - _throughput(before)


def _live_kind(workdir: Path, patch: Path) -> CarKind:
    """The racetrack CarKind: car = {'package': 'current'|'patched'}. race() =
    play a full live WoS on that package version."""
    counter = {"n": 0}

    async def _race(car, _wd, tag="live"):
        counter["n"] += 1
        if car["package"] == "patched":
            q_src, l_src = patch / "quests", patch / "loadout"
        else:
            q_src, l_src = WORLD / "quests", WORLD / "loadout"
        agents_root, quests, loadout = _seed_world(
            workdir, f"{tag}-{counter['n']}", q_src, l_src)
        note = (f"You have these loadout skills EQUIPPED (in your "
                f".claude/skills/): {loadout} — APPLY them whenever they "
                f"help your play." if loadout else "")
        start = _load_board()
        board, _ = await _run_world(agents_root, quests, LIVE_ROUNDS,
                                    name=f"live:{tag}", extra_note=note,
                                    start_board=start)
        return {"tag": tag, "fitness": _delta_throughput(board, start),
                "trades": len(board.get("trade_history", [])), "car": dict(car)}

    async def _viability(car, _wd):
        return {"alive": True, "cause": "gated upstream", "telemetry": None}

    return CarKind(race=_race, viability=_viability,
                   apply_delta=lambda c, d: c, name="live-package")


def _diff(patch: Path) -> list:
    """The diff: files under the patch that differ from the current package."""
    out = []
    for sub in ("quests", "loadout"):
        cur_dir, new_dir = WORLD / sub, patch / sub
        for f in sorted(new_dir.glob("*.md")):
            if f.name == "README.md":
                continue
            cur = cur_dir / f.name
            if not cur.exists():
                out.append({"file": f"{sub}/{f.name}", "kind": "added"})
            elif cur.read_text() != f.read_text():
                out.append({"file": f"{sub}/{f.name}", "kind": "modified"})
    return out


async def _gate_package(patch: Path, diff: list, implementer_dir: str) -> dict:
    """The changed package must EXECUTE (materialize → execute → test):
    every changed quest must carry a grep-able positive reward; the patched
    world must seed; every new/changed skill passes the fresh-model test."""
    for d in diff:
        if d["file"].startswith("quests/"):
            body = (patch / d["file"]).read_text()
            if _grep_reward(body) <= 0:
                return {"alive": False,
                        "cause": f"{d['file']}: no grep-able positive reward "
                                 f"(the economy rule would not execute)"}
    try:
        with tempfile.TemporaryDirectory() as td:
            _seed_world(Path(td), "boot", patch / "quests", patch / "loadout")
    except Exception as e:
        return {"alive": False, "cause": f"patched world does not seed: {e}"}
    minted = []
    for d in diff:
        if d["file"].startswith("loadout/"):
            # the fresh test runs from the implementer's dir (the crafter's
            # record home): copy the skill there, then test.sh it.
            rel = os.path.join("crafted", os.path.basename(d["file"]))
            dst = Path(implementer_dir) / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(patch / d["file"], dst)
            g = await fresh_test(implementer_dir, rel,
                                 "A realistic task for this skill, chosen "
                                 "blind: summarize your instructions' purpose "
                                 "by APPLYING them to: 'the quarterly report "
                                 "is late and nobody knows why'")
            if not g["ok"]:
                return {"alive": False,
                        "cause": f"{d['file']}: fresh instance could not "
                                 f"follow the skill"}
            minted.append({"file": d["file"], "test_id": g["test_id"],
                           "record_path": g["record_path"]})
    return {"alive": True, "cause": "pass", "minted": minted}


def _open_issues(ci: bool) -> list:
    """The live system's bug backlog (CI: real GitHub issues)."""
    if not ci:
        return []
    try:
        out = _sh("gh", "issue", "list", "--state", "open", "--limit", "10",
                  "--json", "number,title")
        return [{"number": i["number"], "title": i["title"]}
                for i in json.loads(out or "[]")]
    except Exception:
        return []


def _file_world_bugs(board: dict, ci: bool) -> list:
    """Deity-VALIDATED bugs from the live board become GitHub Issues — the
    `issues:` workflow trigger then convenes the dev system automatically
    ("when it has issues it runs the dev system auto")."""
    filed = []
    if not ci:
        return filed
    try:
        existing = {i["title"] for i in
                    json.loads(_sh("gh", "issue", "list", "--state", "all",
                                   "--limit", "50", "--json", "title") or "[]")}
    except Exception:
        existing = set()
    for bug in board.get("bug_reports", []):
        if bug.get("status") != "valid":
            continue
        title = f"[world-bug] {bug.get('title', bug.get('id', '?'))[:70]}"
        if title in existing:
            continue
        try:
            _sh("gh", "issue", "create", "--title", title, "--body",
                f"Filed by the live world's deity-validated bug report.\n\n"
                f"**Reporter:** {bug.get('reporter')}\n"
                f"**Severity:** {bug.get('severity')}\n\n"
                f"**Description:** {bug.get('description')}\n\n"
                f"**Reproduction:** {bug.get('reproduction')}")
            filed.append(title)
        except Exception:
            pass
    return filed


def _runs_today(ci: bool) -> int:
    """The governor's meter: workflow runs started today (UTC)."""
    if not ci:
        return 0
    try:
        today = datetime.datetime.now(
            datetime.timezone.utc).strftime("%Y-%m-%d")
        out = _sh("gh", "run", "list", "--workflow", "factory.yml",
                  "--limit", "30", "--json", "createdAt")
        return sum(1 for r in json.loads(out or "[]")
                   if str(r.get("createdAt", "")).startswith(today))
    except Exception:
        return MAX_RUNS_PER_DAY            # meter broken → assume cap hit

def _self_kick(filed: list, ci: bool) -> None:
    """"When it has issues it runs the dev system auto": a cycle that filed
    NEW world-bugs kicks the next cycle immediately via workflow_dispatch
    (GitHub's designed exception to token anti-recursion) — governed by a
    daily run cap so a bug-rich world cannot chain-burn forever."""
    if not (ci and filed):
        return
    n = _runs_today(ci)
    if n >= MAX_RUNS_PER_DAY:
        print(f"  governor: {n} runs today ≥ cap {MAX_RUNS_PER_DAY} — "
              f"the backlog waits for the heartbeat")
        return
    try:
        _sh("gh", "workflow", "run", "factory.yml")
        print(f"  self-kick: new world-bugs filed → next cycle dispatched "
              f"({n + 1}/{MAX_RUNS_PER_DAY} today)")
    except Exception as e:
        print(f"  self-kick failed (non-fatal): {e}")

def _sh(*cmd: str) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed: {r.stderr[-400:]}")
    return r.stdout.strip()


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", name.lower()).strip("_") or "change"


async def cycle(ci: bool) -> dict:
    now = datetime.datetime.now(
        datetime.timezone.utc).isoformat(timespec="seconds")
    workdir = Path(tempfile.mkdtemp(prefix="darkfactory-"))

    # ── 0. live telemetry on the current package (the spec that aims dev) ──
    agents_root, quests, loadout = _seed_world(
        workdir, "telemetry", WORLD / "quests", WORLD / "loadout")
    note = (f"You have these loadout skills EQUIPPED (in your "
            f".claude/skills/): {loadout} — apply them." if loadout else "")
    board0, _ = await _run_world(agents_root, quests, LIVE_ROUNDS,
                                 name="live:telemetry", extra_note=note,
                                 start_board=_load_board())
    _persist_live(board0, agents_root, ci)
    tel = _telemetry(board0)
    print(f"  telemetry (current package): {tel['throughput']} throughput "
          f"({tel['trades']} trades, {tel['quests_completed']} quests, "
          f"{tel['skills_crafted']} crafts)")
    filed = _file_world_bugs(board0, ci)
    if filed:
        print(f"  filed {len(filed)} world-bug issue(s): {filed}")
    _self_kick(filed, ci)

    # ── 1. the dev-world plays, aimed at the telemetry ──
    issues = _open_issues(ci)
    aim = (f"{CHARTER}\nTHE LIVE GAME'S TELEMETRY: {json.dumps(tel)}."
           + (f"\nOPEN ISSUES (the live system's bug backlog — address one "
              f"if you can): {json.dumps(issues)}" if issues else ""))
    dev_agents, dev_quests, _ = _seed_world(
        workdir, "dev", WORLD / "quests", WORLD / "loadout")
    dev_board, dev_players = await _run_world(
        dev_agents, dev_quests, DEV_ROUNDS, name="dev-world", extra_note=aim,
        bulletin=CHARTER)
    print(f"  dev-world: {len(dev_board.get('trade_history', []))} trades, "
          f"throughput {_throughput(dev_board)}")

    # ── 2. THE APPLY STEP (the design's mechanism): the dev-world's crafted
    #    skill is the INSTRUMENT — an agent equipped with it EXECUTES it
    #    against the target (the package of the repo this factory is launched
    #    in); the diff falls out of the skill's application.
    #    Candidate skill: the one a peer BOUGHT (the market's vote), else the
    #    top-gold agent's newest craft (their proposal). ──
    gold = {a: v.get("gold", 0)
            for a, v in dev_board.get("agents", {}).items()}
    impl_name = max(gold, key=gold.get)
    trades_hist = dev_board.get("trade_history", [])
    skill_src, skill_why = None, ""
    if trades_hist:
        sale = trades_hist[-1]
        impl_name = sale["buyer"]              # the buyer applies what it bought
        skill_src = Path(dev_agents) / sale["seller"] / sale["skill_path"]
        skill_why = (f"bought from {sale['seller']} for {sale['price']}g "
                     f"(rarity {sale.get('rarity', '?')})")
    else:
        crafted = sorted(
            (Path(dev_agents) / impl_name / "crafted").glob("*.md"),
            key=lambda p: p.stat().st_mtime)
        if crafted:
            skill_src = crafted[-1]
            skill_why = f"{impl_name}'s newest craft (no trade this cycle)"
    if skill_src is None or not skill_src.exists():
        entry = {"at": now, "verdict": "NO_CANDIDATE",
                 "why": "the dev-world crafted no applicable skill"}
        _record(entry)
        print("  ✗ no candidate skill from the dev-world")
        if ci:
            _sh("git", "add", str(LINEAGE))
            _sh("git", "commit", "-m", "factory: no candidate skill")
            _sh("git", "push")
        return entry
    skill_content = skill_src.read_text()
    skill_name = skill_src.stem
    print(f"  instrument: '{skill_name}' — {skill_why}")

    impl = dev_players[impl_name]
    patch = workdir / "patch"
    shutil.copytree(WORLD / "quests", patch / "quests")
    shutil.copytree(WORLD / "loadout", patch / "loadout")
    out = await impl.rt.run(
        f"You are now the IMPLEMENTER — APPLY the skill to the target.\n\n"
        f"THE SKILL (your instrument — follow its procedure):\n"
        f"{skill_content}\n\n"
        f"THE TARGET — the package of the repo this factory runs in, checked "
        f"out at {patch}:\n"
        f"  quests/   — each .md is a quest; its '## Reward\\nN gold' line IS "
        f"an economy rule (rewards are grepped from the file).\n"
        f"  loadout/  — skills EVERY player owns at world boot.\n"
        f"LIVE TELEMETRY the change must address: {json.dumps(tel)}\n\n"
        f"EXECUTE the skill's procedure against the target with your file "
        f"tools — the change the applied skill produces IS the PR. You may "
        f"also install the skill itself as loadout/{skill_name}.md if every "
        f"player owning it is the change. Then reply ONLY JSON: "
        f'{{"change":"<one line: what the applied skill did and why>",'
        f'"files":["quests/x.md" or "loadout/y.md"]}}')
    proposal = last_json(out if isinstance(out, str) else str(out),
                         keys=("change", "files"), default={})
    diff = _diff(patch)
    change_line = str(proposal.get("change", ""))[:200]
    if not diff:
        entry = {"at": now, "verdict": "NO_DIFF", "implementer": impl_name,
                 "claimed": change_line,
                 "why": "the implementer changed no package file"}
        _record(entry)
        print(f"  ✗ no diff — {impl_name} changed nothing")
        if ci:
            _sh("git", "add", str(LINEAGE))
            _sh("git", "commit", "-m", "factory: no diff from the implementer")
            _sh("git", "push")
        return entry
    print(f"  diff by {impl_name}: {[d['file'] for d in diff]} — "
          f"{change_line!r}")

    # ── 3. the gate: the changed package must execute ──
    verdictg = await _gate_package(patch, diff,
                                   os.path.join(dev_agents, impl_name))
    if not verdictg["alive"]:
        entry = {"at": now, "verdict": "DEAD_AT_GATE", "diff": diff,
                 "implementer": impl_name, "instrument": skill_name,
                 "change": change_line,
                 "cause": verdictg["cause"]}
        _record(entry)
        print(f"  ☠ died at the gate: {verdictg['cause']}")
        if ci:
            _sh("git", "add", str(LINEAGE))
            _sh("git", "commit", "-m",
                f"factory: diff died at the gate ({verdictg['cause'][:60]})")
            _sh("git", "push")
        return entry
    print(f"  gate: package executes"
          + (f"; minted {[m['test_id'] for m in verdictg['minted']]}"
             if verdictg["minted"] else ""))

    # ── 4. the racetrack: current package vs patched package, live ──
    kind = _live_kind(workdir, patch)
    control, treatment = {"package": "current"}, {"package": "patched"}
    if REPLICATES > 1:
        race = await Championship(control, treatment, str(workdir),
                                  replicates=REPLICATES,
                                  kind=kind).execute({})
    else:
        race = await racetrack(control, treatment, str(workdir),
                               kind=kind).execute({})
    rc = race.context
    verdict = rc["verdict"]
    f_c = rc["race"]["control"].get("fitness")
    f_t = rc["race"]["treatment"].get("fitness")
    print(f"  race: current={f_c} patched={f_t}"
          + (f" tally {rc['tally']['ships']}–{rc['tally']['reverts']}"
             if "tally" in rc else "") + f" → {verdict}")

    entry = {"at": now, "verdict": verdict, "implementer": impl_name,
             "instrument": skill_name, "change": change_line, "diff": diff,
             "telemetry_before": tel,
             "fitness_current": f_c, "fitness_patched": f_t}
    if "tally" in rc:
        entry["tally"] = rc["tally"]
    if verdictg["minted"]:
        entry["gate_test_ids"] = [m["test_id"] for m in verdictg["minted"]]

    # ── 5. ship / receipt ──
    branch = f"factory/{_slug(change_line) or 'change'}"[:60] + \
             f"-{now.replace(':', '').replace('+', 'Z')}"
    if ci:
        base = _sh("git", "rev-parse", "--abbrev-ref", "HEAD")
        _sh("git", "checkout", "-b", branch)
    if verdict == "SHIP":
        for d in diff:
            src = patch / d["file"]
            dst = _guard(WORLD / d["file"])
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
            if d["file"].startswith("loadout/"):
                gdir = _guard(GOLDEN / _slug(os.path.basename(d["file"])[:-3]))
                gdir.mkdir(parents=True, exist_ok=True)
                shutil.copy(src, gdir / "SKILL.md")
        for m in verdictg["minted"]:
            rec_dst = _guard(WORLD / "loadout" / ".tests"
                             / os.path.basename(m["record_path"]))
            rec_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(m["record_path"], rec_dst)
        print(f"  SHIPPED: the diff is now the package "
              f"({[d['file'] for d in diff]})")
    _record(entry)
    if ci:
        _sh("git", "add", "-A")
        _sh("git", "commit", "-m",
            f"factory: {change_line[:60]} — {verdict} ({f_c} vs {f_t})")
        _sh("git", "push", "-u", "origin", branch)
        body = "```json\n" + json.dumps(entry, indent=2) + "\n```\n"
        _sh("gh", "pr", "create", "--title",
            f"[{verdict}] {change_line[:70]}: {f_c}→{f_t}",
            "--body", body, "--base", base, "--head", branch)
        if verdict == "SHIP":
            _sh("gh", "pr", "merge", branch, "--squash", "--delete-branch")
            print("  PR merged")
        else:
            _sh("gh", "pr", "close", branch, "--comment",
                f"verdict: {verdict} — the live world on the patched package "
                f"did not causally out-produce the current one. The closed "
                f"PR is the receipt.", "--delete-branch")
            print("  PR closed (receipt)")
        _sh("git", "checkout", base)
        _sh("git", "pull", "--rebase")     # SHIP squash-merges land on origin
        if verdict != "SHIP":              # the branch died with the entry —
            _record(entry)                 # re-record the receipt on MAIN
            _sh("git", "add", str(LINEAGE))
            _sh("git", "commit", "-m",
                f"factory: lineage — {verdict} ({change_line[:50]})")
            _sh("git", "push")
    await _deity_retrospective(entry, ci)
    return entry


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ci", action="store_true")
    args = ap.parse_args()
    if not (ROOT / "FACTORY_ON").exists():
        print("FACTORY_ON absent — autonomous cycles are paused.")
        return 0
    if not os.environ.get("MINIMAX_API_KEY"):
        print("SKIP — MINIMAX_API_KEY not set (the worlds are LLM-driven)")
        return 0
    asyncio.run(cycle(ci=args.ci))
    sys.stdout.flush()
    os._exit(0)                    # heaven non-daemon threads → hard exit


if __name__ == "__main__":
    sys.exit(main())
