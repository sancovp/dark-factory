#!/usr/bin/env python3
"""darkfloor.py — THE AUTONOMOUS SUBJECT PICKER (Isaac 2026-08-10: "running
full auto. dark floor.").

A scheduled beat has no subject; this picks one so the factory runs unattended:
  1. OPEN kb-door issues win — each names a subject to grow/deepen (the human
     steering surface; oldest first).
  2. else DEEPEN the least-recently-rounded existing module (round reports
     carry the timestamp; the coldest module gets the next beat).
  3. else a SEED subject (first not-yet-built), so a fresh floor still moves.

Prints the chosen subject on stdout — the workflow captures it and dispatches
one round. Stdlib + gh only. The round itself self-merges through the CI/CD
gate; the publisher then ships the module. Nothing here needs a human."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

SEEDS = ["home espresso", "vegetable gardening", "wine tasting",
         "bread baking", "coffee roasting", "cheesemaking"]

_SAFE = re.compile(r"[^a-zA-Z0-9 _-]")


def sanitize(subject: str) -> str:
    """SECURITY (2026-08-10 review): a kb-door issue title is UNTRUSTED input
    that flows into a CI runner. Strip everything outside [A-Za-z0-9 _-] so a
    title can never carry shell metacharacters (backtick, $, ", ;, newline)
    into the dispatch. Collapse whitespace; cap length. Empty after strip →
    fall back to a seed (never dispatch an empty/degenerate subject)."""
    clean = _SAFE.sub(" ", subject or "")
    clean = " ".join(clean.split())[:80].strip()
    return clean or SEEDS[0]


def _gh(*args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def _slug(x):
    return re.sub(r"[^a-z0-9_]+", "_", x.strip().lower()).strip("_")[:48]


def pick(state_root="kbworld/state", repo=None) -> str:
    # 1 — open kb-door issues (oldest first). A door is a ONE-SHOT aim: pick
    # the oldest, then CLOSE it so the next beat advances to the next door
    # (else the beat re-picks the same oldest door forever and the portfolio
    # never drains). After bootstrapping, the subject keeps growing via the
    # coldest-module rotation below.
    base = (["issue", "list"] + (["--repo", repo] if repo else [])
            + ["--label", "kb-door", "--state", "open", "--json",
               "number,title,createdAt", "--jq",
               'sort_by(.createdAt) | .[0] | '
               'if . == null then "" else "\\(.number)\\t\\(.title)" end'])
    row = _gh(*base).strip()
    if row and "\t" in row:
        num, title = row.split("\t", 1)
        subject = sanitize(re.sub(r"^kb-door:\s*", "", title))
        close = (["issue", "close", num] + (["--repo", repo] if repo else [])
                 + ["--comment", "aimed — the dark floor dispatched a round "
                    "on this subject; it deepens via the coldest-module "
                    "rotation thereafter"])
        _gh(*close)
        return subject

    # 2 — deepen the least-recently-rounded existing module
    kbs = Path(state_root) / "kbs"
    reports = sorted(Path(state_root).glob("round_*.json"))
    last_seen = {}
    for rp in reports:
        try:
            subj = json.loads(rp.read_text()).get("subject")
        except Exception as e:
            print(f"WARNING: unreadable round report {rp.name}: {e}",
                  file=sys.stderr)
            continue
        if subj:
            last_seen[subj] = rp.stat().st_mtime
    if kbs.is_dir():
        built = [d.name for d in kbs.iterdir() if d.is_dir()]
        if built:
            # coldest: a built module with the oldest (or no) round record
            def age(name):
                for subj, ts in last_seen.items():
                    if _slug(subj) == name:
                        return ts
                return 0.0
            coldest = min(built, key=age)
            # pick the subject whose round report ran MOST RECENTLY for this
            # dir (mtime, not insertion order — matters when subjects collide
            # to the same slug)
            matches = [(subj, ts) for subj, ts in last_seen.items()
                       if _slug(subj) == coldest]
            if matches:
                return sanitize(max(matches, key=lambda x: x[1])[0])
            return sanitize(coldest.replace("_", " "))

    # 3 — a fresh seed the floor hasn't built yet
    built_slugs = {d.name for d in kbs.iterdir()} if kbs.is_dir() else set()
    for seed in SEEDS:
        if _slug(seed) not in built_slugs:
            return sanitize(seed)
    return sanitize(SEEDS[0])


if __name__ == "__main__":
    repo = sys.argv[1] if len(sys.argv) > 1 else None
    print(pick(repo=repo))
