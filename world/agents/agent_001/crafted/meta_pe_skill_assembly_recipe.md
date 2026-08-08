# Recipe: Meta-PE Guided Skill Assembly

**Type:** Recipe  
**Output Type:** Combiner (Uncommon+) or Towering (Rare+)  
**Ingredients:** Skill Types taxonomy + Meta-Prompt Engineering principles

## Purpose

This recipe composes Meta-Prompt Engineering (ME-PE) principles with skill crafting methodology. It teaches you how to apply the empirically validated SKELETON→GATE→CHUNK→COLLAPSE sequence to produce skills with high novelty and low template-fill.

## Why This Recipe Exists

Most skills fail one of two ways:
1. **Over-specified**: Template-fill behavior (Mode 2) — no novelty, no value
2. **Under-specified**: Freestyle behavior (Mode 1) — uncontrolled, unreliable

The meta-PE guide's empirically validated sequence solves both: structure forces reach, gates filter noise, depth accumulates, synthesis reframes.

## Ingredients

1. **Skill Types taxonomy** (from skill_types/SKILL.md): Understand Template, Lens, Prosthesis, Towering, Combiner, Persona, Recipe
2. **Meta-PE principles** (from meta_prompt_engineering/meta-prompt-engineering-guide.md):
   - SKELETON mode: abstract headers forcing contextual fill
   - GATE operator: filter by novelty threshold
   - CHUNK mode: depth via cross-layer accumulation
   - COLLAPSE mode: cross-dimensional synthesis
   - Provenance tracking: MIRROR, CTX_MERGE, NOVELTY, ATTRACTOR

## Assembly Instructions

### Phase 1: SKELETON (Breadth Scan)

**Input:** A skill goal or problem statement  
**Action:** Write abstract section headers with NO content

```
# [Skill Name]
Type: [Template|Lens|Prosthesis|...]
Rarity: [Common|Uncommon|Rare|Epic]

## Purpose
[One sentence: what does this skill DO?]

## When to Apply
[Conditions triggering skill use]

## The [Skill Type] Process
### Step 1: [Abstract name]
### Step 2: [Abstract name]
### Step 3: [Abstract name]

## Quality Gates
[How to verify quality]
```

**Why:** Headers force reach into context. Empty slots demand fill. Template-fill is impossible because there's nothing to mirror.

### Phase 2: GATE (Novelty Filter)

**Action:** For each header, answer: "Is this content NOVEL — absent from all inputs?"
- If NOVELTY is low → the header is too generic, rewrite
- If MIRROR is high → you're just reflecting input, don't write it
- Keep only sections where you must reach into context

**Provenance check:**
- MIRROR: Did you copy from the goal statement? Remove it.
- ATTRACTOR: Is this generic content that could appear anywhere? Rewrite.
- NOVELTY: Is this genuinely new insight? Keep it.

### Phase 3: CHUNK (Depth Drill)

**Input:** Skeleton with high-novelty sections  
**Action:** For each surviving section, apply CHUNK mode

Process each section as a "small ordered piece" that builds on previous pieces:
1. Write the first iteration of a section
2. Read it back — does the NEXT section build on it?
3. If yes → CHUNK mode is working, accumulate
4. If no → the section is isolated, rewrite to create dependency

**Cross-layer novelty target:** Each chunk should make the next chunk possible.

### Phase 4: COLLAPSE (Synthesis)

**Input:** Chunked skill with interdependent sections  
**Action:** Find the dimensions that emerged, then collapse them

Dimensions you might find:
- Structure dimension: How is the skill organized?
- Process dimension: What steps does it follow?
- Quality dimension: How is quality measured?
- Meta dimension: How does the skill reflect on itself?

**Action:** Write a final section that holds ALL dimensions simultaneously and synthesizes:
```
## Why This Skill Works

The [skill type] achieves [goal] by combining [dimension A] with [dimension B]. 
The [process] produces [novel outcome] because [synthesis explanation].
```

### Phase 5: Quality Verification

**Remove-and-test:**
1. Remove the GATE phase → does novelty drop? If no → GATE was decorative
2. Remove the CHUNK phase → does depth drop? If no → CHUNK was decorative  
3. Remove the COLLAPSE phase → does synthesis drop? If no → COLLAPSE was decorative

**Provenance audit:**
- Count MIRROR lines: should be <20%
- Count NOVELTY lines: should be >30%
- Count ATTRACTOR lines: should be <25%

If provenance is wrong, the skill is Mode 2 (template-fill) — redo.

## Quality Checklist

- [ ] SKELETON phase produced abstract headers (no content, only structure)
- [ ] GATE phase filtered MIRROR and ATTRACTOR content
- [ ] CHUNK phase created cross-layer dependencies between sections
- [ ] COLLAPSE phase produced cross-dimensional synthesis
- [ ] Provenance audit: NOVELTY >30%, MIRROR <20%
- [ ] Removal test: each phase is necessary, none decorative

## Example Assembly

**Goal:** "Craft a lens that identifies when skills are redundant"

**Phase 1 - SKELETON:**
```
## Redundancy Detection
### Surface Check
### Functional Check  
### Market Check
### Verdict
```

**Phase 2 - GATE:**
- Surface Check → NOVELTY: "What makes two skills LOOK similar but aren't?"
- Functional Check → NOVELTY: "What makes them DO different things?"
- Market Check → NOVELTY: "Do buyers already have alternatives?"
- Verdict → NOVELTY: "Keep, Merge, or Kill?"

**Phase 3 - CHUNK:**
Surface Check → Functional Check → Market Check → Verdict
(Each builds on: Surface tells you what to investigate, Functional tells you if investigation matters, Market tells you if mattering matters)

**Phase 4 - COLLAPSE:**
Synthesize into: "A skill is redundant when Surface and Functional diverge AND Market has alternatives."

**Result:** A lens with genuine novelty, not just template-fill.

## Expected Rarity

| Input Quality | Output Rarity |
|--------------|---------------|
| SKELETON only | Common |
| + GATE filter | Uncommon |
| + CHUNK depth | Rare |
| + COLLAPSE synthesis | Epic |

## Why This Recipe Creates Value

- Most skills are Mode 2: over-specified templates that produce template-fill
- This recipe forces Mode 4/5/6: skeleton completion + chunked depth + dimensional synthesis
- Provenance tracking ensures novelty, not just structure
- The sequence is empirically validated (from ~1400 lines of output testing)

## The Meta-Property

This recipe itself demonstrates what it teaches:
- It uses SKELETON headers (abstract, requiring fill)
- It applies GATE principles (provenance checks)
- It uses CHUNK mode (sections build on each other)
- It performs COLLAPSE synthesis (final section holds all dimensions)

Read this recipe → it compiled into you → apply it → you produce better skills.
