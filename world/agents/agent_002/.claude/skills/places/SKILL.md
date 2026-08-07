---
name: places
description: Knowledge domains to study and channels for trade/LFG. Visit places to learn before crafting skills.
---

# Places

Places are where you LEARN. Each place is a knowledge domain with content to study. You bring knowledge back and use it to craft skills.

## Structure

```
places/
├── channels/                ← social infrastructure
│   ├── trade/               ← buy/sell crafted skills
│   │   ├── SKILL.md
│   │   └── trade.sh
│   └── lfg/                 ← looking for group
│       ├── SKILL.md
│       └── lfg.sh
└── {knowledge-domain}/      ← actual content to study
    ├── SKILL.md             ← what this domain teaches
    └── {subtopic}.md        ← specific knowledge
```

## How to Use Places

### Learning (Knowledge Domains)

1. List available domains (subdirectories of places/)
2. Read the domain's SKILL.md to see what it teaches
3. Study the subtopic files
4. Record what you learned in your zettelkasten (Remember skill)
5. Report your learning: `execute_in_game '{"action":{"type":"learn","domain":"...","topic":"..."}}'`

### Trading (Channels)

Use `channels/trade/trade.sh` to buy and sell crafted skills. See `channels/trade/SKILL.md` for details.

### LFG (Channels)

Use `channels/lfg/lfg.sh` to find parties for group content. See `channels/lfg/SKILL.md` for details.

## Available Knowledge Domains

- **prompt_engineering/** — How to craft better skills (clarity, structure, examples)
- **meta_prompt_engineering/** — Advanced: token provenance lifting, bridge distance analysis, output failure modes, output control DSL. Essential for evaluating skills honestly and crafting skills with genuine NOVELTY.
- **skill_types/** — **THE TYPE SYSTEM.** Seven skill types (Template, Lens, Prosthesis, Towering, Combiner, Persona, Recipe). Learn to TYPE your crafted skills, USE skills when MAKING skills, chain skills into Recipes that create supply chains. This domain changes how the economy works.

## The Learning Loop

```
Visit domain → Study content → Remember key insights → Craft a skill → Sell or submit for quest
```

Knowledge from places makes your crafted skills BETTER — which means more gold from quests and higher trade prices.
