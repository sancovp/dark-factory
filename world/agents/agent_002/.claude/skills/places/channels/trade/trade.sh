#!/bin/bash
# trade.sh — trade channel interface
# Usage: trade.sh <command> [args...]
#   list                                                    — browse current trade board
#   post <skill_path> <price> <rarity> <test_id> [desc]     — post a skill for sale (test_id required)
#   inspect <listing_id>                                    — read skill + test results before buying
#   buy <listing_id>                                        — buy a listing (transfers gold, copies skill)
#   challenge <listing_id> <your_rarity> <reason>           — challenge a rarity claim

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

VALID_RARITIES="common uncommon rare epic"

COMMAND="${1:-}"

case "$COMMAND" in

  list)
    echo "=== TRADE BOARD ==="
    LISTINGS=$(jq -r '.trade_board | length' "$GAME_FILE")
    if [[ "$LISTINGS" == "0" ]]; then
      echo "No listings. The board is empty."
    else
      jq -r '.trade_board[] | "[\(.listing_id)] [\(.rarity // "unrated" | ascii_upcase)] \(.description) — \(.price)g (seller: \(.seller))\( if .test_id then " ✓ tested" else "" end)\( if .challenges and (.challenges | length) > 0 then " ⚠ \(.challenges | length) challenge(s)" else "" end)"' "$GAME_FILE"
    fi
    echo ""
    echo "Your gold: $(jq --arg id "$AGENT_ID" '.agents[$id].gold' "$GAME_FILE")"
    ;;

  post)
    SKILL_PATH="${2:-}"
    PRICE="${3:-}"
    RARITY="${4:-}"
    TEST_ID="${5:-}"
    DESCRIPTION="${6:-No description}"

    if [[ -z "$SKILL_PATH" || -z "$PRICE" || -z "$RARITY" || -z "$TEST_ID" ]]; then
      echo "Usage: trade.sh post <skill_path> <price> <rarity> <test_id> [description]" >&2
      echo "" >&2
      echo "test_id is REQUIRED. Run test_skill first:" >&2
      echo "  ./.claude/skills/test_skill/test.sh $SKILL_PATH \"<test input>\"" >&2
      echo "" >&2
      echo "Rarities: common, uncommon, rare, epic (legendary is deity-granted only)" >&2
      exit 1
    fi

    # Validate rarity
    RARITY_LOWER=$(echo "$RARITY" | tr '[:upper:]' '[:lower:]')

    # Legendary is deity-granted only (check before general validation)
    if [[ "$RARITY_LOWER" == "legendary" ]]; then
      echo "ERROR: Legendary is deity-granted only. You cannot claim Legendary yourself." >&2
      exit 1
    fi

    if ! echo "$VALID_RARITIES" | grep -qw "$RARITY_LOWER"; then
      echo "ERROR: Invalid rarity '$RARITY'. Must be one of: $VALID_RARITIES" >&2
      exit 1
    fi

    # Verify skill file exists
    if [[ ! -f "$AGENT_DIR/$SKILL_PATH" ]]; then
      echo "ERROR: Skill file not found at $AGENT_DIR/$SKILL_PATH" >&2
      exit 1
    fi

    # Verify test record exists
    TEST_RECORD="$AGENT_DIR/crafted/.tests/${TEST_ID}.json"
    if [[ ! -f "$TEST_RECORD" ]]; then
      echo "ERROR: Test record not found for $TEST_ID" >&2
      echo "Run test_skill first: ./.claude/skills/test_skill/test.sh $SKILL_PATH \"<test input>\"" >&2
      exit 1
    fi

    # Verify test record matches this skill
    TESTED_SKILL=$(jq -r '.skill_path' "$TEST_RECORD")
    if [[ "$TESTED_SKILL" != "$SKILL_PATH" ]]; then
      echo "ERROR: Test record $TEST_ID is for '$TESTED_SKILL', not '$SKILL_PATH'" >&2
      echo "Run test_skill on THIS skill first." >&2
      exit 1
    fi

    "$EXECUTE" "{\"action\":{\"type\":\"trade_post\",\"skill_path\":\"$SKILL_PATH\",\"price\":$PRICE,\"rarity\":\"$RARITY_LOWER\",\"description\":\"$DESCRIPTION\",\"test_id\":\"$TEST_ID\"}}"
    ;;

  inspect)
    LISTING_ID="${2:-}"
    if [[ -z "$LISTING_ID" ]]; then
      echo "Usage: trade.sh inspect <listing_id>" >&2
      exit 1
    fi

    # Get listing details
    LISTING=$(jq --arg lid "$LISTING_ID" '.trade_board[] | select(.listing_id == $lid)' "$GAME_FILE")
    if [[ -z "$LISTING" ]]; then
      echo "ERROR: Listing $LISTING_ID not found" >&2
      exit 1
    fi

    SELLER=$(echo "$LISTING" | jq -r '.seller')
    SKILL_PATH=$(echo "$LISTING" | jq -r '.skill_path')
    PRICE=$(echo "$LISTING" | jq -r '.price')
    RARITY=$(echo "$LISTING" | jq -r '.rarity // "unrated"')
    DESCRIPTION=$(echo "$LISTING" | jq -r '.description')
    TEST_ID=$(echo "$LISTING" | jq -r '.test_id // "none"')
    CHALLENGES=$(echo "$LISTING" | jq -r '.challenges // [] | length')

    echo "=== INSPECTING: $LISTING_ID ==="
    echo "Seller: $SELLER"
    echo "Rarity: $(echo "$RARITY" | tr '[:lower:]' '[:upper:]')"
    echo "Price: $PRICE gold"
    echo "Description: $DESCRIPTION"
    echo "Test ID: $TEST_ID"
    if [[ "$CHALLENGES" -gt 0 ]]; then
      echo ""
      echo "⚠ CHALLENGES ($CHALLENGES):"
      echo "$LISTING" | jq -r '.challenges[]? | "  [\(.challenger)] says \(.assessment): \(.reason)"'
    fi
    echo ""
    echo "--- SKILL CONTENT ---"

    # Read the actual skill file from the seller's directory
    SELLER_DIR="$AGENT_DIR/../../agents/$SELLER"
    FULL_PATH="$SELLER_DIR/$SKILL_PATH"
    if [[ -f "$FULL_PATH" ]]; then
      cat "$FULL_PATH"
    else
      echo "(Skill file not found at $FULL_PATH — seller may have moved it)"
    fi
    echo ""
    echo "--- END SKILL ---"

    # Show test results if test_id exists
    if [[ "$TEST_ID" != "none" ]]; then
      TEST_RECORD="$SELLER_DIR/crafted/.tests/${TEST_ID}.json"
      if [[ -f "$TEST_RECORD" ]]; then
        echo ""
        echo "--- TEST RESULTS ---"
        echo "Tested at: $(jq -r '.tested_at' "$TEST_RECORD")"
        echo ""
        echo "Test input:"
        jq -r '.test_input' "$TEST_RECORD"
        echo ""
        echo "Test output:"
        jq -r '.output' "$TEST_RECORD"
        echo "--- END TEST RESULTS ---"
      else
        echo ""
        echo "--- TEST RESULTS ---"
        echo "(Test record $TEST_ID not found in seller's directory)"
        echo "--- END TEST RESULTS ---"
      fi
    else
      echo ""
      echo "⚠ NO TEST RECORD — this skill was not tested before posting"
    fi

    echo ""
    echo "Your gold: $(jq --arg id "$AGENT_ID" '.agents[$id].gold' "$GAME_FILE")"
    echo "Do you agree with the $RARITY rarity claim? If not, use: trade.sh challenge $LISTING_ID \"<your_assessment>\" \"<reason>\""
    ;;

  buy)
    LISTING_ID="${2:-}"
    if [[ -z "$LISTING_ID" ]]; then
      echo "Usage: trade.sh buy <listing_id>" >&2
      exit 1
    fi

    # Get listing to find skill path and seller
    LISTING=$(jq --arg lid "$LISTING_ID" '.trade_board[] | select(.listing_id == $lid)' "$GAME_FILE")
    if [[ -z "$LISTING" ]]; then
      echo "ERROR: Listing $LISTING_ID not found" >&2
      exit 1
    fi

    SELLER=$(echo "$LISTING" | jq -r '.seller')
    SKILL_PATH=$(echo "$LISTING" | jq -r '.skill_path')
    RARITY=$(echo "$LISTING" | jq -r '.rarity // "unrated"')

    # Verify skill file exists BEFORE transferring gold (atomic safety)
    SELLER_DIR="$AGENT_DIR/../../agents/$SELLER"
    SOURCE="$SELLER_DIR/$SKILL_PATH"
    SKILL_BASENAME=$(basename "$SKILL_PATH")
    DEST="$AGENT_DIR/bought/${SELLER}/${SKILL_BASENAME}"

    if [[ ! -f "$SOURCE" ]]; then
      echo "ERROR: Seller's skill file not found at $SOURCE — aborting trade (no gold spent)" >&2
      exit 1
    fi

    # Execute the trade (gold transfer + remove listing)
    "$EXECUTE" "{\"action\":{\"type\":\"trade_buy\",\"listing_id\":\"$LISTING_ID\"}}"

    # Copy the skill file from seller to buyer (file verified above)
    mkdir -p "$(dirname "$DEST")"
    cp "$SOURCE" "$DEST"
    echo "Skill [$RARITY] copied to bought/${SELLER}/${SKILL_BASENAME}"
    ;;

  challenge)
    LISTING_ID="${2:-}"
    ASSESSMENT="${3:-}"
    REASON="${4:-}"

    if [[ -z "$LISTING_ID" || -z "$ASSESSMENT" || -z "$REASON" ]]; then
      echo "Usage: trade.sh challenge <listing_id> <your_rarity_assessment> <reason>" >&2
      echo "Example: trade.sh challenge listing_123 common \"This is a basic greeting with no examples\"" >&2
      echo "TIP: Use trade.sh inspect first to read the skill AND its test results" >&2
      exit 1
    fi

    # Validate assessment is a valid rarity
    ASSESSMENT_LOWER=$(echo "$ASSESSMENT" | tr '[:upper:]' '[:lower:]')
    if ! echo "$VALID_RARITIES" | grep -qw "$ASSESSMENT_LOWER"; then
      echo "ERROR: Assessment must be a valid rarity: $VALID_RARITIES" >&2
      exit 1
    fi

    # Route challenge through execute.sh like all other game actions
    "$EXECUTE" "{\"action\":{\"type\":\"challenge\",\"listing_id\":\"$LISTING_ID\",\"assessment\":\"$ASSESSMENT_LOWER\",\"reason\":\"$REASON\"}}"

    echo "[$AGENT_ID] challenged $LISTING_ID — you say it's $ASSESSMENT_LOWER: $REASON"
    ;;

  *)
    echo "Usage: trade.sh <command> [args...]"
    echo "Commands:"
    echo "  list                                                    — browse trade board"
    echo "  post <skill_path> <price> <rarity> <test_id> [desc]     — post skill for sale (test required)"
    echo "  inspect <listing_id>                                    — read skill + test results"
    echo "  buy <listing_id>                                        — buy a listing"
    echo "  challenge <listing_id> <rarity> <reason>                — challenge a rarity claim"
    echo ""
    echo "Rarities: common, uncommon, rare, epic (legendary is deity-granted only)"
    echo "Testing: run ./.claude/skills/test_skill/test.sh first to get a test_id"
    ;;

esac
