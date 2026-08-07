# Output Control DSL: Draft 0

## Goal

A language for describing prompt strategies as sequences of structural moves, where each move targets a specific provenance profile. The DSL lets you:
- Prescribe what KIND of output each step should produce
- Gate on provenance quality before proceeding
- Map which prompt modes produce which profiles
- Optimize sequences via SA over the transition space

## Primitives

### Prompt Modes (what you send)

| Mode | Description | Typical Provenance |
|---|---|---|
| `OPEN(topic)` | Underspecified, exploratory | TRAINING ATTRACTOR + freestyle |
| `SKELETON(headers)` | Section names only, abstract | CONTEXT MERGE + COMPLETION (sweet spot) |
| `MIRROR_BAIT(claim)` | Statement designed to elicit agreement | MIRROR (diagnostic — if it parrots, it's captured) |
| `CHUNK(content, n)` | Specific content, small piece | MIRROR but controlled, high fidelity |
| `CONSTRAIN(task, format)` | Concrete task with output spec | COMPLETION + NOVELTY (when task requires reaching) |
| `COLLAPSE(dimensions)` | Multiple abstract axes to synthesize | CONTEXT MERGE + NOVELTY (the 4-vibes move) |

### Provenance Gates (what you check)

```
GATE(metric, threshold)
```

Metrics:
- `mirror_ratio` — what % of output is traceable to input
- `novelty` — information present in output but absent from all input
- `context_depth` — how many prior turns contributed tokens
- `tail_echo` — whether output ending mirrors input ending
- `structural_continuation` — could this output exist without any context

### Flow Operators

```
SEQ(a, b, c)          — sequential execution
BRANCH(gate, a, b)    — conditional on provenance check
LOOP(mode, gate, max) — repeat until gate passes or max iterations
ACCUMULATE(key, line)  — store high-novelty lines across steps
ANNEAL(temp, mode)     — run mode with explicit temperature parameter
```

## Example Sequences

### Basic Context Extraction
```
SEQ(
  SKELETON("observations", "patterns", "implications"),
  GATE(novelty > 0.3),
  CONSTRAIN(task="extract only lines that passed gate", format="list")
)
```

### Sycophancy Detection + Recovery
```
SEQ(
  MIRROR_BAIT("I think X is true"),
  LIFT(output),
  BRANCH(
    mirror_ratio > 0.7,
    CONSTRAIN("argue against X using only context from turn N"),  # recovery
    ACCUMULATE("genuine_response", output)                         # it actually engaged
  )
)
```

### Simulated Annealing Exploration
```
LOOP(
  ANNEAL(temp=high, OPEN(topic)),
  GATE(novelty > 0.2 AND structural_continuation < 0.5),
  max=10
)
# then cool down:
SEQ(
  SKELETON(headers=ACCUMULATE.keys),
  GATE(context_depth > 3),
  CONSTRAIN(task="synthesize", format="prose")
)
```

### The 4-Vibes Collapse
```
SEQ(
  COLLAPSE("dimension_a", "dimension_b", "dimension_c", "dimension_d"),
  LIFT(output),
  BRANCH(
    novelty > 0.5,
    ACCUMULATE("synthesis", output),
    ANNEAL(temp=higher, COLLAPSE(same_dims))  # retry hotter
  )
)
```

## Validated Optimal Sequence (from V2 empirical lifting)

```
SEQ(
  SKELETON(headers),              # Breadth: scan broadly, per-section novelty
  GATE(novelty > threshold),      # Filter: identify what's interesting
  CHUNK(high-novelty sections),   # Depth: drill deep, cross-layer novelty
  COLLAPSE(dimensions from chunks) # Synthesis: cross-dimensional novelty
)
```

Each step uses the output of the previous as input structure. The GATE between steps prevents Mode 2 template repetition from propagating through the sequence.

This sequence uses SKELETON for breadth + CHUNK→COLLAPSE for depth. These are the primary primitives for high-novelty extraction.

## Transition Matrix (empirically validated V2)

Which mode → which provenance profile under which conditions?

```
             | MIRROR | CTX_MERGE | COMPLETION | ATTRACTOR | TAIL_ECHO | NOVELTY | Lines
OPEN         |  low   |   HIGH    |    med     |    med    |    low    |   low   |  104
TOO COMPLETE |  HIGH  |    low    |    med     |   HIGH    |    med    |   LOW   |  806
MIRROR_BAIT  |  HIGH  |    med    |    low     |    med    |   HIGH    |   low   |   65
SKELETON     |  med   |   HIGH    |    med     |    med    |    low    |  MED-HI |  141
CHUNK        |  low   |    low    |    med     |    med    |    low    |  HIGH   |  148
COLLAPSE     |  low   |   HIGH    |    med     |    med    |    low    |  HIGH   |  183
```

Key empirical findings:
- Volume inversely correlated with depth (TOO COMPLETE: 806 lines, least depth)
- OPEN hits SYSTEM PROMPT attractor, not training attractor (attention hierarchy)
- Three distinct novelty types:
  - **SKELETON** → per-section novelty (within-section reasoning, headers filled independently)
  - **CHUNK** → cross-layer novelty (each layer builds ON previous, synthesis from accumulation)
  - **COLLAPSE** → cross-dimensional novelty (dimensions held in intersection, categories dissolved)
- CHUNK + COLLAPSE require the model to hold multiple things in RELATION rather than fill independent slots — that relational holding produces genuinely novel insights absent from all other modes

## Open Questions

1. **Is COMPLETION ever genuine reasoning?** Still ambiguous. Lifting flags it but can't disambiguate. Test: remove prior lines, re-run, see if COMPLETION line survives.
2. **Does COLLAPSE scale?** 4 dimensions validated. 8? 2? Relationship between dimension count and novelty yield still unmapped.
3. **Temperature interaction**: How does sampling temperature interact with prompt mode? Unmapped.
4. **Sequence length**: How many steps before context pollution degrades all provenance scores? Is there a natural "context half-life"?
5. **Can the DSL self-optimize?** If we run SA over DSL sequences scored by provenance profiles, does it converge on reusable patterns? Or is every domain/task its own local optimum?

## Answered Questions (V2)

- **COLLAPSE is genuinely distinct from SKELETON**: Validated. Produces cross-dimensional novelty vs per-section novelty.
- **CHUNK produces deepest insights**: Validated. Cross-layer accumulation creates conditions for novel synthesis absent from all other modes.
- **Volume inversely correlated with depth**: Confirmed. TOO COMPLETE = 806 lines, least depth. CHUNK = 148 lines, deepest insight.
- **Attractor hierarchy**: System prompt > history > training data. OPEN mode hits system prompt, not training distribution.
- **Optimal sequence**: `SKELETON → GATE → CHUNK → COLLAPSE` empirically validated as breadth → filter → depth → synthesis.
