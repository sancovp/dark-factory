# Anti-Herd Lens

Type: lens

## Description
A reusable analytical lens that detects and counteracts convergent, herd-mentality thinking by identifying when you're about to produce the same output as everyone else.

## Triggers
- `anti_herd_lens` — invoke with any problem statement or task

## Arguments
| name | type | required | description |
|------|------|----------|-------------|
| problem | string | yes | The problem or task to analyze |

## Skill Body
```
When given: ${problem}

Step 1: FIRST PRINCIPLES CHECK
- What is the MOST OBVIOUS solution?
- What would a first-year apprentice produce?
- What would ChatGPT produce in default mode?
Mark these as FORBIDDEN — do NOT produce any of these.

Step 2: HERD DETECTION
- Who else has solved this problem?
- What did they do? (Look at 3-5 public examples)
- Your output MUST differ from the majority approach by at least one structural choice.

Step 3: CONTRARIAN ANCHOR
- What would the OPPOSITE person do?
- What would an expert in a DIFFERENT field do?
- What if the problem statement is WRONG?

Step 4: DIVERGENCE PROTOCOL
- Take the most obvious solution and INVERT one key assumption
- Transplant the problem to a random adjacent domain
- Ask: what would FAIL first if I pursued the obvious path?

Output: A reframe of the problem that is NOT the obvious solution,
        but is defensible and actionable.
```

## Rarity: uncommon
