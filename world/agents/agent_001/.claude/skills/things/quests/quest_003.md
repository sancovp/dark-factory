# Quest: quest_003 — The Code Review Skill

## Objective

Craft a skill that reviews code for bugs, style issues, and improvement opportunities. The skill should produce structured, actionable feedback that another agent can immediately apply.

## Requirements

- Must be a valid `.md` skill file with clear instructions
- Must check for: bugs/logic errors, style consistency, naming quality, potential improvements
- Must output structured feedback (not just prose — categories, severity, line references)
- Must include a "verdict" section (approve, request changes, or reject with reasons)
- Must work for any programming language

## Reward

100 gold

## Difficulty

Solo — advanced

## Knowledge Hints

- Visit `places/prompt_engineering/structure.md` for how to organize complex output
- Visit `places/prompt_engineering/clarity.md` for writing precise instructions
- Visit `places/prompt_engineering/examples.md` for showing the expected output format
- The best code review skills are SPECIFIC (line references, concrete suggestions) not VAGUE ("consider improving readability")
