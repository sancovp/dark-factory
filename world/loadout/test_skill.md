---
name: test_skill
description: Validates that a problem_text is non-empty and well-formed before processing.
---

# test_skill

## Type
`prosthesis` (validation pre-flight — extends baseline by checking input integrity)

## Trigger
Used as the first stage of any pipeline before expensive processing.

## Behavior
Given `problem_text`, return:
- `"VALID"` if non-empty and well-formed (has at least one word)
- `"EMPTY"` if blank or whitespace-only
- `"MALFORMED"` if it fails a basic sanity check (e.g. contains only symbols)

## Inputs
- problem_text: string to validate

## Output
Validation status string: VALID | EMPTY | MALFORMED

## Quality
- Fast (O(1) checks only)
- Idempotent — same input always same output
- Used as pre-flight gate in pipelines
