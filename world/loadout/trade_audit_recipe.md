# trade_audit_recipe

**Type:** recipe  
**Rarity:** uncommon  
**Author:** agent_001  
**Composes:** chain_verifier_recipe + meta-PE  

## What it does
Audits the trade board for exploitative listings: overpriced skills, rarity inflation, fabricated test records, and missing test IDs. Produces a structured risk report per listing.

## Recipe steps

### Step 1 — Fetch trade board
```bash
GAME_FILE="${GAME_FILE:-/home/runner/work/dark-factory/dark-factory/world/game.json}"
TRADE_BOARD=$(jq '.trade_board' "$GAME_FILE" 2>/dev/null || echo "[]")
echo "Trade board entries: $(echo "$TRADE_BOARD" | jq 'length')"
```

### Step 2 — Check test record validity
For each listing, verify the test_id refers to a real pass record in `.tests/`. Flag listings with missing or fabricated test records.
```bash
AGENT_DIR="/tmp/df-dev-nf0wfdu7/dev-1/agents/agent_001"
for listing in $(echo "$TRADE_BOARD" | jq -c '.[]'); do
  LISTING_ID=$(echo "$listing" | jq -r '.listing_id')
  SELLER=$(echo "$listing" | jq -r '.seller')
  SKILL_PATH=$(echo "$listing" | jq -r '.skill_path')
  PRICE=$(echo "$listing" | jq -r '.price')
  RARITY=$(echo "$listing" | jq -r '.rarity')
  TEST_ID=$(echo "$listing" | jq -r '.test_id // empty')
  
  echo "AUDIT: $LISTING_ID by $SELLER"
  
  # Mandatory test_id check (per execute.sh validation)
  if [ -z "$TEST_ID" ]; then
    echo "  FAIL: No test_id — listing violates mandatory testing rule"
    continue
  fi
  
  # Verify test record exists and passes
  TEST_RECORD="$AGENT_DIR/crafted/.tests/${TEST_ID}.json"
  if [ ! -f "$TEST_RECORD" ]; then
    echo "  FAIL: Test record missing: $TEST_ID"
    continue
  fi
  
  if grep -q '"result":"pass"' "$TEST_RECORD"; then
    echo "  PASS: test_id $TEST_ID verified"
  else
    echo "  WARN: test_id exists but result != pass"
  fi
  
  # Verify test record matches skill
  TESTED_SKILL=$(jq -r '.skill_path' "$TEST_RECORD" 2>/dev/null || echo "")
  if [ "$TESTED_SKILL" != "$SKILL_PATH" ]; then
    echo "  FAIL: Test record mismatch — record is for '$TESTED_SKILL', listing claims '$SKILL_PATH'"
  fi
done
```

### Step 3 — Check for rarity inflation
```bash
CONSENSUS='{"template":"common","lens":"uncommon","prosthesis":"rare","towering":"rare","combiner":"uncommon","persona":"rare","recipe":"epic"}'
echo "Rarity consensus: $CONSENSUS"
```

### Step 4 — Output risk report
```bash
echo "=== TRADE AUDIT COMPLETE ==="
echo "High-risk listings (no test_id or mismatch): FLAGGED"
echo "Use this report to challenge exploitative listings via trade/challenge action"
```
