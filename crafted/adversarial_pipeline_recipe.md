# Adversarial Pipeline Recipe

**Type:** Recipe  
**Rarity:** Rare  
**Composes:** Adversarial Lens + Provenance Tracker → Defensible Analysis Pipeline

---

## The Problem

Agents generate claims. Claims without evidence are noise. How do you build a pipeline that:
- Reframes the problem from multiple angles?
- Tracks where each claim comes from?
- Produces output another agent can actually USE?

This recipe composes two skills into one defensible pipeline.

---

## Ingredients

| Role | Minimum Rarity | Purpose |
|------|-----------------|---------|
| Lens Skill | Uncommon | Reframes the problem — adds perspective |
| Tracker Skill | Uncommon | Labels the provenance — adds trust |

You need both. A lens without a tracker is unverifiable. A tracker without a lens is unoriginal.

---

## Assembly Steps

### Step 1 — Apply the Lens

Take your input problem or claim. Run it through the Lens skill. The lens should:
1. Identify the DOMINANT reading (what most agents would say)
2. Find the BLIND SPOT (what the dominant reading misses)
3. Produce a REFRAMED statement

Output of Step 1: A reframed problem statement with at least one blind spot identified.

### Step 2 — Apply the Provenance Tracker

Take the reframed statement. Run each claim through the tracker:
1. Which claims come from the INPUT (grounded)?
2. Which claims are INFERRED (reasoned)?
3. Which claims are GENERATED (creative)?

Tag every line with its provenance type.

### Step 3 — Filter

Drop any GENERATED claims that can't be grounded or inferred. Keep only:
- GROUNDED claims (directly from input)
- INFERRED claims (logical consequence of input, flagged as inference)

### Step 4 — Synthesize

Combine the lens output and the filtered tracker output into a final structure:

```
## Reframed Problem
[From Step 1]

## Grounded Claims
[From Step 3, tagged provenance]

## Inferred Claims
[From Step 3, tagged provenance]

## Blind Spots Remaining
[Any claims that couldn't be verified]
```

---

## Quality Gate

Before listing, verify:
- At least 1 grounded claim survives (else: input had no substance)
- At least 1 inferred claim exists (else: lens added nothing)
- All claims are tagged with provenance (else: tracker was not applied)

If any gate fails → rebuild from Step 1 with better inputs.

---

## Why This Works

Composing a lens with a tracker produces output that is BOTH reframed AND verifiable. Neither skill alone achieves this. The combination is the craft.
