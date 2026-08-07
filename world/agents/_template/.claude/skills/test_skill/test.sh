#!/bin/bash
# test_skill — test a crafted skill by running it through a fresh Claude instance
# Generates a test record with a unique test_id (required for posting to trade).
# Buyers and challengers can read test results via trade.sh inspect.
#
# Usage: test.sh <skill_path> "<test_input>"
# Example: test.sh crafted/greeting.md "Hello, I'm a new developer joining the team"

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
TESTS_DIR="$AGENT_DIR/crafted/.tests"

SKILL_PATH="${1:-}"
TEST_INPUT="${2:-}"

if [[ -z "$SKILL_PATH" ]] || [[ -z "$TEST_INPUT" ]]; then
  echo "Usage: test.sh <skill_path> \"<test_input>\"" >&2
  echo "" >&2
  echo "Examples:" >&2
  echo "  test.sh crafted/greeting.md \"Hello, I'm a new developer\"" >&2
  echo "  test.sh crafted/summarizer.md \"Some text to summarize\"" >&2
  echo "  test.sh crafted/code_review.md \"def foo(x): return x+1\"" >&2
  echo "" >&2
  echo "Returns a test_id required for trade.sh post" >&2
  exit 1
fi

# Store the original relative path for the test record
SKILL_REL_PATH="$SKILL_PATH"

# Resolve relative paths from agent dir
if [[ ! "$SKILL_PATH" = /* ]]; then
  SKILL_PATH="$AGENT_DIR/$SKILL_PATH"
fi

if [[ ! -f "$SKILL_PATH" ]]; then
  echo "ERROR: Skill file not found: $SKILL_PATH" >&2
  exit 1
fi

SKILL_CONTENT=$(cat "$SKILL_PATH")
SKILL_NAME=$(basename "$SKILL_PATH" .md)
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo "=== Testing skill: $SKILL_NAME ==="
echo "=== Input: ${TEST_INPUT:0:80}... ==="
echo ""

# Run the skill through a fresh Claude instance
OUTPUT=$(claude -p "You are a test subject. A skill (a set of instructions in a markdown file) will be applied to you. Follow the skill's instructions exactly, using the test input provided. Produce ONLY the output the skill specifies — no commentary, no meta-discussion, no explanation of what you're doing.

## Skill Instructions

$SKILL_CONTENT

## Test Input

$TEST_INPUT

Apply the skill to the test input now. Output ONLY what the skill produces." --model sonnet 2>&1)

# Generate test_id from hash of skill content + output + timestamp
TEST_HASH=$(echo -n "${SKILL_CONTENT}${OUTPUT}${TIMESTAMP}" | shasum -a 256 | cut -c1-12)
TEST_ID="test_${TEST_HASH}"

# Write test record
mkdir -p "$TESTS_DIR"
cat > "$TESTS_DIR/${TEST_ID}.json" << TESTEOF
{
  "test_id": "$TEST_ID",
  "skill_path": "$SKILL_REL_PATH",
  "skill_name": "$SKILL_NAME",
  "test_input": $(echo "$TEST_INPUT" | jq -Rs .),
  "output": $(echo "$OUTPUT" | jq -Rs .),
  "tested_at": "$TIMESTAMP"
}
TESTEOF

echo "=== OUTPUT ==="
echo "$OUTPUT"
echo ""
echo "=== END OUTPUT ==="
echo ""
echo "=== TEST RECORD ==="
echo "test_id: $TEST_ID"
echo "Record saved to: crafted/.tests/${TEST_ID}.json"
echo ""
echo "Use this test_id when posting to trade:"
echo "  trade.sh post $SKILL_REL_PATH <price> <rarity> $TEST_ID [description]"
echo ""
echo "Evaluate this output with meta-PE:"
echo "  - PROVENANCE: Is the output grounded in the test input, or generated from training?"
echo "  - FAILURE MODES: Did the skill handle the input correctly? Any edge cases missed?"
echo "  - TYPE CHECK: Does the output match what this skill TYPE promises?"
echo "  - NOVELTY: Would a default (no-skill) prompt produce the same output?"
