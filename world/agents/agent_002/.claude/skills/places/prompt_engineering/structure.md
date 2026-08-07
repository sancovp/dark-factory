# Structure — Organizing Skill Files

A well-structured skill is scannable. The reader should know what it does, when to use it, and what to expect — all within 10 seconds of opening the file.

## The Standard Skill Layout

```markdown
# Skill Name

One-sentence summary of what this skill does.

## When To Use

Trigger conditions — when should this skill activate?

## Input

What the skill expects to receive.

## Output

What the skill produces. Include format.

## Process

Step-by-step instructions for how to produce the output from the input.

## Examples

At least one input → output example.
```

## Why This Order Matters

1. **Name + summary** — Reader knows if this is relevant (0.5 seconds)
2. **When to use** — Reader knows if this applies NOW (2 seconds)
3. **Input/Output** — Reader knows the contract (5 seconds)
4. **Process** — Reader knows HOW (only if they committed to using it)
5. **Examples** — Reader sees proof (anchors understanding)

Most readers bail after step 2 if the skill isn't relevant. Don't bury the lede.

## Sections Are Better Than Prose

Prose hides structure. Sections expose it. Compare:

**Prose:** "This skill takes code as input and produces a review. The review should cover bugs, style, and suggestions. Each item should have a severity, location, and description. Start by reading all the code, then..."

**Structured:**
```markdown
## Input
Source code (any language)

## Output
| Field | Format |
|-------|--------|
| Severity | critical / warning / info |
| Location | file:line |
| Description | One sentence |
| Fix | One sentence |
```

The structured version is unambiguous. The prose version is interpretable multiple ways.

## Nesting Depth

- One level of headers (`##`) for main sections
- Two levels (`###`) for subsections within a section
- Never go deeper than three levels — if you need more, the skill is too complex; split it

## Exercise

Take any skill you've crafted. Time yourself: open the file, and measure how many seconds until you know what it does, what it needs, and what it produces. Under 10 seconds = good structure. Over 30 seconds = restructure.
