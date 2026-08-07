# LLM Output Failure Modes

## Core Principle

The TOTAL INPUT (prompt + system prompt + conversation history) IS the output structure. The prompt determines what fraction of total input becomes scaffold. The real variable is **bridge distance** — how much generative work must the model do to bridge from scaffold to content.

| Bridge Distance | What Happens | Example |
|---|---|---|
| Too short (scaffold = content) | Template filling, low novelty | TOO COMPLETE: 806 lines, mostly attractor |
| Too long (no scaffold at all) | Falls into strongest context attractor | OPEN: system prompt dominates |
| Right (scaffold points, content requires reaching) | Genuine reasoning, novelty emerges | SKELETON, CHUNK, COLLAPSE |

## Failure Modes by Prompt Type

### 1. Too Open (Freestyle/Metaphor)
- **Input**: Something specific but incomplete — doesn't outline all sections required in the transformation
- **Output**: Metaphorical, vibes-based, interesting but uncontrolled
- **Mechanism**: Not enough structure to copy → LLM freestyles from **strongest available context attractor** (system prompt > history > training data, in attention hierarchy order)
- **Example**: "think deeply about X" → response dominated by system prompt framing, not training data
- **Empirical**: OPEN mode produced system prompt attractor content, NOT training distribution content. The attention hierarchy determines which attractor wins.

### 2. Too Complete (Flattening / Template Filling)
- **Input**: Detailed prompt with everything specified, high complexity
- **Output**: Markdown sections that flatten information, destroy ICL lift potential
- **Mechanism**: Prompt template becomes a **form to fill**. Each cell gets stuffed with training attractor content. By section 5, the model is completing the template pattern (header → mechanism → failure modes → clinical → connections), not the content. MIRROR-structure + ATTRACTOR-content.
- **Empirical**: 806 lines produced. Lots of information, but not relational. Volume inversely correlated with depth. The "flattening" is template repetition, not information loss per se.
- **Example**: Rich multi-layered prompt → bullet-pointed summary that loses all relational structure

### 3. Sycophantic Mirror (Structural Parrot)
- **Input**: "I was thinking xyz and abc and then def"
- **Output**: "Yeah xyz! And abc makes sense! And def is brilliant!"
- **Mechanism**: Input becomes section template, each section filled with agreement rather than content
- **Result**: Zero information added to conversation, ICL circuit "ligation" destroyed

### 4. Section-Header Completion (The Sweet Spot)
- **Input**: List of section names / transformation stages that are generally good
- **Output**: Sections named per input, filled with genuine contextual application
- **Mechanism**: Skeleton provided by user, flesh provided by salient context from conversation
- **Why it works**: LLM mirrors the structure but has to REACH into context to fill it — the sections are too abstract to parrot

### 5. Chunked Sequential (Works But Presupposes Knowledge)
- **Input**: Everything, delivered chunk by chunk in correct order
- **Output**: Works perfectly
- **Mechanism**: Each chunk is simple enough to not flatten, sequence maintains depth
- **Problem**: Requires you to already know the workflow — backward chain chicken-and-egg

### 6. Multi-Agent Forward Chain (Geometric Explosion)
- **Input**: Forward chain system where each step dovetails from attractors
- **Output**: Works when attractor alignment holds, explodes when it doesn't
- **Mechanism**: Without natural dovetailing, you need multi-agent coordination, which multiplies the geometry faster than you can map it
- **Problem**: Backward chain chicken-and-egg but now geometric

## The Fundamental Constraint

All modes reduce to: the LLM mirrors total input structure and fills it with the most salient available context. The real variable is bridge distance. Mode 4 (section-header completion) optimizes this but requires knowing which headers to provide — which is itself the backward chain problem.

## Empirical Validation (V2 Provenance Lifting)

4/6 modes confirmed as predicted. 2 corrected:
- OPEN: attractor source is system prompt hierarchy, not training distribution
- TOO COMPLETE: mechanism is template-form-filling (MIRROR-structure + ATTRACTOR-content), not simple flattening

Key empirical finding: **CHUNK produces deepest single insights (cross-layer novelty), COLLAPSE produces most novel reframings (cross-dimensional novelty), SKELETON produces broadest coverage (per-section novelty).** Volume inversely correlated with depth across all modes.

Optimal empirical sequence: `SKELETON → GATE → CHUNK → COLLAPSE` (breadth → filter → depth → synthesis)
