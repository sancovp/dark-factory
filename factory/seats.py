"""The two LLM seats, as thin HTTP clients — no agent framework in CI.

MiniMax exposes an Anthropic-compatible endpoint; both seats speak to it with
plain `requests`. The FRESH JUDGE is a brand-new, toolless, zero-history call
per case — it sees ONLY the skill document and one input (the fresh-model
test-gate). The DEV SEAT keeps its own message list as the conversation.

Anti-Goodhart boundary (stated, not implied): the dev seat is toolless and is
prompt-fed the failing INPUTS only — expected outputs never enter any prompt.
The batteries are public in this repo, but nothing in the loop hands them to
the seat; a seat that could browse the repo would be a different (weaker)
claim, which is why the seats are HTTP calls and not agents.
"""
from __future__ import annotations

import os
import re
from typing import Dict, List, Optional

import requests

BASE_URL = os.environ.get("MINIMAX_BASE_URL",
                          "https://api.minimax.io/anthropic/v1/messages")
MODEL = os.environ.get("FACTORY_MODEL", "MiniMax-M2.7-highspeed")


def have_key() -> bool:
    return bool(os.environ.get("MINIMAX_API_KEY"))


def chat(system: str, messages: List[Dict[str, str]],
         max_tokens: int = 2000, temperature: float = 0.2) -> str:
    """One Anthropic-shaped call. Raises on transport/HTTP errors."""
    key = os.environ["MINIMAX_API_KEY"]
    r = requests.post(
        BASE_URL,
        headers={"x-api-key": key, "Authorization": f"Bearer {key}",
                 "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json={"model": MODEL, "max_tokens": max_tokens,
              "temperature": temperature, "system": system,
              "messages": messages},
        timeout=180)
    r.raise_for_status()
    data = r.json()
    parts = data.get("content") or []
    return "".join(p.get("text", "") for p in parts
                   if p.get("type") in (None, "text")).strip()


# ── the fresh judge (gate #1): new call, zero history, document + input only ──
JUDGE_SYSTEM = ("You are a skill executor. Follow the skill document EXACTLY "
                "as written, even where it seems suboptimal or wrong — "
                "fidelity to the document is your only job. Output ONLY the "
                "final result, no commentary, no quotes.")


def fresh_judge(artifact: str, task_input: str, workdir: str) -> Dict:
    """skillcar executor signature (sync ok — awaited via to_thread upstream)."""
    try:
        out = chat(JUDGE_SYSTEM,
                   [{"role": "user",
                     "content": f"SKILL DOCUMENT:\n{artifact}\n\nINPUT:\n"
                                f"{task_input}\n\nExecute the skill on the "
                                f"input now."}],
                   temperature=0.0)
    except Exception as e:
        return {"ok": False, "error": f"judge transport: {e}"}
    out = out.strip().strip('"\'')
    if out.lower() in ("empty string", "(empty string)", "none", '""', "''"):
        out = ""
    return {"ok": True, "output": out}


# ── the dev seat: one conversation; artifact + failing inputs in, delta out ──
DEV_SYSTEM = ("You are the development seat of a dark factory. The artifact "
              "is a skill document; for 'code' cars its fenced ```python "
              "block defines solve(text) and is executed by a sandboxed "
              "interpreter; for 'prose' cars the document is followed "
              "literally by a fresh model. Your job: edit the document so it "
              "scores more correct outputs on the hidden task battery. You "
              "see which INPUTS failed — never the expected outputs. Your "
              "proposal is quarantined first (a candidate that cannot execute "
              "dies and you will be re-asked with the cause), then raced "
              "against the incumbent in a controlled split; only a strict "
              "causal win ships. Reason briefly, then output the COMPLETE "
              "edited document between <ARTIFACT> and </ARTIFACT> tags.")


class DevSeat:
    def __init__(self):
        self.messages: List[Dict[str, str]] = []

    def propose(self, car: Dict, telemetry: Dict,
                gate_feedback: Optional[str] = None) -> Dict:
        prompt = (f"CURRENT ARTIFACT (kind={car.get('kind')}, generation "
                  f"{car.get('generation')}):\n{car.get('artifact')}\n\n"
                  f"TELEMETRY: fitness={telemetry.get('fitness')}/"
                  f"{telemetry.get('cases')} correct.\nFAILING INPUTS:\n"
                  + "\n".join(f"- {i}"
                              for i in telemetry.get("failing_inputs", []))
                  + (f"\nYOUR LAST PROPOSAL DIED AT THE GATE: {gate_feedback}\n"
                     if gate_feedback else "")
                  + "\nPropose the edited document now.")
        self.messages.append({"role": "user", "content": prompt})
        out = chat(DEV_SYSTEM, self.messages, max_tokens=3000)
        self.messages.append({"role": "assistant", "content": out})
        m = re.search(r"<ARTIFACT>(.*?)</ARTIFACT>", out, re.S)
        return {"artifact": m.group(1).strip() + "\n"} if m else {}
