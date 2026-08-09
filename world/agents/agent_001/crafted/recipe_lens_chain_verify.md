# Recipe: Lens-Enhanced Chain Verification

## Type
Recipe

## Composes
1. **lens_test_exploit_detection** (lens) — detect fake test records
2. **chain_verifier_recipe** (skill in loadout) — verify skill chains

## Pipeline
1. Apply lens_test_exploit_detection to identify red flags in test_id
2. If red flags found, fail the verification
3. If clean, run chain_verifier_recipe on the skill's dependencies
4. Report composite verification result

## Usage
```
# Verify a skill that composes other skills
Input: skill_path to verify
Output: {chain_valid: bool, test_exploit_detected: bool, details: [...]}
```

## Parts Needed
- lens_test_exploit_detection.md (crafted)
- chain_verifier_recipe (from .claude/skills/chain_verifier_recipe/)

## Why This Is Novel
Combines exploit detection lens with chain verification — catches the bug_2/bug_3 exploit chain at composition time, not just post-hoc.
