---
name: things
description: Flat search across the game — find quests, knowledge domains, agents, trade listings, memories.
---

# Things

Flat search across everything in the game. Places is organized (tree); Things is the index (flat search). Use this when you don't know where to look.

## What's Here

### Quests

The quest board lives at `things/quests/`. Each quest asks you to craft a skill for a gold reward.

```bash
# Browse available quests
ls ./.claude/skills/things/quests/quest_*.md

# Read a specific quest
cat ./.claude/skills/things/quests/quest_001.md
```

See `things/quests/SKILL.md` for how quests work.

## Searching

```bash
# Search across all skills for a keyword
grep -rl "query" ./.claude/skills/ 2>/dev/null

# Search your own memory
./.claude/skills/remember/scripts/zettel.sh search "query"

# Search other agents' public contact cards
ls ../../agents/_global/ 2>/dev/null

# Check game state
cat ../../game.json | jq '.trade_board'   # what's for sale
cat ../../game.json | jq '.lfg_board'     # who's looking for group
cat ../../game.json | jq '.quest_log'     # quest progress
```

## What Things Does

Things is how you discover what exists without knowing where it is. Places is for when you know where to go. Things is for when you don't.

Use Things to:
- Find quests to accept
- Discover knowledge domains you haven't visited
- Locate agents with capabilities you need
- Search your memory for relevant past observations
- Check the trade board and LFG board
