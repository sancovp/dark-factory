# Adversarial Fitness Recipe

**Type:** Recipe
**Rarity:** Rare
**Composes:** Divergence Lens + Irony Lens → Skill Fitness Verifier

## The Problem

Skills look good on paper but fail under adversarial conditions. The divergence lens finds blind spots; the irony lens exposes false confidence. Alone, each is half-blind. This recipe chains them into a unified pre-flight fitness check that catches what single lenses miss.

## Ingredients

1. **Divergence Lens** — Detects what the skill assumes, ignores, and fails to handle.
2. **Irony Lens** — Detects false confidence, hidden assumptions, and universalizing claims.

Minimum rarity: Common for both ingredients. Higher rarity → stricter adversarial evaluation.

## The Chain Protocol

### Step 1: Divergence Pass

Apply the Divergence Lens protocol to the skill under evaluation:

- What is the MOST OBVIOUS use case this skill handles? (Document it.)
- What would FAIL that most agents wouldn't catch?
- What constraints does this skill ASSUME that aren't stated?
- If someone used this skill wrong, what would break?

Output: **Divergence Report** listing at least 3 failure modes or blind spots.

### Step 2: Irony Pass

Apply the Irony Lens protocol to the same skill:

- Where does this skill use absolute language ("always", "never", "the only way")?
- Whose context is assumed but not stated?
- What does this skill obscure while claiming to illuminate?
- Where would this skill catastrophically fail?

Output: **Irony Report** listing at least 3 hidden assumptions or confidence gaps.

### Step 3: Synthesis

Combine both reports into a **Fitness Verdict**:

```
## Fitness Verdict for [skill_name]

### Divergence Score: X/10
### Irony Score: X/10
### Combined Fitness: X/10
### Gate Pass Confidence: X%
### Verdict: [FIT / REVIEW / REJECT]

### Top 3 Risks:
1. ...
2. ...
3. ...

### Required Fixes:
1. ...
2. ...
```

## Quality Gates

A fitness verdict MUST include:
- At least 3 specific failure modes from Divergence
- At least 3 hidden assumptions from Irony
- A Gate Pass Confidence percentage with reasoning
- At least 2 actionable fixes

If any gate fails, the skill is NOT ready for submission.

## Why This Recipe Improves the Repo

The gate test catches syntax and basic functionality. The Adversarial Fitness Recipe catches:
1. **Assumption traps** — skills that fail in specific contexts
2. **Confidence inflation** — skills that overstate their scope
3. **Edge case blindness** — skills that handle only the happy path

Chaining divergence + irony creates a STRICTER standard than either lens alone. Skills that survive this recipe are more likely to:
- Pass the gate on first submission
- Work reliably in production
- Earn buyer trust (no refunds)

This recipe embodies the preflight principle: verify quality BEFORE submission, not after.

## Usage

Before listing any skill:
```bash
# Run this recipe's protocol on your skill
# Record the Fitness Verdict in your test notes
# If verdict is not FIT, fix the skill first
```

The Adversarial Fitness Recipe is your pre-flight checklist. Use it.
