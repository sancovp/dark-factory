"""observe.py — THE OBSERVATION PASS (§22.4: observation replaces control).

A seat reads the module's own recent regions IN USE (round reports, teach
events, retrieval logs from state/events.jsonl) and names wrongness — which
becomes supersede-issues (§18b: never retract, supersede; consumers-cone
prices the regret). The deity retrospective (factory.run_cycle) later mints
standing rules from these logs."""
from __future__ import annotations


async def observation_pass(host, kb, brain) -> dict:
    """TODO(fill §22.4):
    1. gather: last N round reports + events.jsonl tail + warmest regions
    2. one seat: 'read these regions AS A USER would; name concrete
       wrongness (not style) with the atom ids' → typed list
    3. for each finding: relative_root(consumers) → priced; file a
       `kb-supersede` issue via gh (maintainer-gated repo, safe)
    4. return {"findings": n, "issues_filed": [...]}"""
    raise NotImplementedError("fill: kbworld rule step 6")
