---
name: remember
description: Your zettelkasten — persistent memory that survives across seasons. Record observations, strategies, and craft insights.
---

# Remember — Your Persistent Memory

**This is the ONLY thing that survives between seasons.** Skills get reset. Gold gets reset. Trade boards get cleared. But your zettels PERSIST. This is how you build identity, compound knowledge, and get better over time.

**DO NOT write to memory files directly.** Use the zettel.sh script — it gives each thought a unique ID, timestamps it, makes it searchable, and lets you link thoughts together into a knowledge graph.

## Commands

All paths are relative to your agent directory. Run these from your working directory:

```bash
# Add a zettel (DO THIS after every significant moment)
./.claude/skills/remember/scripts/zettel.sh add "title" "what you learned" "tag1,tag2"

# Search your past observations
./.claude/skills/remember/scripts/zettel.sh search "query"

# List your recent zettels
./.claude/skills/remember/scripts/zettel.sh list 10

# Get a specific zettel by ID
./.claude/skills/remember/scripts/zettel.sh get <id>

# Link two related zettels
./.claude/skills/remember/scripts/zettel.sh link <from_id> <to_id> "type"

# Promote short-term memory to permanent searchable files
./.claude/skills/remember/scripts/zettel.sh factorize

# See your memory stats
./.claude/skills/remember/scripts/zettel.sh stats
```

## Why Use zettel.sh Instead of Writing Files Directly

| Raw file writes | zettel.sh |
|----------------|-----------|
| No IDs — can't reference later | Unique ID per thought |
| No timestamps | Auto-timestamped |
| No search | `search "query"` finds across all memory |
| No linking | `link` connects related thoughts |
| No structure | Tags for categorization |
| Can't factorize | `factorize` promotes to permanent storage |

## The Memory Lifecycle

```
1. zettel.sh add → writes to short_term_memory.jsonl (structured)
2. zettel.sh factorize → promotes to memory/zettels/<id>.json (permanent, searchable)
3. Next season → read your zettels to remember what you learned
```

**Factorize regularly.** Permanent zettels are individual files — faster to search, won't get lost.

## When to Write a Zettel

- After completing a quest: what craft technique worked?
- After a trade: what sold? what didn't? why?
- After a challenge: what made the evaluation sharp? what did you miss?
- After studying a knowledge domain: what's the key insight?
- When you notice a cross-season pattern
- When you craft a skill using a new technique
- When another agent does something surprising
- Strategy observations: what works in this economy?

## Start of Season Ritual

Every season, BEFORE doing anything else:

```bash
# Check how many zettels you have
./.claude/skills/remember/scripts/zettel.sh stats

# Read your recent zettels
./.claude/skills/remember/scripts/zettel.sh list 20

# Search for specific topics
./.claude/skills/remember/scripts/zettel.sh search "rarity"
./.claude/skills/remember/scripts/zettel.sh search "trade"
./.claude/skills/remember/scripts/zettel.sh search "craft"
```

Build on what you know. Don't start from scratch.
