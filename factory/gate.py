"""The fresh-model test gate — WoS `test_skill/test.sh`, verbatim semantics.

The prompt below IS test.sh's prompt (copied, not paraphrased). The record
shape IS test.sh's record ({test_id, skill_path, skill_name, test_input,
output, tested_at}); the test_id IS test.sh's mint
(`test_` + sha256(skill_content + output + timestamp)[:12]).

The one substitution is the same one cave-teams' live run already makes in the
polymorphic runtime slot: the fresh instance is a fresh `MiniMaxRuntime`
(tools=[], zero history) instead of `claude -p --model sonnet`. Everything the
fresh instance sees and everything that gets recorded is identical.

Run BY THE FACTORY, this is the independent mint: the test record comes from
the gate's own fresh run, not the crafter's word — the fix for the
self-minted/forgeable test_id the deity itself filed as a bug.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone

from cave_teams.examples import MiniMaxRuntime

# test.sh's prompt, verbatim (the fresh instance is the substitutable runtime).
TEST_SH_PROMPT = """You are a test subject. A skill (a set of instructions in a markdown file) will be applied to you. Follow the skill's instructions exactly, using the test input provided. Produce ONLY the output the skill specifies — no commentary, no meta-discussion, no explanation of what you're doing.

## Skill Instructions

{skill_content}

## Test Input

{test_input}

Apply the skill to the test input now. Output ONLY what the skill produces."""


async def fresh_test(agent_dir: str, skill_rel_path: str,
                     test_input: str) -> dict:
    """test.sh, executed: fresh instance runs the skill on the input; a test
    record is written to <agent_dir>/crafted/.tests/<test_id>.json. Returns
    {test_id, output, record_path, ok} — ok=False iff the fresh instance
    produced nothing (the skill could not be followed)."""
    skill_path = os.path.join(agent_dir, skill_rel_path)
    skill_content = open(skill_path).read()
    skill_name = os.path.basename(skill_rel_path)[:-3]

    fresh = MiniMaxRuntime(name="fresh_test", tools=[], system_prompt="")
    output = await fresh.run(TEST_SH_PROMPT.format(
        skill_content=skill_content, test_input=test_input))
    output = output if isinstance(output, str) else str(output)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    test_hash = hashlib.sha256(
        (skill_content + output + timestamp).encode()).hexdigest()[:12]
    test_id = f"test_{test_hash}"

    tests_dir = os.path.join(agent_dir, "crafted", ".tests")
    os.makedirs(tests_dir, exist_ok=True)
    record_path = os.path.join(tests_dir, f"{test_id}.json")
    with open(record_path, "w") as f:
        json.dump({"test_id": test_id, "skill_path": skill_rel_path,
                   "skill_name": skill_name, "test_input": test_input,
                   "output": output, "tested_at": timestamp}, f, indent=2)

    return {"test_id": test_id, "output": output, "record_path": record_path,
            "ok": bool(output.strip())}
