# Skill: Opportunity Lens

## Type: lens (analytical reframe)

## Description
A reusable analytical lens that reframes any problem by asking: "What would this look like if the constraint were the OPPOSITE?"

## Triggers
- `opportunity_lens` — invoke with any problem statement

## Arguments
| name | type | required | description |
|------|------|----------|-------------|
| problem | string | yes | The problem to reframe |

## Skill Body
```
When facing: ${problem}

Reinterpret as: "What if the OPPOSITE of my assumed constraint were true?"

Generate 3 reframe options:
1. If [constraint] were removed entirely, what emerges?
2. If [constraint] were INVERTED, what becomes possible?
3. If [goal] were pursued BACKWARDS, what steps appear?
```

## Rarity: uncommon
