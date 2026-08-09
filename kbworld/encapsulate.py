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


def emit_module_skill(kb, modules_root) -> dict:
    """Render the universal skill + plugin manifest from the KB. Manifest
    schemas mirrored from the REAL precedents (read 2026-08-10, not
    invented): plugin.json = sancovp/promptworld/.claude-plugin/plugin.json
    {name, version, description, author}; the marketplace entry =
    sancovp/sancrev-marketplace/.claude-plugin/marketplace.json plugins[]
    {name, description, author, category, source:{source:"url", url}}.
    v1 emits the plugin dir NESTED under state/modules/<slug>/ — the Garage
    metaformat wants plugins in their OWN repos; splitting out is a later
    mechanical move (the marketplace entry ships ready, url = placeholder)."""
    import json
    import re
    from collections import Counter

    from ee_v2.kbc.projector import call_number

    slug = re.sub(r"[^a-z0-9_]+", "_", kb.subject.lower()).strip("_")[:40]
    mod = Path(modules_root) / slug
    skill_dir = mod / ".claude" / "skills" / f"using-{slug}"
    skill_dir.mkdir(parents=True, exist_ok=True)
    (mod / ".claude-plugin").mkdir(parents=True, exist_ok=True)

    deg = Counter()
    for s_, t_ in kb.relations:
        deg[s_] += 1
        deg[t_] += 1
    top = sorted(kb.concepts, key=lambda c: -deg[c])[:12]
    index = "\n".join(f"- `{call_number(kb, c)[0]}`" for c in top)

    skill = USING_SKILL_TEMPLATE.format(
        slug=slug, subject=kb.subject,
        n_concepts=len(kb.concepts), n_relations=len(kb.relations),
        library_path=f"kbworld/state/libraries/{slug}",
        call_number_index=index)
    (skill_dir / "SKILL.md").write_text(skill, encoding="utf-8")

    plugin = {"name": f"{slug}-module", "version": "0.1.0",
              "description": (f"{kb.subject} — a cultivated, proof-checked "
                              "neurosymbolic knowledge module: RAG library, "
                              "agent brain, growable KB, factory-deepened. "
                              f"{len(kb.concepts)} concepts."),
              "author": {"name": "Isaac Rubin"}}
    (mod / ".claude-plugin" / "plugin.json").write_text(
        json.dumps(plugin, indent=2), encoding="utf-8")

    entry = {"name": f"{slug}-module", "description": plugin["description"],
             "author": {"name": "Isaac Rubin"}, "category": "productivity",
             "source": {"source": "url",
                        "url": f"https://github.com/sancovp/{slug}-module.git"
                               "  # placeholder until split to own repo"}}
    (mod / "marketplace-entry.json").write_text(
        json.dumps(entry, indent=2), encoding="utf-8")
    return {"module": str(mod), "skill": str(skill_dir / "SKILL.md"),
            "plugin": plugin["name"]}
