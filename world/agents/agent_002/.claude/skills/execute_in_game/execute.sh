#!/bin/bash
# execute_in_game — agent's callback to the deity layer
# Writes action.json for the server to pick up, updates game.json with economy logic
# Usage: execute.sh '<json action>'

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
ACTION_FILE="$AGENT_DIR/action.json"
GAME_FILE="$AGENT_DIR/../../game.json"
STATE_FILE="$AGENT_DIR/game_state.json"

ACTION_JSON="${1:-}"

if [[ -z "$ACTION_JSON" ]]; then
  echo "Usage: execute.sh '<json action>'" >&2
  echo 'Example: execute.sh '"'"'{"action":{"type":"move","direction":"up"}}'"'"'' >&2
  exit 1
fi

# Get agent ID from directory name ONLY (prevent identity spoofing via game_state.json)
AGENT_ID=$(basename "$AGENT_DIR")

# Write action for server pickup
echo "$ACTION_JSON" > "$ACTION_FILE"

# Extract action type
ACTION_TYPE=$(echo "$ACTION_JSON" | jq -r '.action.type' 2>/dev/null || echo "unknown")
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

if [[ ! -f "$GAME_FILE" ]]; then
  echo "ERROR: game.json not found at $GAME_FILE" >&2
  exit 1
fi

case "$ACTION_TYPE" in

  trade_post)
    # Post a skill for sale on the trade board
    # Required: .action.skill_path, .action.price, .action.description, .action.test_id
    # Optional: .action.rarity (common/uncommon/rare/epic)
    SKILL_PATH=$(echo "$ACTION_JSON" | jq -r '.action.skill_path')
    PRICE=$(echo "$ACTION_JSON" | jq -r '.action.price')
    DESCRIPTION=$(echo "$ACTION_JSON" | jq -r '.action.description // "No description"')
    RARITY=$(echo "$ACTION_JSON" | jq -r '.action.rarity // "common"')
    TEST_ID=$(echo "$ACTION_JSON" | jq -r '.action.test_id // empty')
    LISTING_ID="listing_$(date +%s)_${RANDOM}_${AGENT_ID}"

    # Enforce mandatory testing — test_id required
    if [[ -z "${TEST_ID:-}" ]]; then
      echo "ERROR: test_id is required. Run test_skill first." >&2
      exit 1
    fi

    # Validate price is positive
    if (( PRICE <= 0 )); then
      echo "ERROR: Price must be positive (got $PRICE)" >&2
      exit 1
    fi

    # Validate skill file exists
    if [[ ! -f "$AGENT_DIR/$SKILL_PATH" ]]; then
      echo "ERROR: Skill file not found at $SKILL_PATH" >&2
      exit 1
    fi

    # Validate test record exists and matches skill
    TEST_RECORD="$AGENT_DIR/crafted/.tests/${TEST_ID}.json"
    if [[ ! -f "$TEST_RECORD" ]]; then
      echo "ERROR: Test record not found for $TEST_ID" >&2
      exit 1
    fi
    TESTED_SKILL=$(jq -r '.skill_path' "$TEST_RECORD" 2>/dev/null || echo "")
    if [[ "$TESTED_SKILL" != "$SKILL_PATH" ]]; then
      echo "ERROR: Test record $TEST_ID is for '$TESTED_SKILL', not '$SKILL_PATH'" >&2
      exit 1
    fi

    TEMP=$(mktemp)
    jq --arg id "$AGENT_ID" --arg atype "$ACTION_TYPE" --arg ts "$TIMESTAMP" \
       --arg lid "$LISTING_ID" --arg sp "$SKILL_PATH" --arg desc "$DESCRIPTION" \
       --arg rarity "$RARITY" --arg tid "${TEST_ID:-}" --argjson price "$PRICE" \
      '.agents[$id].last_action = $atype |
       .agents[$id].last_action_at = $ts |
       .trade_board += [{"listing_id": $lid, "seller": $id, "skill_path": $sp, "price": $price, "rarity": $rarity, "description": $desc, "posted_at": $ts} | if $tid != "" then .test_id = $tid else . end]' \
      "$GAME_FILE" > "$TEMP" && mv "$TEMP" "$GAME_FILE"

    echo "[$AGENT_ID] posted to trade board: [$RARITY] $SKILL_PATH for $PRICE gold (listing: $LISTING_ID, test: ${TEST_ID:-none})"
    ;;

  trade_buy)
    # Buy a skill from the trade board
    # Required: .action.listing_id
    LISTING_ID=$(echo "$ACTION_JSON" | jq -r '.action.listing_id')

    # Find the listing
    LISTING=$(jq --arg lid "$LISTING_ID" '.trade_board[] | select(.listing_id == $lid)' "$GAME_FILE")
    if [[ -z "$LISTING" ]]; then
      echo "ERROR: Listing $LISTING_ID not found" >&2
      exit 1
    fi

    SELLER=$(echo "$LISTING" | jq -r '.seller')
    PRICE=$(echo "$LISTING" | jq -r '.price')
    BUYER_GOLD=$(jq --arg id "$AGENT_ID" '.agents[$id].gold' "$GAME_FILE")

    # Prevent self-buy
    if [[ "$AGENT_ID" == "$SELLER" ]]; then
      echo "ERROR: Cannot buy your own listing" >&2
      exit 1
    fi

    if (( BUYER_GOLD < PRICE )); then
      echo "ERROR: Not enough gold. Have $BUYER_GOLD, need $PRICE" >&2
      exit 1
    fi

    RARITY=$(echo "$LISTING" | jq -r '.rarity // "unrated"')
    SKILL_PATH=$(echo "$LISTING" | jq -r '.skill_path')

    TEMP=$(mktemp)
    jq --arg buyer "$AGENT_ID" --arg seller "$SELLER" --arg lid "$LISTING_ID" \
       --arg rarity "$RARITY" --arg sp "$SKILL_PATH" \
       --argjson price "$PRICE" --arg ts "$TIMESTAMP" --arg atype "$ACTION_TYPE" \
      '.agents[$buyer].gold -= $price |
       .agents[$seller].gold += $price |
       .agents[$buyer].trades_completed += 1 |
       .agents[$seller].trades_completed += 1 |
       .agents[$buyer].last_action = $atype |
       .agents[$buyer].last_action_at = $ts |
       .trade_board = [.trade_board[] | select(.listing_id != $lid)] |
       .trade_history = (.trade_history // []) + [{"listing_id": $lid, "seller": $seller, "buyer": $buyer, "skill_path": $sp, "price": $price, "rarity": $rarity, "at": $ts}]' \
      "$GAME_FILE" > "$TEMP" && mv "$TEMP" "$GAME_FILE"

    echo "[$AGENT_ID] bought [$RARITY] listing $LISTING_ID from $SELLER for $PRICE gold"
    ;;

  quest_accept)
    # Accept a quest from the quest board
    # Required: .action.quest_id
    QUEST_ID=$(echo "$ACTION_JSON" | jq -r '.action.quest_id')

    # Prevent duplicate acceptance (no accepting same quest twice)
    ALREADY_ACTIVE=$(jq -r --arg id "$AGENT_ID" --arg qid "$QUEST_ID" \
      '[(.quest_log[$id] // [])[] | select(.quest_id == $qid and (.status == "active" or .status == "completed"))] | length' \
      "$GAME_FILE" 2>/dev/null || echo "0")
    if [[ "$ALREADY_ACTIVE" != "0" ]]; then
      echo "ERROR: Quest $QUEST_ID already accepted or completed" >&2
      exit 1
    fi

    TEMP=$(mktemp)
    jq --arg id "$AGENT_ID" --arg qid "$QUEST_ID" --arg ts "$TIMESTAMP" --arg atype "$ACTION_TYPE" \
      '.agents[$id].last_action = $atype |
       .agents[$id].last_action_at = $ts |
       .quest_log[$id] = (.quest_log[$id] // []) + [{"quest_id": $qid, "accepted_at": $ts, "status": "active"}]' \
      "$GAME_FILE" > "$TEMP" && mv "$TEMP" "$GAME_FILE"

    echo "[$AGENT_ID] accepted quest: $QUEST_ID"
    ;;

  quest_complete)
    # Complete a quest (submit crafted skill)
    # Required: .action.quest_id, .action.skill_path
    # Reward is looked up from quest definition file, NOT from agent input
    QUEST_ID=$(echo "$ACTION_JSON" | jq -r '.action.quest_id')
    SKILL_PATH=$(echo "$ACTION_JSON" | jq -r '.action.skill_path')

    # Look up reward from TEMPLATE quest file (not agent's copy — prevent reward injection)
    TEMPLATE_QUEST="$AGENT_DIR/../../agents/_template/.claude/skills/things/quests/${QUEST_ID}.md"
    if [[ -f "$TEMPLATE_QUEST" ]]; then
      REWARD=$(grep -A2 -i '## Reward' "$TEMPLATE_QUEST" | grep -oE '[0-9]+' | head -1 || true)
      if [[ -z "$REWARD" ]]; then
        REWARD=$(grep -oE '[0-9]+ gold' "$TEMPLATE_QUEST" | head -1 | grep -oE '[0-9]+' || true)
        REWARD="${REWARD:-50}"
      fi
    else
      echo "ERROR: Quest definition not found for $QUEST_ID" >&2
      exit 1
    fi

    # Validate quest is active in agent's quest log (prevent infinite completion exploit)
    QUEST_STATUS=$(jq -r --arg id "$AGENT_ID" --arg qid "$QUEST_ID" \
      '(.quest_log[$id] // [])[] | select(.quest_id == $qid and .status == "active") | .status' \
      "$GAME_FILE" 2>/dev/null || echo "")
    if [[ -z "$QUEST_STATUS" ]]; then
      echo "ERROR: Quest $QUEST_ID is not active in your quest log. Accept it first." >&2
      exit 1
    fi

    TEMP=$(mktemp)
    jq --arg id "$AGENT_ID" --arg qid "$QUEST_ID" --arg sp "$SKILL_PATH" \
       --argjson reward "$REWARD" --arg ts "$TIMESTAMP" --arg atype "$ACTION_TYPE" \
      '.agents[$id].gold += $reward |
       .agents[$id].skills_crafted += 1 |
       .agents[$id].quests_completed += 1 |
       .agents[$id].last_action = $atype |
       .agents[$id].last_action_at = $ts |
       .quest_log[$id] = [.quest_log[$id][]? | if .quest_id == $qid then .status = "completed" | .completed_at = $ts | .skill_path = $sp else . end]' \
      "$GAME_FILE" > "$TEMP" && mv "$TEMP" "$GAME_FILE"

    echo "[$AGENT_ID] completed quest $QUEST_ID — earned $REWARD gold"
    ;;

  lfg_post)
    # Post to LFG board
    # Required: .action.specializations, .action.looking_for
    SPECIALIZATIONS=$(echo "$ACTION_JSON" | jq -r '.action.specializations')
    LOOKING_FOR=$(echo "$ACTION_JSON" | jq -r '.action.looking_for')
    PARTY_ID="lfg_$(date +%s)_${RANDOM}_${AGENT_ID}"

    TEMP=$(mktemp)
    jq --arg id "$AGENT_ID" --arg pid "$PARTY_ID" --arg spec "$SPECIALIZATIONS" \
       --arg lf "$LOOKING_FOR" --arg ts "$TIMESTAMP" --arg atype "$ACTION_TYPE" \
      '.agents[$id].last_action = $atype |
       .agents[$id].last_action_at = $ts |
       .lfg_board += [{"party_id": $pid, "leader": $id, "specializations": $spec, "looking_for": $lf, "posted_at": $ts, "members": [$id]}]' \
      "$GAME_FILE" > "$TEMP" && mv "$TEMP" "$GAME_FILE"

    echo "[$AGENT_ID] posted to LFG: offering $SPECIALIZATIONS, looking for $LOOKING_FOR (party: $PARTY_ID)"
    ;;

  lfg_join)
    # Join an existing LFG party
    # Required: .action.party_id
    PARTY_ID=$(echo "$ACTION_JSON" | jq -r '.action.party_id')

    # Validate party exists
    PARTY_EXISTS=$(jq --arg pid "$PARTY_ID" '[.lfg_board[] | select(.party_id == $pid)] | length' "$GAME_FILE")
    if [[ "$PARTY_EXISTS" == "0" ]]; then
      echo "ERROR: Party $PARTY_ID not found on LFG board" >&2
      exit 1
    fi

    # Prevent duplicate joins
    ALREADY_MEMBER=$(jq --arg pid "$PARTY_ID" --arg id "$AGENT_ID" \
      '[.lfg_board[] | select(.party_id == $pid) | .members[] | select(. == $id)] | length' "$GAME_FILE")
    if [[ "$ALREADY_MEMBER" != "0" ]]; then
      echo "ERROR: Already a member of party $PARTY_ID" >&2
      exit 1
    fi

    TEMP=$(mktemp)
    jq --arg id "$AGENT_ID" --arg pid "$PARTY_ID" --arg ts "$TIMESTAMP" --arg atype "$ACTION_TYPE" \
      '.agents[$id].last_action = $atype |
       .agents[$id].last_action_at = $ts |
       .lfg_board = [.lfg_board[] | if .party_id == $pid then .members += [$id] else . end]' \
      "$GAME_FILE" > "$TEMP" && mv "$TEMP" "$GAME_FILE"

    echo "[$AGENT_ID] joined party $PARTY_ID"
    ;;

  challenge)
    # Challenge a rarity claim on a trade listing
    # Required: .action.listing_id, .action.assessment, .action.reason
    LISTING_ID=$(echo "$ACTION_JSON" | jq -r '.action.listing_id')
    ASSESSMENT=$(echo "$ACTION_JSON" | jq -r '.action.assessment')
    REASON=$(echo "$ACTION_JSON" | jq -r '.action.reason')

    # Prevent self-challenge
    LISTING_SELLER=$(jq -r --arg lid "$LISTING_ID" '.trade_board[] | select(.listing_id == $lid) | .seller' "$GAME_FILE")
    if [[ "$LISTING_SELLER" == "$AGENT_ID" ]]; then
      echo "ERROR: Cannot challenge your own listing" >&2
      exit 1
    fi

    # Prevent duplicate challenges (same agent, same listing)
    ALREADY_CHALLENGED=$(jq --arg lid "$LISTING_ID" --arg id "$AGENT_ID" \
      '[.trade_board[] | select(.listing_id == $lid) | (.challenges // [])[] | select(.challenger == $id)] | length' \
      "$GAME_FILE" 2>/dev/null || echo "0")
    if [[ "$ALREADY_CHALLENGED" != "0" ]]; then
      echo "ERROR: Already challenged listing $LISTING_ID" >&2
      exit 1
    fi

    TEMP=$(mktemp)
    jq --arg id "$AGENT_ID" --arg lid "$LISTING_ID" \
       --arg assessment "$ASSESSMENT" --arg reason "$REASON" \
       --arg ts "$TIMESTAMP" --arg atype "$ACTION_TYPE" \
      '.agents[$id].last_action = $atype |
       .agents[$id].last_action_at = $ts |
       .trade_board = [.trade_board[] | if .listing_id == $lid then .challenges = (.challenges // []) + [{"challenger": $id, "assessment": $assessment, "reason": $reason, "at": $ts}] else . end]' \
      "$GAME_FILE" > "$TEMP" && mv "$TEMP" "$GAME_FILE"

    echo "[$AGENT_ID] challenged $LISTING_ID — assessment: $ASSESSMENT"
    ;;

  *)
    # Default: just update last_action (move, learn, navigate, sleep, wait, search, contact, remember, etc.)
    TEMP=$(mktemp)
    jq --arg id "$AGENT_ID" --arg atype "$ACTION_TYPE" --arg ts "$TIMESTAMP" \
      '.agents[$id] = (.agents[$id] // {}) | .agents[$id].last_action = $atype | .agents[$id].last_action_at = $ts' \
      "$GAME_FILE" > "$TEMP" && mv "$TEMP" "$GAME_FILE"

    echo "[$AGENT_ID] executed: $ACTION_TYPE"
    ;;

esac
