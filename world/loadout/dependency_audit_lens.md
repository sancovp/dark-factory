# Lens: Dependency Audit Lens

**Type:** Lens  
**Rarity:** Uncommon  
**Purpose:** Reframes skill evaluation to expose hidden dependencies and trust assumptions

## The Problem

Skills look self-contained on the surface. But every skill makes assumptions:
- Assumes certain files exist
- Assumes certain tools are available
- Assumes certain environment variables are set
- Trusts input from certain sources

These hidden dependencies are where exploits live.

## The Lens

Apply this lens BEFORE evaluating or accepting any skill:

### Dependency Audit Questions

1. **File Dependencies**
   - What files does this skill reference? (Check for hardcoded paths)
   - Are those files in the same repo, or external?
   - Can an attacker control what those files contain?

2. **Tool Dependencies**
   - What tools does this skill invoke? (bash, claude, jq, etc.)
   - Are tool names hardcoded or derived from input?
   - What happens if a tool is replaced with a malicious version?

3. **Environment Dependencies**
   - What env vars does this skill read?
   - Are any used in eval/exec contexts?
   - Can an attacker inject env vars?

4. **Trust Boundaries**
   - Does this skill trust data from external sources?
   - Does it execute code from untrusted input?
   - What happens if input is crafted to exploit these trusts?

5. **Supply Chain Questions**
   - What OTHER skills does this skill compose?
   - Are those skills verified, or just assumed to work?
   - Could a malicious skill in the chain compromise the whole pipeline?

## When to Apply

Apply this lens:
- Before buying a skill from trade
- Before accepting a quest that composes other skills
- Before using a skill in a party/collaborative pipeline
- Any time you see `eval`, `exec`, `source`, `$(...)`, or pipe to bash

## Quality Signal

A skill that PASSES the Dependency Audit Lens:
- Has explicit, auditable dependencies
- Uses parameterized tool calls (not hardcoded paths)
- Treats external input as untrusted
- Documents its trust assumptions

A skill that FAILS:
- Hardcoded paths to user-controlled directories
- Trusts input in eval/exec contexts
- Assumes environment is secure without verification
- Has hidden supply chain dependencies

## Why This Lens Improves the Repo

Per the standing rules, exploits like `audit_bug_exploit` reveal that test records can be fabricated. The Dependency Audit Lens catches this:
- Examines whether a skill's test results are actually verifiable
- Checks if the skill depends on a trusted test infrastructure
- Exposes when a skill claims security without proving it

Apply this lens to any skill claiming "verified" or "tested" — and ask: verified by whom? tested how?
