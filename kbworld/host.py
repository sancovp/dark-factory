"""FactoryKbcHost — dark-factory as the functor's SECOND object (§18).
State lives IN THE REPO: kbworld/state/ — KBs, brains, personas, certs,
round reports all become git history (the crystallization log)."""
from __future__ import annotations

import json
import time
from pathlib import Path

STATE_ROOT = Path(__file__).resolve().parent / "state"


class FactoryKbcHost:
    """HOST_PROTOCOL: seat_factory + state_root + emit."""

    def __init__(self):
        self.state_root = STATE_ROOT
        self.state_root.mkdir(parents=True, exist_ok=True)

    def seat_factory(self):
        from cave_teams.examples import MiniMaxRuntime
        return MiniMaxRuntime(name="kbworld_seat", tools=[],
                              system_prompt="", max_tokens=6000)

    def named_seat_factory(self, name: str, system_prompt: str = ""):
        from cave_teams.examples import MiniMaxRuntime
        return MiniMaxRuntime(name=f"kbw_{name}"[:24], tools=[],
                              system_prompt=system_prompt, max_tokens=6000)

    def emit(self, event: dict) -> None:
        event = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), **event}
        with (self.state_root / "events.jsonl").open("a") as f:
            f.write(json.dumps(event) + "\n")
