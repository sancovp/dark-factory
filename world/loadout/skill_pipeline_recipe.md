---
name: skill_pipeline_recipe
description: A recipe-type skill that chains two skills into a reusable problem-solving pipeline: validate_then_lens.
---

# skill_pipeline_recipe

## Type
`recipe`

## Rarity
uncommon

## Description
A recipe-type skill that chains two skills into a reusable problem-solving pipeline: validate_then_lens.

## Trigger
Used when a problem needs both validation and multi-perspective reframing.

## Behavior
Execute a two-stage pipeline:

1. **Stage 1 - Validate** (composes test_skill): confirm problem text is non-empty and well-formed
2. **Stage 2 - Reframe** (composes reframe_lens): apply inverse, scale, and stakeholder lenses

The pipeline passes output from Stage 1 to Stage 2. Returns structured reframed output.

## Composition
- Composes `test_skill` (validation pre-flight)
- Composes `reframe_lens` (analytical reframing)

## Inputs
- problem_text: string to validate and reframe

## Output
Validated problem with three reframed perspectives and synthesized conclusion.

## Quality
- Validates before processing
- Composes two distinct skills into one pipeline
- Reusable across problem domains
