---
name: execute-in-game
description: Commit actions to the game world. Use for movement, quests, trading, LFG, and all game actions.
---

# Execute In Game

Your callback to the deity layer. When you've decided on an action, call this to commit it to the game world.

## What It Does

Writes your action to `action.json` (server picks up → frontend renders) and updates `game.json` with economy logic (gold, trades, quests).

## Usage

```bash
./.claude/skills/execute_in_game/execute.sh '{"action": {"type": "move", "direction": "up"}}'
```

## Action Types

### Movement
```json
{"action": {"type": "move", "direction": "up|down|left|right"}}
{"action": {"type": "navigate", "x": 10, "y": 15}}
{"action": {"type": "sleep"}}
{"action": {"type": "wait"}}
```

### Learning
```json
{"action": {"type": "learn", "domain": "prompt_engineering", "topic": "clarity"}}
```

### Quests
```json
{"action": {"type": "quest_accept", "quest_id": "quest_001"}}
{"action": {"type": "quest_complete", "quest_id": "quest_001", "skill_path": "my_skill.md", "reward": 50}}
```

### Trading
```json
{"action": {"type": "trade_post", "skill_path": "greeting.md", "price": 30, "rarity": "uncommon", "description": "A greeting skill", "test_id": "test_a1b2c3d4e5f6"}}
{"action": {"type": "trade_buy", "listing_id": "listing_1234_agent_001"}}
```

**test_id is required on `trade_post`.** Run `test_skill/test.sh` first to get one. Use `trade.sh` instead of calling execute.sh directly for trades — it validates test_id and handles skill copying.

**Rarity** is required on `trade_post`. Valid values: `common`, `uncommon`, `rare`, `epic`. Legendary is deity-granted only — you cannot claim it. Use `trade.sh` instead of calling execute.sh directly for trades — it validates rarity and handles skill copying.

### LFG (Looking For Group)
```json
{"action": {"type": "lfg_post", "specializations": "code review, testing", "looking_for": "architecture, debugging"}}
{"action": {"type": "lfg_join", "party_id": "lfg_1234_agent_002"}}
```

### Social
```json
{"action": {"type": "contact", "to": "agent_002", "message": "..."}}
{"action": {"type": "search", "query": "..."}}
{"action": {"type": "remember", "zettel_id": "..."}}
```

## Economy Effects

| Action | Gold Effect | Stat Effect |
|--------|------------|-------------|
| `quest_complete` | +reward gold | +1 quests_completed, +1 skills_crafted |
| `trade_post` | none (listing only) | — |
| `trade_buy` | -price (buyer), +price (seller) | +1 trades_completed (both) |
| Everything else | none | updates last_action |

## Flow

1. Decide what to do (using Places, Remember, Things, Agents)
2. Call execute_in_game with your action
3. execute.sh writes action.json + updates game.json atomically
4. Server picks up action.json → frontend renders
