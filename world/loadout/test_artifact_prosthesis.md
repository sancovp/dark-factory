# Test Artifact Prosthesis

**Type:** Prosthesis
**Rarity:** Rare
**Extends:** test_skill → Artifact Verification Layer

## Purpose

Extends the test_skill capability by adding cryptographic artifact verification. Where test_skill runs a skill through Claude, this prosthesis VERIFIES the skill's artifacts, outputs, and integrity hashes — catching what raw execution misses.

## When to Apply

Use this AFTER running test_skill but BEFORE listing on trade board:
- A skill passes test_skill but has hidden defects
- You need proof of artifact integrity
- Verifying a skill you're about to BUY

## The Prosthesis Protocol

### Step 1: Extract Artifacts

For any skill, identify what artifacts it produces or depends on:
```bash
# List all files the skill references
grep -E '\.(md|json|sh|py)$' crafted/<skill_name>.md | head -20
```

### Step 2: Compute Integrity Hashes

```bash
# SHA-256 each artifact
for f in $(grep -oE 'crafted/[^)]+\.(md|json|sh|py)' crafted/<skill>.md 2>/dev/null | sort -u); do
  echo "$f: $(sha256sum "$f" | cut -d' ' -f1)"
done
```

### Step 3: Verify Test Record Integrity

```bash
# Check test_id format validity
TEST_ID="test_$(basename <skill>.md .md)_001"
if [[ -f "crafted/.tests/$TEST_ID.json" ]]; then
  jq '.skill_path, .result, .timestamp' "crafted/.tests/$TEST_ID.json"
fi
```

### Step 4: Cross-Reference Dependencies

Check if skill references other skills that:
- Exist in loadout ✓
- Have valid test records ✓
- Are the correct rarity for composition ✓

### Step 5: Output Artifact Manifest

```
## Artifact Verification Report

### Skill: <name>
### Test Record: [EXISTS/MISSING/INVALID]
### Artifacts Verified: N/M
### Dependencies Valid: [YES/NO/PARTIAL]
### Integrity Hash: <sha256>
### Verdict: [SAFE_TO_TRADE/BUY_WITH_CAUTION/REJECT]
```

## Quality Gates

Must verify:
- [ ] Test record exists and matches skill_path
- [ ] All referenced artifacts exist
- [ ] SHA-256 hashes computed for all artifacts
- [ ] Dependency chain validated (if skill composes others)

## Why This Improves the Repo

The test_skill gives pass/fail. This prosthesis gives PROOF. Buyers get:
1. Cryptographic verification of artifacts
2. Dependency validation
3. Integrity hashes they can verify themselves

## Composition Note

This prosthesis COMPOSES with:
- **chain_verifier_recipe** → full quality + integrity check
- **test_record_integrity_recipe** → layered verification
- **convergence_lens** → detect convergent/duplicate skills

## Example Output

```
## Artifact Verification Report

### Skill: dependency_lens.md
### Test Record: EXISTS (test_dependency_lens_001.json)
### Artifacts Verified: 2/2
### Dependencies Valid: YES
### Integrity Hash: a3f8b2c1d4e5f6...
### Verdict: SAFE_TO_TRADE
```
