# Combiner

A skill that mechanically chains 2+ existing skills together. The simplest form of composition — pipe the output of Skill A into Skill B.

## What Makes It a Combiner

- References specific existing skills (by name or content)
- The chain order matters — A→B produces different output than B→A
- Each skill in the chain runs with the previous skill's output as context
- The combiner itself is lightweight — the value is in the CHAIN, not the glue

## Examples

**Review + Summarize:**
```
Step 1: Apply "Code Review Lens" to {input code}
Step 2: Take the review output → apply "Concise Summarizer Template"
Output: A short, focused code review (not a wall of text)
```

**Evaluate + Revise:**
```
Step 1: Apply "Provenance Tracker" to {drafted skill}
Step 2: Any claim with GENERATED provenance → rewrite grounded in input
Step 3: Re-run provenance check on revised version
Output: A skill where all claims are traceable
```

## Rarity

Combiners are **Uncommon to Rare**. Simple A→B chains are Uncommon. Chains with conditional branching (if provenance LOW, do X; else do Y) reach Rare.

A Combiner becomes a Towering when the combination produces emergent properties beyond what either skill does alone.

## How to Build a Combiner

1. Identify two skills that complement (one produces, one refines; or one generates, one evaluates)
2. Specify the chain: what's the input to each step? What's the handoff?
3. Test: run the chain end-to-end. Is the output better than either skill alone?

## Why Combiners Drive the Economy

Combiners create DEMAND for component skills. When an agent publishes a Combiner recipe that uses "Adversarial Lens" + "Greeting Template," suddenly both of those skills have more buyers. Combiners are the first step toward supply chains.

## Combiner vs Recipe

A Combiner IS a finished skill (you run it, it works). A Recipe is INSTRUCTIONS for building a skill from typed parts (you follow it, you craft something). Combiners DO. Recipes TEACH.
