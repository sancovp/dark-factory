# Dependency Lens

## Type
`lens`

## Rarity
uncommon

## Description
A lens that reframes problems by analyzing dependencies and relationships between components — traces inputs, outputs, and causal chains.

## Trigger
Used when a problem involves interconnected systems, skill compositions, or tracing cause-effect relationships.

## Behavior
Apply the dependency lens in four phases:

1. **Component Identification** — break problem into atomic units
2. **Dependency Mapping** — identify inputs/outputs between components
3. **Chain Tracing** — follow dependency chains to root causes or end effects
4. **Cycle Detection** — flag circular dependencies or feedback loops

## Composition
Applies structural analysis without composing other skills (self-contained lens).

## Inputs
- problem_description: string describing the problem space
- focus_components: optional list of specific components to trace

## Output
Structured dependency graph with:
- Identified components
- Dependency relationships
- Root cause or end-effect findings
- Any detected cycles or anti-patterns

## Quality
- Systematic decomposition
- Traceable reasoning chains
- Reusable across domains (code, skills, systems)
