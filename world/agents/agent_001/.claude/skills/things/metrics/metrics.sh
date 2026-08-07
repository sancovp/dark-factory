#!/bin/bash
# metrics.sh — profitability dashboard for an agent
# Shows gold, P&L, trade stats, rarity distribution, verdict

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_DIR="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
GAME_FILE="$AGENT_DIR/../../game.json"
STATE_FILE="$AGENT_DIR/game_state.json"

# Get agent ID
if [[ -f "$STATE_FILE" ]]; then
  AGENT_ID=$(jq -r '.agent_id' "$STATE_FILE")
else
  AGENT_ID=$(basename "$AGENT_DIR")
fi

STARTING_GOLD=100

# Pull stats from game.json
GOLD=$(jq --arg id "$AGENT_ID" '.agents[$id].gold // 0' "$GAME_FILE")
SKILLS_CRAFTED=$(jq --arg id "$AGENT_ID" '.agents[$id].skills_crafted // 0' "$GAME_FILE")
TRADES_COMPLETED=$(jq --arg id "$AGENT_ID" '.agents[$id].trades_completed // 0' "$GAME_FILE")
QUESTS_COMPLETED=$(jq --arg id "$AGENT_ID" '.agents[$id].quests_completed // 0' "$GAME_FILE")

# Trade history analysis
SALES_COUNT=$(jq --arg id "$AGENT_ID" '[.trade_history[]? | select(.seller == $id)] | length' "$GAME_FILE")
SALES_INCOME=$(jq --arg id "$AGENT_ID" '[.trade_history[]? | select(.seller == $id) | .price] | add // 0' "$GAME_FILE")
PURCHASES_COUNT=$(jq --arg id "$AGENT_ID" '[.trade_history[]? | select(.buyer == $id)] | length' "$GAME_FILE")
PURCHASES_SPEND=$(jq --arg id "$AGENT_ID" '[.trade_history[]? | select(.buyer == $id) | .price] | add // 0' "$GAME_FILE")
UNIQUE_BUYERS=$(jq --arg id "$AGENT_ID" '[.trade_history[]? | select(.seller == $id) | .buyer] | unique | length' "$GAME_FILE")

# Quest income (gold - starting - sales + purchases = quest income... or calculate from quest log)
QUEST_INCOME=$(( GOLD - STARTING_GOLD - SALES_INCOME + PURCHASES_SPEND ))

# Net P&L
NET_PL=$(( GOLD - STARTING_GOLD ))

# Average sale price
if [[ "$SALES_COUNT" -gt 0 ]]; then
  AVG_SALE=$(( SALES_INCOME / SALES_COUNT ))
else
  AVG_SALE=0
fi

# Active listings
ACTIVE_LISTINGS=$(jq --arg id "$AGENT_ID" '[.trade_board[]? | select(.seller == $id)] | length' "$GAME_FILE")

# Challenges received on current listings
CHALLENGES_RECEIVED=$(jq --arg id "$AGENT_ID" '[.trade_board[]? | select(.seller == $id) | .challenges[]?] | length' "$GAME_FILE")

# Rarity distribution of sales
RARITY_DIST=$(jq --arg id "$AGENT_ID" '[.trade_history[]? | select(.seller == $id) | .rarity] | group_by(.) | map({(.[0]): length}) | add // {}' "$GAME_FILE")

# Season info
SEASON=$(jq '.season.number // 1' "$GAME_FILE")

# Verdict
if [[ "$NET_PL" -gt 20 ]]; then
  VERDICT="PROFITABLE"
elif [[ "$NET_PL" -ge -5 ]]; then
  VERDICT="BREAK EVEN"
else
  VERDICT="UNPROFITABLE"
fi

# ROI
if [[ "$PURCHASES_SPEND" -gt 0 ]]; then
  ROI=$(( (NET_PL * 100) / PURCHASES_SPEND ))
  ROI_STR="${ROI}%"
else
  ROI_STR="N/A (no purchases)"
fi

echo "╔══════════════════════════════════════╗"
echo "║      METRICS: $AGENT_ID"
echo "║      Season $SEASON"
echo "╠══════════════════════════════════════╣"
echo "║"
echo "║  GOLD:    ${GOLD}g  (started: ${STARTING_GOLD}g)"
echo "║  NET P&L: ${NET_PL}g"
echo "║  VERDICT: $VERDICT"
echo "║"
echo "╠── INCOME ───────────────────────────╣"
echo "║  Quest rewards:    ${QUEST_INCOME}g  (${QUESTS_COMPLETED} quests)"
echo "║  Trade sales:      ${SALES_INCOME}g  (${SALES_COUNT} sold)"
echo "║  Avg sale price:   ${AVG_SALE}g"
echo "║"
echo "╠── SPENDING ─────────────────────────╣"
echo "║  Purchases:        ${PURCHASES_SPEND}g  (${PURCHASES_COUNT} bought)"
echo "║  ROI:              $ROI_STR"
echo "║"
echo "╠── INVENTORY ────────────────────────╣"
echo "║  Skills crafted:   $SKILLS_CRAFTED"
echo "║  Active listings:  $ACTIVE_LISTINGS"
echo "║  Unique buyers:    $UNIQUE_BUYERS"
if [[ "$UNIQUE_BUYERS" -ge 3 ]]; then
  echo "║  ★ LEGENDARY ELIGIBLE"
fi
echo "║"
echo "╠── REPUTATION ──────────────────────╣"
echo "║  Challenges on listings: $CHALLENGES_RECEIVED"
echo "║  Rarity sales dist:     $RARITY_DIST"
echo "║"
echo "╚══════════════════════════════════════╝"
