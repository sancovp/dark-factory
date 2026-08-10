#!/usr/bin/env python3
"""atlas.py — THE KB ATLAS: the auto-generated website of the dark floor
(Isaac 2026-08-10: "how do we link them all and show the graph? that should
be the website. the workflow should auto make pages for each kb").

For every published module: one page with the INTERACTIVE GRAPH (certified
atoms ringed gold), the numbers, and the links (repo · marketplace · .ttl).
The index is the shelf; cross-KB same-name atoms are surfaced as CANDIDATE
bridges (never claimed as identity — same word is not same concept until
proven); combined.html draws the whole floor with bridges dashed.

Stdlib-only; self-contained vanilla-JS force graph (no CDN — the site works
from a cave). Deploys by mirroring the built site into the public
sancovp/kb-atlas repo (GitHub Pages)."""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import time
from collections import Counter
from pathlib import Path

SITE_REPO = "sancovp/kb-atlas"
VIZ_CAP = 600          # per-module page: top-N by degree when bigger
COMBINED_CAP = 120     # per-module share of the combined floor


def _run(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)}: {(r.stderr or r.stdout)[-300:]}")
    return r


# ── discovery ────────────────────────────────────────────────────────────────
def load_module(mod_dir: Path) -> dict | None:
    entry_p = mod_dir / "marketplace-entry.json"
    if not entry_p.exists():
        return None
    entry = json.loads(entry_p.read_text())
    data = None
    for using in (mod_dir / "skills").glob("using-*"):
        if (using / "data" / "concepts.jsonl").exists():
            data = using / "data"
            break
    if data is None:
        return None
    concepts, relations = {}, []
    for line in (data / "concepts.jsonl").read_text().splitlines():
        o = json.loads(line)
        concepts[o["c"]] = o["d"]
    for line in (data / "relations.jsonl").read_text().splitlines():
        s, t = json.loads(line)
        relations.append((s, t))
    certified = set()
    hyper = data / "hyperedges.jsonl"
    n_cert = 0
    if hyper.exists():
        for line in hyper.read_text().splitlines():
            h = json.loads(line)
            certified.update(h["atoms"])
            n_cert += 1
    n_skel = 0
    skel = data / "skeletons.jsonl"
    arg_edges = []
    if skel.exists():
        for line in skel.read_text().splitlines():
            sk = json.loads(line)
            n_skel += 1
            arg_edges += [(op, s, t) for op, s, t in sk["edges"]]
    meter = None
    log = data / "automaton_log.jsonl"
    if log.exists():
        calls = [json.loads(x)["llm_calls"]
                 for x in log.read_text().splitlines() if x]
        if calls:
            meter = {"statements": len(calls),
                     "calls_per_statement": round(sum(calls) / len(calls), 3),
                     "last5": round(sum(calls[-5:]) / len(calls[-5:]), 3)}
    slug = entry["name"].replace("-module", "").replace("-", "_")
    n_skills = sum(1 for d in (mod_dir / "skills").iterdir()
                   if (d / "SKILL.md").exists())
    return {"slug": slug, "entry": entry, "concepts": concepts,
            "relations": relations, "certified": certified,
            "n_cert": n_cert, "n_skel": n_skel, "arg_edges": arg_edges,
            "n_skills": n_skills, "meter": meter,
            "repo_url": entry["source"]["url"].removesuffix(".git")}


def graph_json(m: dict, cap: int) -> dict:
    deg = Counter()
    for s, t in m["relations"]:
        deg[s] += 1
        deg[t] += 1
    ids = sorted(m["concepts"], key=lambda c: -deg[c])
    shown = set(ids[:cap])
    nodes = [{"id": c, "label": c.replace("_", " "),
              "def": m["concepts"][c][:180], "deg": deg[c],
              "cert": c in m["certified"]} for c in ids[:cap]]
    args = {(s, t): op for op, s, t in m["arg_edges"]}
    links = [{"s": s, "t": t, "op": args.get((s, t)) or args.get((t, s))}
             for s, t in m["relations"] if s in shown and t in shown]
    return {"nodes": nodes, "links": links,
            "total": len(m["concepts"]), "shown": len(nodes)}


# ── templates ────────────────────────────────────────────────────────────────
CSS = """
:root{--bg:#0a0a0f;--panel:#12121a;--ink:#d8d8e0;--dim:#71718a;
--gold:#e8b64c;--acc:#5ac8a8;--line:#26263a}
*{box-sizing:border-box;margin:0}
body{background:var(--bg);color:var(--ink);
font:15px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
header{padding:28px 32px 10px}h1{font-size:22px;letter-spacing:.04em}
.sub{color:var(--dim);margin-top:6px;max-width:70ch}
.stats{display:flex;gap:26px;flex-wrap:wrap;padding:14px 32px}
.stat b{font-size:20px;color:var(--gold)}.stat span{color:var(--dim);font-size:12px;display:block}
.links{padding:0 32px 12px;display:flex;gap:18px;flex-wrap:wrap;font-size:13px}
#wrap{display:flex;gap:0;border-top:1px solid var(--line)}
#cv{flex:1;min-height:72vh;cursor:grab}
aside{width:300px;border-left:1px solid var(--line);padding:16px;
max-height:78vh;overflow-y:auto;font-size:13px}
aside h3{color:var(--dim);font-size:11px;letter-spacing:.12em;margin:10px 0 8px}
.c{padding:6px 0;border-bottom:1px solid var(--line)}
.c b{color:var(--ink)}.c.gold b{color:var(--gold)}
.c small{color:var(--dim);display:block}
#tip{position:fixed;pointer-events:none;background:var(--panel);
border:1px solid var(--line);padding:8px 10px;font-size:12px;max-width:320px;
display:none;z-index:9}
#q{width:100%;background:var(--panel);border:1px solid var(--line);
color:var(--ink);padding:7px 9px;font:inherit}
footer{padding:20px 32px;color:var(--dim);font-size:12.5px;max-width:90ch}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));
gap:16px;padding:10px 32px 26px}
.card{background:var(--panel);border:1px solid var(--line);padding:18px}
.card h2{font-size:17px}.card .n{color:var(--gold)}
.card p{color:var(--dim);font-size:13px;margin:8px 0}
.bridge{color:var(--dim);font-size:13px;padding:2px 0}
.tag{border:1px solid var(--line);padding:1px 7px;font-size:11px;color:var(--dim)}
"""

JS = r"""
function atlas(canvasId, data, opts){
opts=opts||{};const cv=document.getElementById(canvasId),cx=cv.getContext('2d');
const N=data.nodes,L=data.links,idx={};N.forEach((n,i)=>idx[n.id]=i);
const E=L.map(l=>({a:idx[l.s],b:idx[l.t],op:l.op,bridge:l.bridge})).filter(e=>e.a!=null&&e.b!=null);
let W,H,tf={x:0,y:0,k:1},sel=null,hov=null,q='';
function size(){W=cv.clientWidth;H=cv.clientHeight;cv.width=W*devicePixelRatio;
cv.height=H*devicePixelRatio;cx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0)}
size();addEventListener('resize',()=>{size();draw()});
N.forEach((n,i)=>{const a=i/N.length*Math.PI*2,r=Math.min(W,H)*.35*(0.4+0.6*Math.random());
n.x=W/2+r*Math.cos(a);n.y=H/2+r*Math.sin(a);n.vx=0;n.vy=0;
n.r=3+Math.min(9,Math.sqrt(n.deg||1)*1.6)});
const adj=N.map(()=>new Set());E.forEach(e=>{adj[e.a].add(e.b);adj[e.b].add(e.a)});
let tick=0,MAX=280;
function step(){
for(let i=0;i<N.length;i++){const a=N[i];
for(let j=i+1;j<N.length;j++){const b=N[j];
let dx=a.x-b.x,dy=a.y-b.y,d2=dx*dx+dy*dy+0.01;if(d2>90000)continue;
const f=1400/d2;dx*=f;dy*=f;a.vx+=dx;a.vy+=dy;b.vx-=dx;b.vy-=dy}}
E.forEach(e=>{const a=N[e.a],b=N[e.b];let dx=b.x-a.x,dy=b.y-a.y;
const d=Math.sqrt(dx*dx+dy*dy)+0.01,f=(d-70)*0.004;dx*=f;dy*=f;
a.vx+=dx;a.vy+=dy;b.vx-=dx;b.vy-=dy});
N.forEach(n=>{n.vx+=(W/2-n.x)*0.0012;n.vy+=(H/2-n.y)*0.0012;
n.x+=n.vx*=0.82;n.y+=n.vy*=0.82})}
function draw(){cx.clearRect(0,0,W,H);cx.save();
cx.translate(tf.x,tf.y);cx.scale(tf.k,tf.k);
const dim=sel!=null;
E.forEach(e=>{const a=N[e.a],b=N[e.b];
const on=!dim||e.a===sel||e.b===sel;
cx.globalAlpha=on?(e.op?0.85:0.28):0.05;
cx.strokeStyle=e.bridge?'#e8b64c':e.op?'#5ac8a8':'#3a3a55';
cx.setLineDash(e.bridge?[4,4]:[]);cx.lineWidth=e.op?1.6:0.7;
cx.beginPath();cx.moveTo(a.x,a.y);cx.lineTo(b.x,b.y);cx.stroke()});
cx.setLineDash([]);
N.forEach((n,i)=>{const on=!dim||i===sel||adj[sel].has(i);
const hit=q&&n.id.includes(q);
cx.globalAlpha=on?1:0.12;
cx.fillStyle=n.color||'#8a8ab0';
cx.beginPath();cx.arc(n.x,n.y,n.r,0,7);cx.fill();
if(n.cert){cx.strokeStyle='#e8b64c';cx.lineWidth=1.6;
cx.beginPath();cx.arc(n.x,n.y,n.r+2.2,0,7);cx.stroke()}
if(hit){cx.strokeStyle='#fff';cx.lineWidth=1.2;
cx.beginPath();cx.arc(n.x,n.y,n.r+5,0,7);cx.stroke()}
if((i===hov||i===sel||(tf.k>1.7&&on)||hit)&&(n.deg>2||i===hov||hit)){
cx.globalAlpha=1;cx.fillStyle='#d8d8e0';cx.font='11px ui-monospace';
cx.fillText(n.label,n.x+n.r+4,n.y+3)}});
cx.restore()}
function loop(){if(tick++<MAX){step();draw();requestAnimationFrame(loop)}else draw()}
loop();
function pt(ev){const r=cv.getBoundingClientRect();
return{x:(ev.clientX-r.left-tf.x)/tf.k,y:(ev.clientY-r.top-tf.y)/tf.k}}
function near(p){let best=null,bd=144;N.forEach((n,i)=>{
const d=(n.x-p.x)**2+(n.y-p.y)**2;if(d<bd){bd=d;best=i}});return best}
const tip=document.getElementById('tip');
cv.addEventListener('mousemove',ev=>{const i=near(pt(ev));hov=i;
if(i!=null){tip.style.display='block';tip.style.left=(ev.clientX+14)+'px';
tip.style.top=(ev.clientY+10)+'px';
tip.innerHTML='<b>'+N[i].label+'</b>'+(N[i].cert?' <span style="color:#e8b64c">●certified</span>':'')+'<br>'+(N[i].def||'')+(N[i].module?'<br><i>'+N[i].module+'</i>':'')}
else tip.style.display='none';draw()});
cv.addEventListener('click',ev=>{const i=near(pt(ev));sel=(i===sel)?null:i;draw()});
let drag=null;
cv.addEventListener('mousedown',ev=>drag={x:ev.clientX,y:ev.clientY});
addEventListener('mouseup',()=>drag=null);
addEventListener('mousemove',ev=>{if(drag){tf.x+=ev.clientX-drag.x;
tf.y+=ev.clientY-drag.y;drag={x:ev.clientX,y:ev.clientY};draw()}});
cv.addEventListener('wheel',ev=>{ev.preventDefault();
const f=ev.deltaY<0?1.12:0.89;tf.k=Math.max(.25,Math.min(6,tf.k*f));draw()},{passive:false});
const qi=document.getElementById('q');
if(qi)qi.addEventListener('input',()=>{q=qi.value.trim().replace(/ /g,'_');draw()});
}
"""

MODULE_PAGE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — KB Atlas</title><link rel="stylesheet" href="style.css"></head>
<body>
<header><h1><a href="index.html">KB ATLAS</a> / {title}</h1>
<div class="sub">{desc}</div></header>
<div class="stats">{stats}</div>
<div class="links">{links}</div>
<div id="wrap"><canvas id="cv"></canvas>
<aside><input id="q" placeholder="search concepts…">
<h3>TOP CONCEPTS</h3>{top}</aside></div>
<div id="tip"></div>
<footer>Machine-grown by a KB factory; every region admitted through a
Prolog consistency gate. Gold ring = in the certificate ledger. The gate
proves <b>coherence, not truth</b> — wrongness is tracked as open supersede
issues, never silently retracted.</footer>
<script src="atlas.js"></script>
<script>fetch('data/{slug}.json').then(r=>r.json()).then(d=>atlas('cv',d));</script>
</body></html>"""

INDEX_PAGE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>KB Atlas — the dark floor</title><link rel="stylesheet" href="style.css"></head>
<body>
<header><h1>KB ATLAS</h1>
<div class="sub">Machine-grown, proof-checked knowledge organisms — compiled,
reviewed, merged, and published by an autonomous factory. Every region below
was admitted through a Prolog consistency gate; every module is a valid
Claude Code plugin with its knowledge as plain JSONL <i>and</i> OWL/Turtle.
Free. Sitting here. Running full auto.</div></header>
<div class="links"><span class="tag">combined floor: <a href="combined.html">all
modules, one graph</a></span></div>
<div class="cards">{cards}</div>
<header><h1 style="font-size:16px">CANDIDATE BRIDGES</h1>
<div class="sub">atoms sharing a name across modules — surfaced as
candidates, never claimed as identity (same word ≠ same concept until
proven)</div></header>
<div style="padding:6px 32px 20px">{bridges}</div>
<footer>The gate proves <b>coherence, not truth</b>. Factual wrongness is
expected, priced by blast radius, and metabolized through supersede issues —
never silently retracted. Domain-expert review promotes regions to trusted.
Grown by the dark floor.</footer>
</body></html>"""

COMBINED_PAGE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The floor — KB Atlas</title><link rel="stylesheet" href="style.css"></head>
<body>
<header><h1><a href="index.html">KB ATLAS</a> / the floor</h1>
<div class="sub">every module's strongest {cap} concepts on one canvas;
dashed gold = candidate bridges between modules</div></header>
<div id="wrap"><canvas id="cv"></canvas>
<aside><input id="q" placeholder="search concepts…">
<h3>MODULES</h3>{legend}</aside></div>
<div id="tip"></div>
<footer>Coherence, not truth. Grown by the dark floor.</footer>
<script src="atlas.js"></script>
<script>fetch('data/combined.json').then(r=>r.json()).then(d=>atlas('cv',d));</script>
</body></html>"""

PALETTE = ["#5ac8a8", "#c85a7a", "#5a8ac8", "#c8a85a", "#9a5ac8", "#5ac85e"]


# ── site build ───────────────────────────────────────────────────────────────
def build_site(modules: list, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    (out / "data").mkdir(exist_ok=True)
    (out / "style.css").write_text(CSS)
    (out / "atlas.js").write_text(JS)

    cards, legend_rows = [], []
    combined_nodes, combined_links = [], []
    owner = {}
    for i, m in enumerate(modules):
        g = graph_json(m, VIZ_CAP)
        (out / "data" / f"{m['slug']}.json").write_text(json.dumps(g))
        meter = (f"<div class='stat'><b>{m['meter']['calls_per_statement']}"
                 f"</b><span>LLM calls/statement (last5 "
                 f"{m['meter']['last5']})</span></div>" if m["meter"] else "")
        stats = (f"<div class='stat'><b>{len(m['concepts'])}</b>"
                 "<span>concepts</span></div>"
                 f"<div class='stat'><b>{len(m['relations'])}</b>"
                 "<span>relations</span></div>"
                 f"<div class='stat'><b>{m['n_cert']}</b>"
                 "<span>certificates</span></div>"
                 f"<div class='stat'><b>{m['n_skel']}</b>"
                 "<span>argument DAGs</span></div>"
                 f"<div class='stat'><b>{m['n_skills']}</b>"
                 "<span>skills</span></div>" + meter)
        shown_note = (f" · showing top {g['shown']} of {g['total']}"
                      if g["shown"] < g["total"] else "")
        links = (f"<a href='{m['repo_url']}'>repo</a> "
                 f"<a href='{m['repo_url']}/blob/main/skills/"
                 f"using-{m['entry']['name'].removesuffix('-module')}"
                 f"/data/module.ttl'>OWL (.ttl)</a> "
                 "<a href='https://github.com/sancovp/sancrev-marketplace'>"
                 "marketplace</a>"
                 f"<span class='tag'>gold ring = certified{shown_note}</span>")
        deg = Counter()
        for s, t in m["relations"]:
            deg[s] += 1
            deg[t] += 1
        top = "".join(
            f"<div class='c{' gold' if c in m['certified'] else ''}'>"
            f"<b>{c.replace('_', ' ')}</b>"
            f"<small>{m['concepts'][c][:110]}</small></div>"
            for c in sorted(m["concepts"], key=lambda c: -deg[c])[:20])
        (out / f"{m['slug']}.html").write_text(MODULE_PAGE.format(
            title=m["entry"]["name"], desc=m["entry"]["description"],
            stats=stats, links=links, top=top, slug=m["slug"]))
        cards.append(
            f"<div class='card'><h2><a href='{m['slug']}.html'>"
            f"{m['entry']['name']}</a></h2>"
            f"<p>{m['entry']['description'][:180]}</p>"
            f"<div>concepts <span class='n'>{len(m['concepts'])}</span> · "
            f"certificates <span class='n'>{m['n_cert']}</span> · "
            f"skills <span class='n'>{m['n_skills']}</span></div>"
            f"<p><a href='{m['slug']}.html'>graph</a> · "
            f"<a href='{m['repo_url']}'>repo</a></p></div>")
        # combined floor
        color = PALETTE[i % len(PALETTE)]
        legend_rows.append(f"<div class='c'><b style='color:{color}'>"
                           f"{m['entry']['name']}</b></div>")
        gg = graph_json(m, COMBINED_CAP)
        shown = set()
        for n in gg["nodes"]:
            nid = f"{m['slug']}:{n['id']}"
            owner.setdefault(n["id"], []).append((m["slug"], nid))
            combined_nodes.append({**n, "id": nid, "color": color,
                                   "module": m["entry"]["name"]})
            shown.add(n["id"])
        combined_links += [{"s": f"{m['slug']}:{l['s']}",
                            "t": f"{m['slug']}:{l['t']}", "op": l["op"]}
                           for l in gg["links"]]

    bridges = []
    for atom, owners in sorted(owner.items(), key=lambda x: -len(x[1])):
        if len(owners) >= 2:
            mods = [o[0] for o in owners]
            bridges.append((atom, mods))
            ids = [o[1] for o in owners]
            for a, b in zip(ids, ids[1:]):
                combined_links.append({"s": a, "t": b, "bridge": True})
    bridge_html = "".join(
        f"<div class='bridge'><b>{a.replace('_', ' ')}</b> ↔ "
        f"{' · '.join(ms)}</div>" for a, ms in bridges[:40]) or \
        "<div class='bridge'>none yet — the floor is young</div>"

    (out / "data" / "combined.json").write_text(json.dumps(
        {"nodes": combined_nodes, "links": combined_links}))
    (out / "combined.html").write_text(COMBINED_PAGE.format(
        cap=COMBINED_CAP, legend="".join(legend_rows)))
    (out / "index.html").write_text(INDEX_PAGE.format(
        cards="".join(cards), bridges=bridge_html))
    return {"modules": len(modules), "bridges": len(bridges),
            "site": str(out)}


def deploy(site: Path, repo=SITE_REPO, run=_run) -> dict:
    if run(["gh", "api", f"repos/{repo}", "--jq", ".name"],
           check=False).returncode != 0:
        run(["gh", "repo", "create", repo, "--public", "--description",
             "THE KB ATLAS — auto-generated pages + graphs for every "
             "machine-grown, proof-checked knowledge module on the dark "
             "floor"])
    with tempfile.TemporaryDirectory(prefix="atlas-") as td:
        work = Path(td) / "w"
        run(["git", "clone", "--depth", "1",
             f"https://github.com/{repo}.git", str(work)], check=False)
        if not (work / ".git").exists():
            work.mkdir(parents=True, exist_ok=True)
            run(["git", "init", "-q", "-b", "main", str(work)])
            run(["git", "remote", "add", "origin",
                 f"https://github.com/{repo}.git"], cwd=work)
        for item in work.iterdir():
            if item.name != ".git":
                run(["rm", "-rf", str(item)])
        for item in site.iterdir():
            run(["cp", "-r", str(item), str(work / item.name)])
        (work / ".nojekyll").write_text("")
        run(["git", "add", "-A"], cwd=work)
        if not run(["git", "status", "--porcelain"], cwd=work
                   ).stdout.strip():
            return {"deployed": False, "reason": "unchanged"}
        run(["git", "-c", "user.name=kb-atlas", "-c",
             "user.email=atlas@dark-factory-live", "commit", "-q", "-m",
             f"atlas rebuild ({int(time.time())})"], cwd=work)
        run(["git", "push", "-q", "origin", "main"], cwd=work)
    run(["gh", "api", "-X", "POST", f"repos/{repo}/pages", "-f",
         "source[branch]=main", "-f", "source[path]=/"], check=False)
    return {"deployed": True,
            "url": f"https://{repo.split('/')[0]}.github.io/"
                   f"{repo.split('/')[1]}/"}


def marketplace_modules(marketplace: str, skip_names: set,
                        run=_run) -> list:
    """DURABLE DISCOVERY: the catalog is the source of truth for what is
    published — clone each listed module repo and load it, so an atlas
    rebuild from ANY checkout carries every module, not just local state
    (found 2026-08-10: a state-only rebuild would have true-mirror-deleted
    restaurants)."""
    out = []
    r = run(["gh", "api",
             f"repos/{marketplace}/contents/.claude-plugin/marketplace.json",
             "--jq", ".content"], check=False)
    if r.returncode != 0:
        return out
    import base64
    cat = json.loads(base64.b64decode(r.stdout).decode())
    for e in cat.get("plugins", []):
        if e["name"] in skip_names or "-module" not in e["name"]:
            continue
        url = e.get("source", {}).get("url", "")
        if not url:
            continue
        td = Path(tempfile.mkdtemp(prefix="atlasmod-"))
        if run(["git", "clone", "--depth", "1", url, str(td / "m")],
               check=False).returncode == 0:
            m = load_module(td / "m")
            if m:
                out.append(m)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modules-root", default="kbworld/state/modules")
    ap.add_argument("--extra-module", action="append", default=[])
    ap.add_argument("--marketplace", default="sancovp/sancrev-marketplace")
    ap.add_argument("--site-repo", default=SITE_REPO)
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-deploy", action="store_true")
    a = ap.parse_args()
    modules = []
    root = Path(a.modules_root)
    if root.is_dir():
        for d in sorted(root.iterdir()):
            m = load_module(d)
            if m:
                modules.append(m)
    for x in a.extra_module:
        m = load_module(Path(x))
        if m:
            modules.append(m)
    have = {m["entry"]["name"] for m in modules}
    modules += marketplace_modules(a.marketplace, have)
    outdir = Path(a.out) if a.out else Path(tempfile.mkdtemp()) / "site"
    rep = build_site(modules, outdir)
    print(json.dumps(rep))
    if not a.no_deploy:
        print(json.dumps(deploy(outdir, a.site_repo)))


if __name__ == "__main__":
    main()
