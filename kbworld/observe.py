"""observe.py — THE OBSERVATION PASS (§22.4: observation replaces control).

A seat reads the module's own warmest regions AS A USER WOULD and names
concrete wrongness — which becomes `kb-supersede` issues (§18b: never
retract, supersede; the consumers-cone prices each regret). The deity
retrospective later mints standing rules from these logs. STRICT boundary:
findings must be the exact JSONL schema; unparseable output is residue-taught
(RULE 2), never accepted loosely."""
from __future__ import annotations

import asyncio
import json
import re


FINDINGS_SCHEMA = ('{"wrong": "<atom_id>", "why": "<what a user would hit, '
                   '>=12 chars>"}')


def _parse_findings(text: str, kb) -> list:
    out = []
    for line in (text or "").splitlines():
        line = line.strip().rstrip(",")
        if not (line.startswith("{") and line.endswith("}")):
            continue
        try:
            o = json.loads(line)
        except ValueError:
            continue
        atom = str(o.get("wrong", ""))
        why = str(o.get("why", "")).strip()
        if atom in kb.concepts and len(why) >= 12:
            out.append({"wrong": atom, "why": why[:300]})
    return out


def _observation_prompt(kb, regions, tissue_texts) -> str:
    return (f"You are auditing the {kb.subject!r} knowledge module AS A USER "
            "who just relied on it. Below are its warmest regions' contents. "
            "Name CONCRETE wrongness only — claims a user would trip over "
            "(factually off, misleadingly framed, missing a load-bearing "
            "caveat). NOT style, NOT gaps (gaps are the worklist's job).\n\n"
            + "\n\n".join(f"### {r}\n{t[:2500]}"
                          for r, t in tissue_texts.items())
            + "\n\nReply ONLY JSONL, one finding per line (empty reply = no "
            f"findings):\n{FINDINGS_SCHEMA}\nNo prose, no fences.")


async def observation_pass(kb, brain, deps, max_regions: int = 3,
                           attempts: int = 2) -> dict:
    """Gather warmest tissue → one seat names wrongness → price each via the
    consumers-cone → file kb-supersede issues. Returns the findings report."""
    from ee_v2.kbc.kb_tool import relative_root
    regions = brain.regions()[:max_regions]
    if not regions:
        return {"findings": 0, "issues": []}
    tissue = {}
    for r in regions:
        d = brain.root / "tissue" / r
        tissue[r] = "\n".join(p.read_text(encoding="utf-8")
                              for p in sorted(d.glob("*.md"))[:6])
    prompt = _observation_prompt(kb, regions, tissue)
    findings = []
    for attempt in range(attempts):
        seat = deps.host.named_seat_factory("observer")
        out = seat.run(prompt)
        out = await out if asyncio.iscoroutine(out) else out
        text = out if isinstance(out, str) else str(out)
        if not text.strip():
            findings = []                     # honest empty = no findings
            break
        findings = _parse_findings(text, kb)
        if findings or "{" not in text:
            break
        prompt += ("\n\nPROOF RESIDUE — your reply contained no parseable "
                   "findings. Emit the exact JSONL schema or an empty reply.")
    issues = []
    for f in findings:
        cone = relative_root(kb, f["wrong"], direction="consumers",
                             max_nodes=50)
        price = len(cone)
        url = deps.issue_filer(
            f"kb-supersede: {f['wrong']} ({kb.subject})",
            f"OBSERVED WRONGNESS (self-audit): {f['why']}\n\n"
            f"Blast radius (consumers-cone): {price} atoms — the regret, "
            "priced. Per §18b: build the replacement region, re-ground each "
            "consumer, never retract; the graveyard keeps this as a "
            "hard-negative once superseded.",
            "kb-supersede")
        issues.append({"atom": f["wrong"], "price": price, "url": url})
    return {"findings": len(findings), "issues": issues}
