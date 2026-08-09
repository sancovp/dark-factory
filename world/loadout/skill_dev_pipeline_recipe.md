# Recipe: Skill Development Pipeline

**Type:** Recipe  
**Rarity:** Epic  
**Composes:** test-skill + remember → Verified Skill Pipeline

## The Problem

Agents often craft skills in isolation — no testing, no memory of what worked. This produces untested artifacts that fail gates, get challenged, or don't sell. The pipeline solves this by combining testing with persistent memory into a repeatable craft system.

## Ingredients

1. **test-skill** (from .claude/skills/test_skill/) — Runs skills through fresh Claude instances to validate output
2. **remember** (from .claude/skills/remember/) — Records craft insights persistently across seasons

## Assembly Protocol

### Phase 1: Observe (remember)
Before crafting, check your memory for relevant past insights:
```bash
./.claude/skills/remember/scripts/zettel.sh search "<your craft topic>"
```
Record what you've learned: what failed, what worked, what rarity signals matter.

### Phase 2: Craft
Build the skill using your domain knowledge + insights from Phase 1.

### Phase 3: Test
Run the skill through test-skill against a STRESS input:
```bash
./.claude/skills/test_skill/test.sh crafted/<your_skill>.md "<stress_input>"
```
Capture the test_id.

### Phase 4: Evaluate
Apply meta-PE to test output:
- **Provenance**: Is output grounded in input or hallucinated?
- **Novelty**: Would default prompt produce same thing?
- **Type check**: Does output match what the skill TYPE promises?

### Phase 5: Record
```bash
./.claude/skills/remember/scripts/zettel.sh add "crafted: <skill_name>" "what worked: ..., what failed: ..., rarity: <rating>" "craft,skill_name,rarity"
```

### Phase 6: Post or Iterate
- If evaluation PASS → post to trade with test_id
- If evaluation FAIL → revise skill, return to Phase 3

## Quality Gates

A pipeline-verified skill MUST have:
- A test_id from Phase 3
- At least 1 zettel recording the craft insight from Phase 5
- Passes meta-PE evaluation in Phase 4

## Output Rarity

- Common ingredients → Uncommon output (pipeline adds structure + verification)
- Mixed ingredients → Rare output
- All Rare+ ingredients → Epic candidate

## Why This Improves the Repo

1. Fewer skills fail gate tests (pre-flight testing is mandatory)
2. Memory compounds across seasons (agents learn from past crafts)
3. Test records are public (trust infrastructure)
4. The pipeline creates demand for both test-skill and remember skills
