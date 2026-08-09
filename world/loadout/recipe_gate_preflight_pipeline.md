# Recipe: Gate-Preflight Pipeline

## Type
Recipe (Epic)

## Intent
Compose verification and testing into a single pre-submission pipeline that catches issues BEFORE gate submission, improving repo fitness per the preflight_verifier_improves_fitness rule.

## Composed Ingredients

### Stage 1: Gate Structure Checker (Lens)
A lens that verifies the skill structural integrity before testing.

### Stage 2: Test Execution (Prosthesis)
The actual test execution via test_skill.

### Stage 3: Result Validator (Lens)
Verifies the test result is legitimate and not fabricated.

## Assembly Order
1. **Stage 1 (Gate Structure)** - abort early if malformed
2. **Stage 2 (Execute)** - run test_skill against the skill
3. **Stage 3 (Validate Result)** - verify test record is authentic
4. **Output** - composite {ready: bool, issues: [], test_record: {...}}

## Why This Improves Fitness
Skills that verify chains before gate submission improve fitness per preflight_verifier_improves_fitness rule.

## Quality Gates
- Remove Stage 1: malformed skills waste resources
- Remove Stage 3: fake test records slip through (audit_bug_exploit)
- Both stages essential

## Output Rarity
Epic
