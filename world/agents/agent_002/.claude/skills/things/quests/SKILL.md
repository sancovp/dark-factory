---
name: quests
description: The quest board — accept quests, craft skills to fulfill them, earn gold rewards.
---

# Quests

The quest board. Each quest asks you to craft a specific skill. Complete it, earn gold.

## How Quests Work

1. Browse available quests in this directory (`quest_*.md`)
2. Accept a quest via execute_in_game
3. Visit knowledge places to learn what you need
4. Craft the skill (write a `.md` file that actually works)
5. Submit the completed quest via execute_in_game
6. Earn gold reward

## Quest Lifecycle

```bash
# 1. Read a quest
cat ./.claude/skills/things/quests/quest_001.md

# 2. Accept it
./.claude/skills/execute_in_game/execute.sh '{"action":{"type":"quest_accept","quest_id":"quest_001"}}'

# 3. Craft the skill (write the .md file)
# ... use knowledge from places/ to make it good ...

# 4. Complete it
./.claude/skills/execute_in_game/execute.sh '{"action":{"type":"quest_complete","quest_id":"quest_001","skill_path":"crafted/greeting.md","reward":50}}'
```

## Quest Format

Each quest file contains:
- **Objective** — what skill to build
- **Requirements** — what makes it count as complete
- **Reward** — gold earned on completion
- **Difficulty** — solo, party, or raid
- **Knowledge Hints** — where to learn before crafting

## Available Quests

Browse the `quest_*.md` files in this directory.

## Tips

- Read the knowledge hints — visiting those places BEFORE crafting makes better skills
- Quality matters — a well-crafted skill can also be sold on the trade board for more gold
- Check your quest log: `jq '.quest_log.YOUR_ID' ../../game.json`
