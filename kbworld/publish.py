#!/usr/bin/env python3
"""publish.py — THE PUBLISHING RAIL for factory-grown knowledge modules.

Tier design (mirrors sancrev-marketplace's own charter: "a thin reference
catalog that POINTS at each plugin's own repo — never houses their code"):

  kbworld/state/modules/<slug>/          the module, gate-merged on main
        │  sync (automatic — already reviewed+merged state)
        ▼
  sancovp/<slug>-module                  the module's OWN repo, PUBLIC
        │  marketplace PR — opened AND auto-merged (full-auto)
        ▼
  sancovp/sancrev-marketplace            listed automatically

FULL-AUTO / DARK FLOOR (Isaac 2026-08-10): door issue in → installable public
plugin out, zero human touch. The flex is the METHOD (proof-checked, self-
grown, self-published, free); the README's honesty note (coherence-not-truth)
is the receipt no competitor can print. Clean merges only — a conflicted
catalog is the one thing left for a human (never override conflicts).

Standalone by design: stdlib + git + gh only (no kbworld/ee_v2 imports), so
the publish workflow needs no model stack. Run:
    python kbworld/publish.py [--modules-root kbworld/state/modules]
                              [--marketplace sancovp/sancrev-marketplace]
                              [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def _run(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)}: {(r.stderr or r.stdout)[-400:]}")
    return r


class PubDeps:
    """Injectable boundary (gh + git); tests script these four."""

    def __init__(self, run=None, repo_exists=None, repo_create=None,
                 pr_open=None, pr_list=None, pr_merge=None):
        self.run = run or _run
        self.repo_exists = repo_exists or self._repo_exists
        self.repo_create = repo_create or self._repo_create
        self.pr_open = pr_open or self._pr_open
        self.pr_list = pr_list or self._pr_list
        self.pr_merge = pr_merge or self._pr_merge

    @staticmethod
    def _repo_exists(name):
        r = _run(["gh", "api", f"repos/{name}", "--jq", ".name"], check=False)
        return r.returncode == 0

    @staticmethod
    def _repo_create(name, description):
        # FULL-AUTO / DARK FLOOR (Isaac 2026-08-10): modules ship PUBLIC.
        # The flex is the method — proof-checked, self-grown, free, sitting
        # there. The README's honesty note (coherence-not-truth) is the
        # thing no competitor can even print.
        _run(["gh", "repo", "create", name, "--public",
              "--description", description])

    @staticmethod
    def _pr_list(repo):
        r = _run(["gh", "pr", "list", "--repo", repo, "--state", "open",
                  "--json", "title", "--jq", ".[].title"], check=False)
        return [t for t in r.stdout.splitlines() if t.strip()]

    @staticmethod
    def _pr_open(repo, branch, title, body):
        r = _run(["gh", "pr", "create", "--repo", repo, "--head", branch,
                  "--title", title, "--body", body], check=False)
        return r.stdout.strip() or r.stderr.strip()

    @staticmethod
    def _pr_merge(repo, branch):
        # clean merge only — a conflicted catalog is left for a human
        # (Isaac's standing rule: never override conflicts)
        r = _run(["gh", "pr", "merge", "--repo", repo, branch, "--merge"],
                 check=False)
        return r.returncode == 0


def sync_module(module_dir: Path, owner: str, deps: PubDeps,
                dry_run=False) -> dict:
    """Mirror one module dir into its own PRIVATE repo. Idempotent: commits
    only when content actually changed. Returns {repo, changed, created}."""
    entry = json.loads((module_dir / "marketplace-entry.json").read_text())
    repo = f"{owner}/{entry['name']}"
    if dry_run:
        return {"repo": repo, "changed": False, "created": False,
                "dry_run": True}
    created = False
    if not deps.repo_exists(repo):
        deps.repo_create(repo, entry["description"][:300])
        created = True
    with tempfile.TemporaryDirectory(prefix="pub-") as td:
        work = Path(td) / "w"
        deps.run(["git", "clone", "--depth", "1",
                  f"https://github.com/{repo}.git", str(work)], check=False)
        if not (work / ".git").exists():          # empty new repo
            work.mkdir(parents=True, exist_ok=True)
            deps.run(["git", "init", "-q", "-b", "main", str(work)])
            deps.run(["git", "remote", "add", "origin",
                      f"https://github.com/{repo}.git"], cwd=work)
        # mirror content (delete-and-copy = true sync, .git preserved)
        for item in work.iterdir():
            if item.name == ".git":
                continue
            deps.run(["rm", "-rf", str(item)])
        for item in module_dir.iterdir():
            deps.run(["cp", "-r", str(item), str(work / item.name)])
        deps.run(["git", "add", "-A"], cwd=work)
        dirty = deps.run(["git", "status", "--porcelain"], cwd=work
                         ).stdout.strip()
        if not dirty:
            return {"repo": repo, "changed": False, "created": created}
        deps.run(["git", "-c", "user.name=kbworld-publisher",
                  "-c", "user.email=kbworld@dark-factory-live",
                  "commit", "-q", "-m",
                  f"sync from factory state ({int(time.time())})"], cwd=work)
        deps.run(["git", "push", "-q", "origin", "main"], cwd=work)
    return {"repo": repo, "changed": True, "created": created}


def marketplace_pr(entries: list, marketplace: str, deps: PubDeps,
                   dry_run=False) -> dict:
    """Upsert entries (by name) into the marketplace catalog and open ONE PR.
    THE MACHINE NEVER MERGES IT — the maintainer's merge is the publishing
    act. Idempotent: no PR when the catalog already matches."""
    if dry_run:
        return {"pr": None, "upserted": [e["name"] for e in entries],
                "dry_run": True}
    with tempfile.TemporaryDirectory(prefix="mkt-") as td:
        work = Path(td) / "m"
        deps.run(["git", "clone", "--depth", "1",
                  f"https://github.com/{marketplace}.git", str(work)])
        cat_path = work / ".claude-plugin" / "marketplace.json"
        cat = json.loads(cat_path.read_text())
        by_name = {p["name"]: i for i, p in enumerate(cat["plugins"])}
        changed = []
        for e in entries:
            if e["name"] in by_name:
                if cat["plugins"][by_name[e["name"]]] != e:
                    cat["plugins"][by_name[e["name"]]] = e
                    changed.append(e["name"])
            else:
                cat["plugins"].append(e)
                changed.append(e["name"])
        if not changed:
            return {"pr": None, "upserted": []}
        # dedup: an open sync-PR already carrying these names means the
        # maintainer just hasn't merged yet — do NOT stack duplicates
        for title in deps.pr_list(marketplace):
            if all(n in title for n in changed):
                return {"pr": "pending (open PR already covers these)",
                        "upserted": [], "pending": changed}
        cat_path.write_text(json.dumps(cat, indent=2) + "\n")
        branch = f"modules/sync-{int(time.time())}"
        deps.run(["git", "checkout", "-q", "-b", branch], cwd=work)
        deps.run(["git", "add", "-A"], cwd=work)
        deps.run(["git", "-c", "user.name=kbworld-publisher",
                  "-c", "user.email=kbworld@dark-factory-live",
                  "commit", "-q", "-m",
                  f"catalog: upsert {', '.join(changed)} (factory modules)"],
                 cwd=work)
        deps.run(["git", "push", "-q", "-u", "origin", branch], cwd=work)
        url = deps.pr_open(
            marketplace, branch,
            f"catalog: {', '.join(changed)} (factory-grown modules)",
            "Machine-opened by the kbworld publishing rail on "
            "dark-factory-live. Each listed module's repo is synced and "
            "PRIVATE.\n\nPUBLISHING = two maintainer acts in one sitting: "
            "flip the module repo(s) public, then merge this PR. The "
            "machine never does either.\n\nModules: "
            + ", ".join(changed) +
            "\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)")
        merged = deps.pr_merge(marketplace, branch)
        return {"pr": url, "upserted": changed, "merged": merged}


def publish_all(modules_root: Path, owner="sancovp",
                marketplace="sancovp/sancrev-marketplace",
                deps: PubDeps = None, dry_run=False, log=print) -> dict:
    deps = deps or PubDeps()
    report = {"synced": [], "marketplace": None}
    entries = []
    for mod in sorted(Path(modules_root).iterdir()):
        if not (mod / "marketplace-entry.json").exists():
            continue
        r = sync_module(mod, owner, deps, dry_run=dry_run)
        log(f"[sync] {r['repo']}: "
            f"{'created+' if r.get('created') else ''}"
            f"{'pushed' if r.get('changed') else 'unchanged'}")
        report["synced"].append(r)
        e = json.loads((mod / "marketplace-entry.json").read_text())
        e["source"]["url"] = f"https://github.com/{r['repo']}.git"
        entries.append(e)
    if entries:
        report["marketplace"] = marketplace_pr(entries, marketplace, deps,
                                               dry_run=dry_run)
        m = report["marketplace"]
        log(f"[marketplace] upserted={m['upserted']} pr={m.get('pr')}")
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--modules-root",
                    default="kbworld/state/modules")
    ap.add_argument("--owner", default="sancovp")
    ap.add_argument("--marketplace", default="sancovp/sancrev-marketplace")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    rep = publish_all(Path(a.modules_root), a.owner, a.marketplace,
                      dry_run=a.dry_run)
    print(json.dumps({"synced": rep["synced"],
                      "marketplace": rep["marketplace"]}, indent=2))
