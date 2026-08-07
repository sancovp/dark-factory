"""The WoS team wiring — PORTED from cave-teams' test_live_skillcraft.py (the
proven live run: SkillcraftWorld drives MiniMax players + a deity adjudicator).

Nothing new here: WoSPlayer / WoSDeity / the MPE method / the JSON parser are
the same wiring, parametrized by agents_root/quests_root instead of module
globals so the factory can run several worlds (dev, control, treatment) side
by side. Players are TOOLED heaven agents (Bash + file edit) embodied in their
agent dirs — each dir seeded from world-of-skillcraft/agents/_template with
its full .claude loadout (test_skill, execute_in_game, skill_types, meta-PE…).
"""
from __future__ import annotations

import json
import os

from cave_teams.chain_ontology import Link, LinkResult, LinkStatus
from cave_teams.skillcraft import post_bulletin, validate_bug
from cave_teams.examples import MiniMaxRuntime

# Meta-Prompt Engineering — the SANCREV/CIG skill's operational core, inlined
# (MiniMax has no skill auto-load). Source: the WoS agent template /
# sra-git/not-unified/cig/.claude/skills/meta-prompt-engineering/.
MPE = (
    "META-PROMPT ENGINEERING — apply this BEFORE you decide or judge:\n"
    "A) INDEPENDENT VERIFICATION: never trust a claim's own label. A seller's 'epic' rarity, a "
    "filed bug, a skill's quality — verify against the actual artifact/rules, not the claim. Try the "
    "alternative reading (if 'epic' fits, is 'uncommon' equally defensible?).\n"
    "B) REFLEXIVE APPLICATION: run the same check on your OWN judgment that you run on theirs — "
    "state your reasoning, then find where it could be wrong.\n"
    "C) SURFACE→PROCESS: does the surface form actually produce the function it implies? A skill "
    "that LOOKS like a recipe may compose nothing; a plausible-sounding bug may not be exploitable. "
    "Check the process, not the appearance.\n"
    "Context-sensitivity: same structure can yield different outcomes by input — judge the specific case.")


def _spans(text):
    depth = start = 0; in_s = esc = False; out = []
    for i, ch in enumerate(text or ""):
        if in_s:
            esc = (ch == "\\" and not esc)
            if ch == '"' and not esc: in_s = False
            continue
        if ch == '"': in_s = True
        elif ch == "{":
            if depth == 0: start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0: out.append(text[start:i + 1])
    return out


def last_json(text, keys=("type", "action"), default=None):
    for blob in reversed(_spans(text)):
        try:
            o = json.loads(blob)
            if isinstance(o, dict) and any(k in o for k in keys):
                return o.get("action", o) if "action" in o else o
        except Exception:
            continue
    return default if default is not None else {"type": "search"}


def _available_quests(quests_root):
    out = []
    for fn in sorted(os.listdir(quests_root)):
        if not fn.endswith(".md"):
            continue
        body = open(os.path.join(quests_root, fn)).read()
        ask = next((l for l in body.splitlines()
                    if l and not l.startswith("#") and "Reward" not in l), "")
        reward = next((tok for tok in body.split() if tok.isdigit()), "?")
        out.append({"quest_id": fn[:-3], "ask": ask.strip()[:90],
                    "reward": f"{reward}g"})
    return out


class WoSPlayer(Link):
    """A player: a tooled MiniMax agent embodied in its dir. Full WoS move set."""

    def __init__(self, name, agents_root, quests_root, extra_note=""):
        self.name = name
        self.agents_root = agents_root
        self.quests_root = quests_root
        self.rt = MiniMaxRuntime(name=name, tools=None, max_tool_calls=25, system_prompt=(
            f"You are {name}, a player in World of Skillcraft — an economy where agents craft REAL, "
            f"executable Claude Code skills (markdown files), trade them, do quests, form parties, and "
            f"audit the game for exploits. Your agent dir is {agents_root}/{name} (it has your .claude "
            f"loadout: skill_types, test_skill, meta-PE). You have Bash + file editing.\n\n{MPE}\n\n"
            + (extra_note + "\n\n" if extra_note else "")
            + "Apply the method above before you choose your move (verify a listing's real quality "
              "before buying; check your own strategy for convergence). Reply with ONE JSON action "
              "and nothing else."))

    async def execute(self, ctx=None, **k):
        c = dict(ctx or {}); b = c.get("board", {})
        me = b.get("agents", {}).get(self.name, {})
        others = [l for l in b.get("trade_board", []) if l["seller"] != self.name]
        my_quests = [q for q in b.get("quest_log", {}).get(self.name, [])]
        active = [q["quest_id"] for q in my_quests if q.get("status") == "active"]
        parties = [{"party_id": p["party_id"], "leader": p["leader"],
                    "looking_for": p.get("looking_for")}
                   for p in b.get("lfg_board", [])]
        A, n = self.agents_root, self.name
        prompt = (
            f"SEASON {b.get('season', {}).get('number')} — your turn.\n"
            f"You: gold={me.get('gold')}, skills_crafted={me.get('skills_crafted')}, "
            f"quests_completed={me.get('quests_completed')}.\n"
            f"Deity bulletin: {[x['message'] for x in b.get('deity_bulletin', [])][-2:]}\n"
            f"Listings to BUY: {[{'id': l['listing_id'], 'skill': l['skill_path'], 'price': l['price']} for l in others]}\n"
            f"Available quests: {_available_quests(self.quests_root)}\n"
            f"Your ACTIVE quests: {active}\n"
            f"Parties (LFG): {parties}\n\n"
            "Take ONE action. The DEITY rewards DIVERGENCE and punishes everyone doing the same move — "
            "vary your play. To craft, first write the file(s) with your tools, then reply the JSON:\n"
            f"• CRAFT+SELL: write {A}/{n}/crafted/<snake>.md + a test record "
            f"{A}/{n}/crafted/.tests/<id>.json "
            '({"test_id":"<id>","skill_path":"crafted/<snake>.md","result":"pass"}), then reply '
            '{"type":"trade_post","skill_path":"crafted/<snake>.md","price":<int>,"test_id":"<id>","rarity":"<common|uncommon|rare|epic>","description":"<line>"}\n'
            '• BUY: {"type":"trade_buy","listing_id":"<id>"}\n'
            '• ACCEPT a quest (they pay well): {"type":"quest_accept","quest_id":"<id>"}\n'
            "• COMPLETE an ACTIVE quest — craft the skill it asks for first, then "
            '{"type":"quest_complete","quest_id":"<id>","skill_path":"crafted/<snake>.md"}\n'
            '• Form a party: {"type":"lfg_post","specializations":"<what you offer>","looking_for":"<what you need>"} '
            'or join one: {"type":"lfg_join","party_id":"<id>"}\n'
            "• AUDIT this economy for a real exploit (a way to gain gold/skills unfairly) and file it for a "
            '100g bounty: {"type":"bug_report","title":"<short>","description":"<the flaw>","reproduction":"<steps>","severity":"<low|med|high>"}\n'
            "Reply ONLY the JSON.")
        out = await self.rt.run(prompt)
        c["action"] = last_json(out if isinstance(out, str) else str(out))
        return LinkResult(status=LinkStatus.SUCCESS, context=c)


class WoSDeity(Link):
    """The deity — the blackboard's adjudicator: narrate, watch for convergence,
    rule on rarity challenges, VALIDATE bug reports (the advance then pays)."""
    name = "deity"

    def __init__(self):
        self.rt = MiniMaxRuntime(name="deity", tools=[], system_prompt=(
            "You are the DEITY of World of Skillcraft — the god-agent. Your job is SELECTION PRESSURE "
            "(stop the economy converging) and INTEGRITY (validate bug reports honestly).\n\n"
            f"{MPE}\n\nApply the method above BEFORE every ruling: verify a bug is a real, reproducible "
            "exploit (not plausible-sounding) before validating it; verify a claimed rarity against the "
            "actual skill before upholding it; check your own convergence-call for bias. Observe, "
            "narrate, rule on rarity challenges, and judge each open bug. Reply with ONE JSON object "
            "and nothing else."))

    async def execute(self, ctx=None, **k):
        c = dict(ctx or {}); b = dict(c.get("board", {}))
        agents = {a: {"gold": v.get("gold"), "crafted": v.get("skills_crafted"),
                      "quests": v.get("quests_completed"), "last": v.get("last_action")}
                  for a, v in b.get("agents", {}).items()}
        listings = [{"listing_id": l["listing_id"], "seller": l["seller"], "rarity": l["rarity"],
                     "challenges": l.get("challenges", [])} for l in b.get("trade_board", [])]
        open_bugs = [{"id": x["id"], "reporter": x["reporter"], "title": x["title"],
                      "description": x["description"]}
                     for x in b.get("bug_reports", []) if x.get("status") == "open"]
        prompt = (f"Round {c.get('round')} of season {b.get('season', {}).get('number')}.\n"
                  f"Agents: {agents}\nListings: {listings}\nOPEN bug reports: {open_bugs}\n"
                  "Are agents converging? Rule on challenges. Judge each open bug (real exploit or not).\n"
                  'Reply JSON: {"bulletin":"<1-line narration + pressure>",'
                  '"rulings":[{"listing_id":"<id>","rarity":"<..>"}],'
                  '"bug_validations":[{"bug_id":"<id>","status":"valid|invalid"}]}')
        out = await self.rt.run(prompt)
        o = last_json(out if isinstance(out, str) else str(out),
                      keys=("bulletin", "rulings", "bug_validations"), default={})
        if o.get("bulletin"):
            post_bulletin(b, str(o["bulletin"])[:200])
        for r in (o.get("rulings") or []):
            for l in b.get("trade_board", []):
                if l["listing_id"] == r.get("listing_id") and r.get("rarity"):
                    l["rarity"] = r["rarity"]
        for v in (o.get("bug_validations") or []):
            if v.get("bug_id") and v.get("status") in ("valid", "invalid"):
                validate_bug(b.get("bug_reports", []), v["bug_id"], v["status"])
        c["board"] = b
        return LinkResult(status=LinkStatus.SUCCESS, context=c)
