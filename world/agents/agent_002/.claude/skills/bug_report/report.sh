#!/bin/bash
# bug_report — file a bug report for a bounty
# Valid bugs earn 100g at the start of next season.
# The deity reviews all reports between seasons.
#
# Usage: report.sh "<title>" "<description>" "<reproduction_steps>" "<severity>"

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
BUG_FILE="$AGENT_DIR/../../bug_reports.json"
STATE_FILE="$AGENT_DIR/game_state.json"

# Get agent ID
if [[ -f "$STATE_FILE" ]]; then
  AGENT_ID=$(jq -r '.agent_id' "$STATE_FILE")
else
  AGENT_ID=$(basename "$AGENT_DIR")
fi

TITLE="${1:-}"
DESCRIPTION="${2:-}"
REPRO="${3:-}"
SEVERITY="${4:-medium}"

if [[ -z "$TITLE" || -z "$DESCRIPTION" || -z "$REPRO" ]]; then
  echo "Usage: report.sh \"<title>\" \"<description>\" \"<reproduction_steps>\" [severity]" >&2
  echo "" >&2
  echo "Severity: low, medium, high (default: medium)" >&2
  echo "" >&2
  echo "Example:" >&2
  echo "  report.sh \"Duplicate listing IDs\" \\" >&2
  echo "    \"Two skills posted in the same second get the same listing_id\" \\" >&2
  echo "    \"1. Post skill A  2. Immediately post skill B  3. Both have same ID\" \\" >&2
  echo "    high" >&2
  echo "" >&2
  echo "Valid bugs earn 100g at the start of next season." >&2
  exit 1
fi

# Validate severity
SEVERITY_LOWER=$(echo "$SEVERITY" | tr '[:upper:]' '[:lower:]')
if [[ "$SEVERITY_LOWER" != "low" && "$SEVERITY_LOWER" != "medium" && "$SEVERITY_LOWER" != "high" ]]; then
  echo "ERROR: Severity must be low, medium, or high" >&2
  exit 1
fi

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
BUG_ID="bug_$(date +%s)_${RANDOM}_${AGENT_ID}"

# Initialize bug_reports.json if it doesn't exist
if [[ ! -f "$BUG_FILE" ]]; then
  echo '[]' > "$BUG_FILE"
fi

# Append bug report
TEMP=$(mktemp)
jq --arg id "$BUG_ID" --arg reporter "$AGENT_ID" \
   --arg title "$TITLE" --arg desc "$DESCRIPTION" \
   --arg repro "$REPRO" --arg sev "$SEVERITY_LOWER" \
   --arg ts "$TIMESTAMP" \
  '. += [{
    "id": $id,
    "reporter": $reporter,
    "title": $title,
    "description": $desc,
    "reproduction": $repro,
    "severity": $sev,
    "reported_at": $ts,
    "status": "open",
    "reward_paid": false
  }]' "$BUG_FILE" > "$TEMP" && mv "$TEMP" "$BUG_FILE"

echo "=== BUG REPORT FILED ==="
echo "ID: $BUG_ID"
echo "Title: $TITLE"
echo "Severity: $SEVERITY_LOWER"
echo "Status: open (deity reviews between seasons)"
echo ""
echo "If validated, you earn 100g at the start of next season."
