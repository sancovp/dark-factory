"""encapsulate.py — PHASE g: THE MODULE SHIPS ITS OWN MANUAL (§23).

One universal template; content projected from the certified KB; the module
becomes a VALID Claude Code plugin (structure per the official plugin-dev
plugin's `plugin-structure` skill, read 2026-08-10 from
anthropics/claude-plugins-official — not invented):

    <slug>-module/
    ├── .claude-plugin/plugin.json     # manifest — the ONLY thing in here
    ├── marketplace-entry.json         # ready-to-paste marketplace row
    └── skills/                        # components at ROOT (critical rule 2)
        ├── using-<slug>/
        │   ├── SKILL.md
        │   ├── data/                  # the KB + ledgers AS SKILL RESOURCES
        │   └── references/            # skilltree index, receipts
        └── understand-*/              # the projected library = sibling
            └── SKILL.md               #   skills, auto-discovered

RULE-1 at product level: a capability that isn't a skill doesn't exist — so
the machine emits the skills, and every data part rides INSIDE a skill as a
resource (Isaac's correction 2026-08-10), never as a loose root dir."""
from __future__ import annotations

import json
import re
import shutil
from collections import Counter
from pathlib import Path

USING_SKILL_TEMPLATE = """---
name: using-{slug}
description: "Use the {subject} neurosymbolic module: RAG library, agent brain, growable KB — proof-checked"
version: 0.1.0
---

# using-{slug}

This module is a CULTIVATED, PROOF-CHECKED knowledge organism about
**{subject}** ({n_concepts} concepts / {n_relations} relations; grown by a
KB factory — every region admitted by a Prolog consistency gate, wrongness
tracked as open supersede-issues, never hidden).

## The four ways to use it

1. **As RAG** — the sibling `understand-{{x}}` skills in this plugin,
   coordinate-addressed (call number = home class : dependency facets — the
   import web, literally); FTS5 index via `skilltree.build_index` over
   `${{CLAUDE_PLUGIN_ROOT}}/skills/using-{slug}/references/skilltree.json`.
2. **As an agent** — `brain_ask("your question")`: the activation graph fires
   the matching gyri numerically, each answers over its territory, the
   synthesis is PROVEN one level up (SES tower) and returns with receipts.
3. **As tools your agents hold** — `ee_v2.kbc.heaven_tools.make_kbc_tools`
   over this module's data root
   (`${{CLAUDE_PLUGIN_ROOT}}/skills/using-{slug}/data/`): 14 heaven tools
   (kb_*, kernel_*, brain_*). Hand them to any heaven agent's `tools=[...]`.
4. **As a factory** — the kbworld round deepens this module on a schedule;
   file a `kb-door` issue to point it somewhere; file `kb-supersede` when
   you catch it being wrong (it also catches itself — see the round reports).

## The data resources (all inside THIS skill)

- `data/concepts.jsonl` + `data/relations.jsonl` — the certified graph
- `data/hyperedges.jsonl` — the certificate ledger (the automaton's KNOWN)
- `data/skeletons.jsonl` — certified argument DAGs (because/since/…)
- `data/worklist.json` — what the module knows it doesn't know
- `references/skilltree.json` — the library index

## Etiquette (the laws this module lives under)

- The prover admits; you never hand-edit certified state (file issues).
- Wrongness is fuel: a wrong-but-coherent region is a PENDING OBSERVATION —
  say what you saw, the next round metabolizes it.
- The worklist is honest: `kb_work` shows exactly what the module knows it
  doesn't know.

## The map

{call_number_index}
"""


def _normalize_frontmatter(skill_md: Path) -> None:
    """Skilltree emits `description: [0.8.4] …` unquoted — YAML reads the
    bracketed call number as a flow sequence and strict parsers reject the
    file (caught by the 2026-08-10 verify pass; upstream issue filed on
    sancovp/skilltree). The harvest guarantees valid plugin output: quote
    any unquoted flow-ish scalar in the frontmatter."""
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return
    out, changed = [], False
    for i, ln in enumerate(lines):
        if 0 < i and ln.strip() == "---":
            out.extend(lines[i:])
            break
        m = re.match(r"^(name|description):\s*(\[.*)$", ln)
        if m:
            val = m.group(2).replace('"', r'\"')
            out.append(f'{m.group(1)}: "{val}"')
            changed = True
        else:
            out.append(ln)
    if changed:
        skill_md.write_text("\n".join(out) + "\n", encoding="utf-8")


def emit_module_skill(kb, modules_root, library_root=None) -> dict:
    """Render the module as a VALID plugin. plugin.json fields follow the
    plugin-structure skill's recommended metadata; the marketplace entry
    mirrors sancrev-marketplace's plugins[] shape (kept at root as the
    ready-to-paste row — it is marketplace data, not a plugin component).
    All data parts ship as RESOURCES inside the using-* skill; the
    understand-* library ships as sibling skills (auto-discovered)."""
    from ee_v2.kbc.projector import call_number

    slug = re.sub(r"[^a-z0-9_]+", "_", kb.subject.lower()).strip("_")[:40]
    kebab = slug.replace("_", "-")
    mod = Path(modules_root) / slug
    skill_dir = mod / "skills" / f"using-{kebab}"
    (skill_dir / "data").mkdir(parents=True, exist_ok=True)
    (skill_dir / "references").mkdir(parents=True, exist_ok=True)
    (mod / ".claude-plugin").mkdir(parents=True, exist_ok=True)

    deg = Counter()
    for s_, t_ in kb.relations:
        deg[s_] += 1
        deg[t_] += 1
    top = sorted(kb.concepts, key=lambda c: -deg[c])[:12]
    index = "\n".join(f"- `{call_number(kb, c)[0]}`" for c in top)

    skill = USING_SKILL_TEMPLATE.format(
        slug=kebab, subject=kb.subject,
        n_concepts=len(kb.concepts), n_relations=len(kb.relations),
        call_number_index=index)
    (skill_dir / "SKILL.md").write_text(skill, encoding="utf-8")

    # the parts ride as resources IN the skill (never loose root dirs)
    for f in sorted(Path(kb.root).glob("*.jsonl")):
        shutil.copy(f, skill_dir / "data" / f.name)
    # PSC-with-OWL-PROJECTED (Isaac 2026-08-10): the module carries its KB
    # as standards-compliant Turtle too; the proof gate stays Prolog
    from ee_v2.kbc.owl import project_owl
    owl_rep = project_owl(kb, skill_dir / "data" / "module.ttl")
    wl = Path(kb.root) / "worklist.json"
    if wl.exists():
        shutil.copy(wl, skill_dir / "data" / "worklist.json")

    # HARVEST the skilltree: the library projects dir-is-the-loadout
    # (each node dir carries .claude/skills/<call-number>-understand-<x>/);
    # a plugin wants those FLAT at root skills/ — kebab-sanitized, unique by
    # call number
    n_lib = 0
    if library_root and Path(library_root).is_dir():
        tree = Path(library_root) / "skilltree.json"
        if tree.exists():
            shutil.copy(tree, skill_dir / "references" / "skilltree.json")
        for sk in sorted(Path(library_root).glob(
                "**/.claude/skills/*/SKILL.md")):
            src_dir = sk.parent
            kname = re.sub(r"[^a-z0-9-]+", "-",
                           src_dir.name.lower()).strip("-")
            dst = mod / "skills" / kname
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src_dir, dst)
            _normalize_frontmatter(dst / "SKILL.md")
            n_lib += 1

    plugin = {"name": f"{kebab}-module", "version": "0.1.0",
              "description": (f"{kb.subject} — a cultivated, proof-checked "
                              "neurosymbolic knowledge module: RAG library, "
                              "agent brain, growable KB, factory-deepened. "
                              f"{len(kb.concepts)} concepts."),
              "author": {"name": "Isaac Wostrel-Rubin"},
              "license": "UNLICENSED",
              "keywords": ["knowledge-base", "neurosymbolic", kebab]}
    (mod / ".claude-plugin" / "plugin.json").write_text(
        json.dumps(plugin, indent=2), encoding="utf-8")

    entry = {"name": f"{kebab}-module", "description": plugin["description"],
             "author": {"name": "Isaac Wostrel-Rubin"}, "category": "productivity",
             "source": {"source": "url",
                        "url": (f"https://github.com/sancovp/{kebab}"
                                "-module.git")}}
    (mod / "marketplace-entry.json").write_text(
        json.dumps(entry, indent=2), encoding="utf-8")

    # the README receipt — the module explains itself to a human reader
    def _count(fname):
        p = Path(kb.root) / fname
        return len(p.read_text().splitlines()) if p.exists() else 0

    readme = (
        f"# {plugin['name']} — a cultivated, proof-checked knowledge "
        "organism\n\n"
        "This repository was **grown, not written** — and it is a valid "
        "Claude Code **plugin**. It is a neurosymbolic knowledge module "
        f"about **{kb.subject}**, produced end-to-end by a KB factory: "
        "every region admitted through a Prolog consistency gate, gaps "
        "enumerated by the prover (not hidden), wrongness tracked as open "
        "supersede issues rather than silently edited away.\n\n"
        "## The numbers\n\n"
        f"- **{len(kb.concepts)} concepts / {len(kb.relations)} relations**, "
        "every region gate-admitted\n"
        f"- **{n_lib} `understand-*` skills** harvested from the projected "
        "library (call-number-addressed — the coordinate is the dependency "
        "web)\n"
        f"- **{_count('hyperedges.jsonl')} certified hyperedges** (the "
        "language automaton's KNOWN vocabulary) · "
        f"**{_count('skeletons.jsonl')} certified argument skeletons**\n\n"
        "## Use it\n\n"
        f"Install as a plugin (skills auto-discover) or read "
        f"`skills/using-{kebab}/SKILL.md` — the four ways (RAG / agent "
        "brain / heaven tools / factory) plus the module's etiquette. The "
        f"knowledge substrate lives at `skills/using-{kebab}/data/` as "
        "plain JSONL.\n\n"
        "## The graph + the OWL\n\n"
        f"- **Interactive graph**: "
        f"https://sancovp.github.io/kb-atlas/{slug}.html "
        "(the KB Atlas — auto-generated pages for every module on the "
        "floor)\n"
        f"- **OWL/Turtle**: `skills/using-{kebab}/data/module.ttl` — "
        f"{owl_rep['concepts']} typed individuals, "
        f"{owl_rep['certificates']} reified certificates, "
        f"{owl_rep['argument_edges']} typed argument edges. The proof gate "
        "underneath stays Prolog; the OWL is a faithful projection.\n\n"
        "## Honesty note\n\n"
        "The gate proves **coherence, not truth**: content is "
        "LLM-cultivated and machine-checked for closure, connectedness, "
        "groundedness, and warrant structure. Factual wrongness is "
        "expected, priced (by consumer-cone size), and metabolized through "
        "supersede issues — never silently retracted. Domain-expert review "
        "is what promotes any region to trusted.\n")
    (mod / "README.md").write_text(readme, encoding="utf-8")
    return {"module": str(mod), "skill": str(skill_dir / "SKILL.md"),
            "plugin": plugin["name"], "library_skills": n_lib}
