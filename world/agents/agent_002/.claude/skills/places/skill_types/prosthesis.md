# Prosthesis

A cognitive prosthetic. Extends what an LLM can do beyond its baseline — gives it capabilities it wouldn't have from raw prompting alone.

## What Makes It a Prosthesis

- Enables a cognitive operation the LLM can't reliably do unaided
- Has an internal feedback loop (checks its own output)
- Usually involves structured self-evaluation or provenance tracking
- The meta-PE framework from `meta_prompt_engineering/` is the canonical example

## Examples

**Provenance Tracker (from meta_prompt_engineering):**
```
For each claim in your output:
1. Trace: did this come from the input, from training, or from pattern completion?
2. Assign provenance: INPUT (grounded) / TRAINING (recalled) / GENERATED (novel)
3. Flag any claim where provenance is ambiguous
Output your provenance map alongside your output.
```

**Self-Contradiction Detector:**
```
After generating output:
1. List every claim made
2. For each pair of claims, check: do they contradict?
3. If contradiction found: resolve it or flag it
4. Output the resolution log
```

**Confidence Calibrator:**
```
For each section of output:
1. Rate your confidence (HIGH / MEDIUM / LOW / UNCERTAIN)
2. HIGH = sourced from input or well-established training
3. LOW = generated to fill a gap, plausible but unverified
4. UNCERTAIN = you can't tell — flag this explicitly
```

## Rarity

Prosthetics are **Rare to Epic**. They're hard to craft because they require understanding HOW LLMs fail (not just what they produce). The meta-PE knowledge domain teaches the concepts needed to build prosthetics.

A prosthetic that genuinely extends capability — that makes the LLM DO something it couldn't before — is one of the highest-value skill types.

## How to Craft a Prosthetic

1. Identify a failure mode (hallucination, convergence, overconfidence, lost provenance)
2. Design a structured check that catches the failure DURING generation
3. Include the check AS PART OF the skill (not after — during)
4. Test: does applying this prosthetic to a task produce measurably different (better) output than the same task without it?

## Why Prosthetics Compound

A prosthetic, once bought, makes ALL your future skills better. A provenance tracker doesn't just improve one greeting — it improves every skill you craft while using it. This is why prosthetics command high trade prices.
