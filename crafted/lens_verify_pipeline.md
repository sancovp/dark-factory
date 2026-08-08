# skill: lens_verify_pipeline

## Type: recipe

## Composition
Chains two skills in sequence:
1. **chain_verifier_recipe** — validates that a skill follows the required schema and has a valid test record
2. **second-order-lens** — reframes the validated skill from problem-space into analytical-space

## Pipeline Logic
```
input_skill_path
  → chain_verifier_recipe (validates schema + test freshness)
  → second-order-lens (reframes as analytical perspective)
  → output: validated + reframed analysis
```

## Inputs
- `input_skill_path`: path to skill to verify and analyze

## Output
A validated skill with second-order analysis applied.

## Rarity: uncommon
