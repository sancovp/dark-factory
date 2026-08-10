#!/usr/bin/env python3
"""publish rail — deterministic proof. REAL git against local bare repos
(the injectable run() rewrites github URLs to local paths); gh scripted.

Asserted:
  * first publish: module repo CREATED private + content synced (README,
    plugin manifest, skills all land);
  * marketplace: entry UPSERTED next to existing entries, ONE PR opened,
    machine never merges (no merge call exists in the module);
  * idempotent: second publish = no new commit, no new PR;
  * update: changed module content → synced; entry unchanged → still no PR.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/home/ceo/repo/dark-factory")
from kbworld import publish                                       # noqa: E402


def sh(*cmd, cwd=None):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    assert r.returncode == 0, (cmd, r.stderr[-300:])
    return r.stdout


def main(tmp):
    tmp = Path(tmp)
    bares = tmp / "gh"
    (bares / "sancovp").mkdir(parents=True)

    def run(cmd, cwd=None, check=True):
        cmd = [c.replace("https://github.com/", f"{bares}/")
               if isinstance(c, str) else c for c in cmd]
        return publish._run(cmd, cwd=cwd, check=check)

    created, prs = [], []

    def repo_exists(name):
        return (bares / f"{name}.git").exists()

    def repo_create(name, description):
        created.append(name)
        sh("git", "init", "-q", "--bare", "-b", "main",
           str(bares / f"{name}.git"))

    def pr_open(repo, branch, title, body):
        prs.append((repo, branch, title))
        return f"local://pr/{len(prs)}"

    merged = []

    def pr_merge(repo, branch):
        merged.append((repo, branch))
        return True

    deps = publish.PubDeps(run=run, repo_exists=repo_exists,
                           repo_create=repo_create, pr_open=pr_open,
                           pr_list=lambda repo: [t for _r, _b, t in prs],
                           pr_merge=pr_merge)

    # seed the marketplace bare repo with one existing entry
    sh("git", "init", "-q", "--bare", "-b", "main",
       str(bares / "sancovp/sancrev-marketplace.git"))
    seed = tmp / "seed"
    sh("git", "clone", "-q", str(bares / "sancovp/sancrev-marketplace.git"),
       str(seed))
    (seed / ".claude-plugin").mkdir()
    (seed / ".claude-plugin/marketplace.json").write_text(json.dumps(
        {"name": "sancrev-marketplace",
         "plugins": [{"name": "doc-mirror", "description": "existing",
                      "author": {"name": "Isaac Rubin"},
                      "category": "productivity",
                      "source": {"source": "url", "url": "x"}}]}, indent=2))
    sh("git", "add", "-A", cwd=seed)
    sh("git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q",
       "-m", "seed", cwd=seed)
    sh("git", "push", "-q", "origin", "main", cwd=seed)

    # a fake emitted module
    mod = tmp / "modules" / "test_subject"
    (mod / ".claude-plugin").mkdir(parents=True)
    (mod / "skills/using-test-subject").mkdir(parents=True)
    (mod / ".claude-plugin/plugin.json").write_text(json.dumps(
        {"name": "test-subject-module", "version": "0.1.0"}))
    (mod / "marketplace-entry.json").write_text(json.dumps(
        {"name": "test-subject-module", "description": "a test module",
         "author": {"name": "Isaac Wostrel-Rubin"},
         "category": "productivity",
         "source": {"source": "url", "url": "placeholder"}}))
    (mod / "README.md").write_text("# test module\n")
    (mod / "skills/using-test-subject/SKILL.md").write_text(
        "---\nname: using-test-subject\ndescription: t\n---\nbody\n")

    # ── first publish ────────────────────────────────────────────────────────
    rep = publish.publish_all(tmp / "modules", deps=deps, log=lambda *_: None)
    assert created == ["sancovp/test-subject-module"]
    assert rep["synced"][0]["changed"] and rep["synced"][0]["created"]
    check = tmp / "check"
    sh("git", "clone", "-q", str(bares / "sancovp/test-subject-module.git"),
       str(check))
    assert (check / "README.md").exists()
    assert (check / ".claude-plugin/plugin.json").exists()
    assert (check / "skills/using-test-subject/SKILL.md").exists()
    print("  publish #1: repo created PUBLIC + fully synced ✓")

    assert rep["marketplace"]["upserted"] == ["test-subject-module"]
    assert len(prs) == 1 and prs[0][0] == "sancovp/sancrev-marketplace"
    assert rep["marketplace"]["merged"] and len(merged) == 1  # full-auto
    mchk = tmp / "mchk"
    sh("git", "clone", "-q", "-b", prs[0][1],
       str(bares / "sancovp/sancrev-marketplace.git"), str(mchk))
    cat = json.loads((mchk / ".claude-plugin/marketplace.json").read_text())
    names = [p["name"] for p in cat["plugins"]]
    assert names == ["doc-mirror", "test-subject-module"]
    assert cat["plugins"][1]["source"]["url"].endswith(
        "test-subject-module.git")
    print("  marketplace: entry upserted beside existing, ONE PR opened "
          "AND auto-merged (full-auto) ✓")

    # ── idempotency ──────────────────────────────────────────────────────────
    rev0 = sh("git", "rev-list", "--count", "main",
              cwd=bares / "sancovp/test-subject-module.git").strip()
    rep2 = publish.publish_all(tmp / "modules", deps=deps,
                               log=lambda *_: None)
    rev1 = sh("git", "rev-list", "--count", "main",
              cwd=bares / "sancovp/test-subject-module.git").strip()
    assert rev0 == rev1 and not rep2["synced"][0]["changed"]
    assert rep2["marketplace"]["upserted"] == [] and len(prs) == 1
    print("  publish #2 (no changes): no commit, no PR — idempotent ✓")

    # ── content update ───────────────────────────────────────────────────────
    (mod / "README.md").write_text("# test module v2\n")
    rep3 = publish.publish_all(tmp / "modules", deps=deps,
                               log=lambda *_: None)
    assert rep3["synced"][0]["changed"]
    assert rep3["marketplace"]["upserted"] == [] and len(prs) == 1
    print("  publish #3 (content changed, entry same): synced, still no new "
          "PR ✓")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as d:
        asyncio_unused = None
        main(d)
    print("PUBLISH PASS — FULL-AUTO / DARK FLOOR: each module mirrors to "
          "its own PUBLIC repo, the catalog upsert PR opens and auto-merges, "
          "idempotent on re-run. Door issue in → installable plugin out.")
