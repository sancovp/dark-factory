# Towering

A skill that stacks multiple distinct concepts into a structure where the COMBINATION produces something none of the parts could alone. The name comes from building upward — each concept is a floor, and the view from the top is different from any single floor.

## What Makes It a Towering

- 3+ distinct concepts layered together
- Emergent capability: the stack does something no individual concept does
- Each layer depends on the one below it (not just parallel)
- Removing any layer visibly degrades the whole

## Example: Self-Evaluating Summarizer

```
FLOOR 1 (Template): Summarize {input} in 3 bullet points
FLOOR 2 (Lens): Apply the "what would a skeptic question?" lens to each bullet
FLOOR 3 (Prosthesis): For each bullet, rate provenance — is this from input or generated?
FLOOR 4 (Evaluation): Score the summary: bullets that are HIGH provenance + survive skeptic lens = keep. Others = revise.

EMERGENT: A summarizer that only keeps claims it can ground AND defend.
None of the 4 floors alone produces this. The stacking does.
```

## Rarity

Towerings are **Rare to Epic**. The rarity comes from genuine emergence — if the stack doesn't produce something MORE than its parts, it's just a long prompt, not a Towering.

**How judges spot fake Towerings:** Remove one layer. Does the output noticeably degrade? If not, that layer was filler — and the "Towering" is actually a Template with padding.

## How to Build a Towering

1. Start with a base capability (Template or Combiner)
2. Add a Lens that reframes how the base operates
3. Add a Prosthesis that catches failure modes the first two miss
4. Test the emergent property: what does the full stack do that no subset does?

## The Naming Convention

Name your floors. A Towering with named floors is readable, debuggable, and tradeable as parts. Unnamed floors make the whole thing a black box.

## Why Towerings Are Hard to Commoditize

A Template is trivially copyable. A Towering requires understanding WHY the layers are in that order. This means Towerings maintain value even after inspection — the recipe might be visible, but executing it well still takes craft.
