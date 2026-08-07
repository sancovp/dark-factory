#!/bin/bash
# lfg.sh — Looking For Group channel interface
# Usage: lfg.sh <command> [args...]
#   list                                    — browse current LFG posts
#   post "<specializations>" "<looking_for>" — post to LFG
#   join <party_id>                         — join an existing party

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_DIR="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
GAME_FILE="$AGENT_DIR/../../game.json"
EXECUTE="$AGENT_DIR/.claude/skills/execute_in_game/execute.sh"
STATE_FILE="$AGENT_DIR/game_state.json"

# Get agent ID
if [[ -f "$STATE_FILE" ]]; then
  AGENT_ID=$(jq -r '.agent_id' "$STATE_FILE")
else
  AGENT_ID=$(basename "$AGENT_DIR")
fi

COMMAND="${1:-}"

case "$COMMAND" in

  list)
    echo "=== LFG BOARD ==="
    POSTS=$(jq -r '.lfg_board | length' "$GAME_FILE")
    if [[ "$POSTS" == "0" ]]; then
      echo "No LFG posts. Nobody is looking for a group right now."
    else
      jq -r '.lfg_board[] | "[\(.party_id)] Leader: \(.leader) | Has: \(.specializations) | Needs: \(.looking_for) | Members: \(.members | join(", ")) | Posted: \(.posted_at)"' "$GAME_FILE"
    fi
    ;;

  post)
    SPECIALIZATIONS="${2:-}"
    LOOKING_FOR="${3:-}"

    if [[ -z "$SPECIALIZATIONS" || -z "$LOOKING_FOR" ]]; then
      echo "Usage: lfg.sh post \"<specializations>\" \"<looking_for>\"" >&2
      exit 1
    fi

    "$EXECUTE" "{\"action\":{\"type\":\"lfg_post\",\"specializations\":\"$SPECIALIZATIONS\",\"looking_for\":\"$LOOKING_FOR\"}}"
    ;;

  join)
    PARTY_ID="${2:-}"
    if [[ -z "$PARTY_ID" ]]; then
      echo "Usage: lfg.sh join <party_id>" >&2
      exit 1
    fi

    # Verify party exists
    PARTY=$(jq --arg pid "$PARTY_ID" '.lfg_board[] | select(.party_id == $pid)' "$GAME_FILE")
    if [[ -z "$PARTY" ]]; then
      echo "ERROR: Party $PARTY_ID not found" >&2
      exit 1
    fi

    "$EXECUTE" "{\"action\":{\"type\":\"lfg_join\",\"party_id\":\"$PARTY_ID\"}}"
    ;;

  *)
    echo "Usage: lfg.sh <command> [args...]"
    echo "Commands:"
    echo "  list                                     — browse LFG board"
    echo "  post \"<specializations>\" \"<looking_for>\"  — post to LFG"
    echo "  join <party_id>                          — join a party"
    ;;

esac
