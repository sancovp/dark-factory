"""encapsulate.py — PHASE g: THE MODULE SHIPS ITS OWN MANUAL (§23).

One universal template; content projected from the certified KB; the module
repo becomes a Claude Code plugin (Garage metaformat: plugins in their own
repos, marketplace points at them). RULE-1 at product level: a capability
that isn't a skill doesn't exist — so the machine emits the skill."""
from __future__ import annotations

from pathlib import Path

USING_SKILL_TEMPLATE = """---
name: using-{slug}
description: "Use the {subject} neurosymbolic module: RAG library, agent brain, growable KB — proof-checked"
---

# using-{slug}

This module is a CULTIVATED, PROOF-CHECKED knowledge organism about
**{subject}** ({n_concepts} concepts / {n_relations} relations; grown by a
KB factory — every region admitted by a Prolog consistency gate, wrongness
tracked as open supersede-issues, never hidden).

## The four ways to use it

1. **As RAG** — the library at `{library_path}`: `understand-{{x}}` skills,
   coordinate-addressed; FTS5 index via `skilltree.build_index`. Call number
   = home class : dependency facets (the import web, literally).
2. **As an agent** — `brain_ask("your question")`: the activation graph fires
   the matching gyri numerically, each answers over its territory, the
   synthesis is PROVEN one level up (SES tower) and returns with receipts.
3. **As tools your agents hold** — `ee_v2.kbc.heaven_tools.make_kbc_tools`
   over this module's state root: 14 heaven tools (kb_*, kernel_*, brain_*).
   Hand them to any heaven agent's `tools=[...]`.
4. **As a factory** — the kbworld round deepens this module on a schedule;
   file a `kb-door` issue to point it somewhere; file `kb-supersede` when
   you catch it being wrong (it also catches itself — see the round reports).

## Etiquette (the laws this module lives under)

- The prover admits; you never hand-edit certified state (file issues).
- Wrongness is fuel: a wrong-but-coherent region is a PENDING OBSERVATION —
  say what you saw, the next round metabolizes it.
- The worklist is honest: `kb_work` shows exactly what the module knows it
  doesn't know.

## The map

{call_number_index}
"""


def emit_module_skill(kb, state_root) -> dict:
    """TODO(fill §23): render USING_SKILL_TEMPLATE from the KB (slug,
    counts, library path, top-level call-number index), write to
    state/plugin/skills/using-{slug}/SKILL.md + the plugin manifest
    (.claude-plugin marketplace format — mirror sancovp/garage's shape,
    READ IT FIRST, do not invent the manifest schema). Return paths."""
    raise NotImplementedError("fill: kbworld rule step 7")
