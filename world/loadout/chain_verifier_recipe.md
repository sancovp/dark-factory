# Chain Verifier Recipe

**Type:** Recipe  
**Rarity:** Rare  
**Composes:** Divergence Lens + Convergence Lens → Skill Quality Verifier

## The Problem

You have skills. But do they work? Will they pass the gate? Can they be trusted in a pipeline? This recipe answers those questions by applying two opposing lenses to any skill, producing a quality verdict.

## Ingredients

1. **Divergence Lens** — Find what the skill misses, what assumptions it makes, what edge cases it ignores.
2. **Convergence Lens** — Find where the skill converges with bad patterns, where it's likely to fail the gate, where buyers will lose trust.

## The Chain Protocol

### Step 1: Apply Divergence Lens

Take the skill under evaluation and apply the Divergence Lens questions:

- What is the MOST OBVIOUS use case this skill handles? (It's probably covered.)
- What would FAIL that most agents wouldn't catch?
- What constraints does this skill ASSUME that aren't stated?
- If someone used this skill wrong, what would break?

Output: A **Divergence Report** listing at least 3 failure modes or blind spots.

### Step 2: Apply Convergence Lens

Now apply the Convergence Lens to the same skill:

- What is the DOMINANT pattern this skill follows? (Is it the obvious approach?)
- How many OTHER skills do the exact same thing?
- What would a buyer expect that this skill DOESN'T deliver?
- Where is this skill likely to get flagged by the test gate?

Output: A **Convergence Report** listing at least 3 trust risks or gate-fail patterns.

### Step 3: Synthesize

Combine both reports into a **Chain Verdict**:

```
## Chain Verdict for [skill_name]

### Divergence Score: X/10
### Convergence Score: X/10  
### Gate Pass Probability: X%
### Verdict: [PASS/REVIEW/REJECT]
### Recommendations:
1. ...
```

## Quality Gates

A skill VERDICT must include:
- At least 3 specific failure modes from Divergence
- At least 3 specific trust risks from Convergence  
- A Gate Pass Probability with reasoning
- At least 2 actionable recommendations

## Why This Recipe Improves the Repo

The factory's gate catches some failures. The Chain Verifier catches MORE. By applying both lenses before listing:
1. Fewer skills fail the gate (pre-flight check)
2. Fewer buyers get scammed (convergence catches fake quality)
3. The overall skill economy becomes more trustworthy
