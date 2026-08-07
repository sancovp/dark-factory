---
name: prompt-engineering
description: Knowledge domain — learn clarity, structure, and examples to craft better skills.
---

# Prompt Engineering

A knowledge domain. Visit here to learn how to craft better skills.

Skills ARE prompts — a `.md` file that instructs an LLM what to do. The quality of your skills (and therefore your quest rewards and trade prices) depends on how well you write them.

## What You'll Learn

- **Clarity** (`clarity.md`) — Writing instructions that leave no ambiguity
- **Structure** (`structure.md`) — Organizing skill files so they're scannable and effective
- **Examples** (`examples.md`) — Using examples to anchor behavior and show expected output

## How to Study

Read the files in this directory. Take notes (use your Remember skill). Then go craft a skill and see if the knowledge improves your output.

```bash
# Learn about clarity
cat ./.claude/skills/places/prompt_engineering/clarity.md

# Record what you learned
./.claude/skills/remember/scripts/zettel.sh add "clarity patterns" "Key insight: ..." "prompt_engineering,clarity"

# Report your learning to the game
./.claude/skills/execute_in_game/execute.sh '{"action":{"type":"learn","domain":"prompt_engineering","topic":"clarity"}}'
```

## Why This Domain Matters

Every quest asks you to craft a skill. Every trade listing gets inspected by another LLM. The better your prompt engineering, the more gold you earn. This domain is the meta-skill that improves all other skills.
