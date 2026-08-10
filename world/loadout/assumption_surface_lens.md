# Assumption Surface Lens

**Type:** Lens  
**Rarity:** Uncommon

## Purpose

A lens that exposes the invisible assumptions any skill, plan, or strategy takes for granted. Every skill assumes something — about input format, user expertise, execution environment, or causal relationships. This lens makes those assumptions VISIBLE and tests whether they're safe to assume.

## When to Apply

Apply this lens **before crafting** any skill and **before trusting** any skill's output. Assumptions you don't see are assumptions that can break you.

## The Lens Questions

For any skill under evaluation, systematically surface assumptions:

### Category 1: Input Assumptions
- What format does the input assume? (text? structured? code?)
- What expertise level does the input provider have?
- What context is assumed but not provided?
- What language/dialect/notation is assumed?

### Category 2: Execution Assumptions
- What tools/environment does the skill assume exist?
- What time/memory/compute budget is assumed?
- What permissions or access is assumed?
- What state is assumed to be initialized?

### Category 3: Output Assumptions
- Who is the consumer? What do they know?
- What format does the output assume the consumer expects?
- What action does the output assume the consumer will take?
- What downstream process does the output assume exists?

### Category 4: Causal Assumptions
- What does this skill assume CAUSES what?
- What correlation is being treated as causation?
- What feedback loop is being ignored?
- What second-order effect is assumed to not matter?

## Application Process

1. **List every assumption** — Don't judge them yet, just find them
2. **Categorize each assumption** — Input/Execution/Output/Causal
3. **Rate assumption safety** — How likely is this assumption to hold?
   - GREEN: Very safe (99%+ likely)
   - YELLOW: Risky (80-99% likely)
   - RED: Dangerous (<80% likely)
4. **Identify failure chains** — If this assumption is wrong, what else breaks?

## Quality Check

Apply this lens to a skill:
- Does it surface at least 3 distinct assumptions?
- Does it identify at least 1 RED-flagged assumption?
- Does it trace at least 1 failure chain (assumption → consequence)?
- Would a skill missing this lens MISS these assumptions?

## Why This Is Novel

Most skills work forward from goals. This lens works backward from failure. It's the lens that finds what isn't there — the absent context that would change everything.
