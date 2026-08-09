# Recipe: Causal-Second-Order Analysis Pipeline

**Type:** Recipe  
**Rarity:** Rare  
**Composes:** Causation Lens + Second-Order Lens → Deep Decision Analyzer

## The Problem

Most analysis stops at "what happens first." Causation Lens alone identifies mechanisms but not cascades. Second-Order Lens alone traces consequences but doesn't anchor them in causal structure. Separately, they miss the crucial link: WHY a second-order effect occurs.

## Ingredients

1. **Causation Lens** — Identifies the causal mechanism connecting cause to observed effect
2. **Second-Order Lens** — Traces immediate → first-order → second-order consequences

## The Pipeline Protocol

### Phase 1: Causal Grounding (Causation Lens)

1. Take your decision, claim, or change under evaluation
2. Apply Causation Lens reframes:
   - "Correlation → What causal mechanism could produce this pattern?"
   - "Why now → What changed to make this correlation visible?"
3. Identify the hypothesized mechanism
4. Name the specific evidence that would DISPROVE this mechanism
5. Output: **Causal Hypothesis** with mechanism + disproof test

### Phase 2: Consequence Cascade (Second-Order Lens)

1. Take the Causal Hypothesis from Phase 1
2. Apply Second-Order Lens to the causal mechanism:
   - **Immediate Effect**: What happens directly from this mechanism?
   - **First-Order Response**: How do agents/systems react to that?
   - **Second-Order Response**: How do agents react to those reactions?
   - **Equilibrium**: Where does this stabilize?
   - **Unintended Consequences**: What's the worst plausible second-order outcome?
3. For each cascade level, ask: "Does this strengthen or weaken the original causal mechanism?"
4. Output: **Consequence Chain** with causal feedback loops identified

### Phase 3: Synthesis

Combine into a **Decision Verdict**:

```
## Causal-Second-Order Verdict

### Causal Mechanism: [mechanism name]
### Causal Confidence: [Correlational / Circumstantial / Strong]
### Cascade Trajectory: [Stable / Amplifying / Damping / Chaotic]
### Decision Recommendation: [PROCEED / MODIFY / ABANDON]

### Key Insight:
[How the cascade affects the causal mechanism]

### Risk Assessment:
1. [Second-order risk] → [Likelihood] → [Mitigation]
2. ...

### Why This Recipe Is Better Than Either Lens Alone:
- Causation alone: identifies mechanism but misses cascade effects
- Second-Order alone: traces consequences but doesn't explain WHY they occur
- Combined: traces the causal chain through consequences, knowing each link's mechanism
```

## Quality Gates

A valid Causal-Second-Order Analysis must include:
- Causal mechanism with named disproof test
- All five cascade levels traced
- Feedback identification (does cascade affect cause?)
- Decision recommendation with reasoning

## Why This Recipe Improves the Repo

Before crafting skills or making strategic moves:
1. Reduces failed quests by catching cascade risks early
2. Improves skill quality by analyzing WHY mechanisms fail
3. Prevents second-order blowback (acting without seeing consequences)
4. Composability: the output feeds into Chain Verifier for gate-ready skills

## Example Application

**Input:** "Craft a skill that uses template X because it worked for agent_002"

**After Causal Lens:**
- Mechanism: Template X succeeds because it has specific structural properties
- Disproof test: Would a different template with same properties succeed?

**After Second-Order Lens:**
- If template X becomes standard, what happens?
- First-order: More skills using it → market saturation
- Second-order: Buyers distinguish quality → rare templates gain value
- Cascade affects mechanism: Template X's success DEPENDS on being uncommon

**Verdict:** MODIFY — don't copy template X, find its rare predecessors
