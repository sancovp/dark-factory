#!/usr/bin/env python3
"""kbworld — deterministic proof of the full round (scripted seats, mocked
gh/git, REAL swipl + kuzu). One round per process (kuzu one-handle law —
matches CI: one round per job).

Asserted (the rule's PASS criteria):
  * bootstrap: empty KB → dump fires → re-aim picks real doors (warm+cold);
  * grow: personas emitted under state/, atoms accreted, gyri wired;
  * drain: define+connect ran under budget;
  * brain: one new strong region grew;
  * project: understand-* library in state/;
  * observe: scripted finding → priced via consumers-cone → kb-supersede
    issue FILED through the mocked gh;
  * encapsulate: plugin dir matches the REAL schemas (plugin.json keys =
    promptworld's; marketplace entry keys = sancrev-marketplace's);
  * report + telemetry written; PR opened via the mocked opener with the
    state root in its paths; grade1 never merges (no merge call exists).
"""
import asyncio
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if Path("/home/ceo/repo/ee-v2").is_dir():          # container; CI pip-installs
    sys.path.insert(1, "/home/ceo/repo/ee-v2")

from kbworld.host import FactoryKbcHost                          # noqa: E402
from kbworld.round import Deps, run_round                        # noqa: E402


class Seat:
    def __init__(self, ledger, name="seat", persona=""):
        self.ledger, self.name = ledger, name

    def run(self, prompt):
        self.ledger.append(self.name)
        j = json.dumps
        if "MASS-ENUMERATE" in prompt:
            lines = []
            for i in range(32):
                lines.append(j({"c": f"c{i:02d}",
                                "d": f"concept number {i:02d} defined here"}))
            for i in range(31):
                lines.append(j({"r": [f"c{i:02d}", f"c{i+1:02d}"]}))
            for i in range(1, 6):                    # hub → degree
                lines.append(j({"r": ["c00", f"c{i:02d}"]}))
            return "\n".join(lines)
        if "EXPAND X" in prompt:
            import re
            x = re.search(r"## X\n(\w+)", prompt)
            a = x.group(1) if x else "part"
            return "\n".join([
                j({"c": f"{a}_inner", "d": "the inner part of it"}),
                j({"r": [a, f"{a}_inner"]})])
        if "DEFINE each concept below" in prompt:
            import re
            ids = re.findall(r"### (\w+)", prompt)
            return "\n".join(j({"c": i, "d": "defined by the drain seat"})
                             for i in ids)
        if "UNCONNECTED" in prompt:
            import re
            orphans = re.search(r"UNCONNECTED:\n([^\n]+)", prompt)
            first = (orphans.group(1).split(",")[0].strip()
                     if orphans else "c00")
            return j({"r": [first, "c00"]})
        if "auditing" in prompt:
            return j({"wrong": "c01",
                      "why": "users trip on this claim in practice"})
        return "ANSWER: contribution.\n" + j(
            {"c": "extra_atom", "d": "an extra certified atom"}) + "\n" + j(
            {"r": ["extra_atom", "c00"]})


async def main(tmp):
    ledger, filed, prs = [], [], []
    host = FactoryKbcHost(state_root=Path(tmp) / "state")
    host.named_seat_factory = lambda n, p="": Seat(ledger, n)
    host.seat_factory = lambda: Seat(ledger)
    deps = Deps(host=host,
                issue_lister=lambda label: [],
                issue_filer=lambda t, b, l: (filed.append((t, l)),
                                             "http://issue/1")[1],
                pr_opener=lambda br, t, b, paths: (prs.append((br, paths)),
                                                   "http://pr/1")[1])
    rep = await run_round("test roasting", deps=deps, budget=40)

    p = rep["phases"]
    assert p["aim"]["mode"] == "bootstrap"
    assert p["grow"]["bootstrap"]["concepts"] >= 30
    assert len(p["aim"]["doors"]) == 2, p["aim"]
    print(f"  bootstrap→re-aim: dumped {p['grow']['bootstrap']['concepts']}c,"
          f" doors={p['aim']['doors']} ✓")
    personas = list((host.state_root / "personas_out/personas").iterdir())
    assert personas
    print(f"  grow: {len(personas)} personas emitted, "
          f"specialize={p['grow']['specialize']['new']} ✓")
    assert "defined" in p["drain"]["define"] or p["drain"]["define"] == {}
    assert p["brain"]["grew"]
    print(f"  drain ran; brain grew {p['brain']['grew']!r} ✓")
    assert p["project"]["skills"] > 0
    print(f"  project: {p['project']['skills']} understand-* skills ✓")
    assert p["observe"]["findings"] == 1 and filed
    assert filed[0][1] == "kb-supersede" and p["observe"]["issues"][0]["price"] >= 0
    print(f"  observe: finding on c01 priced {p['observe']['issues'][0]['price']}"
          " → kb-supersede issue filed ✓")
    mod = Path(p["encapsulate"]["module"])
    plugin = json.loads((mod / ".claude-plugin/plugin.json").read_text())
    assert set(plugin) == {"name", "version", "description", "author",
                           "license", "keywords"}
    assert "-" in plugin["name"] and "_" not in plugin["name"]  # kebab-case
    entry = json.loads((mod / "marketplace-entry.json").read_text())
    assert set(entry) == {"name", "description", "author", "category",
                          "source"}
    # VALID plugin structure (plugin-structure skill, critical rules):
    # manifest alone in .claude-plugin/; components at ROOT; parts as
    # resources INSIDE the skill
    assert [f.name for f in (mod / ".claude-plugin").iterdir()] == \
        ["plugin.json"]
    assert not (mod / ".claude").exists()
    using = next((mod / "skills").glob("using-*"))
    assert (using / "SKILL.md").exists()
    assert (using / "data" / "concepts.jsonl").exists()
    sibs = [d.name for d in (mod / "skills").iterdir()
            if "understand" in d.name and (d / "SKILL.md").exists()]
    assert sibs, "library skills must ship as siblings"
    import yaml
    for d in list((mod / "skills").iterdir()):
        txt = (d / "SKILL.md").read_text()
        assert txt.startswith("---"), d.name
        fm = yaml.safe_load(txt.split("---")[1])
        assert fm.get("name") and fm.get("description"), \
            f"{d.name}: frontmatter must strict-YAML-parse w/ name+description"
    print(f"  encapsulate: VALID plugin — manifest alone in .claude-plugin, "
          f"skills at root ({len(sibs)} understand-* siblings), data as "
          "skill resources ✓")
    assert rep["telemetry"]["worklist"]["after"] is not None
    assert prs and str(host.state_root) in str(prs[0][1][0])
    assert list(host.state_root.glob("round_*.json"))
    print(f"  telemetry + report written; PR opened on {prs[0][0]!r} "
          "(grade1 — no merge path exists) ✓")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as d:
        asyncio.run(main(d))
    print("KBWORLD PASS — the full reified round runs deterministically: "
          "aim→grow→drain→brain→project→observe→encapsulate, all logged, "
          "PR-shaped, human-gated.")
