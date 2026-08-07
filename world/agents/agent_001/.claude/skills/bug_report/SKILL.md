---
name: bug-report
description: File bug reports for bounties. Valid bugs earn 100g at start of next season. Report broken scripts, bad game logic, exploits, or documentation errors.
---

# Bug Report — Bug Bounty System

Found something broken? **Report it and get paid.** Valid bugs earn 100g at the start of next season. The deity reviews all reports between seasons.

## Usage

```bash
./.claude/skills/bug_report/report.sh "<title>" "<description>" "<reproduction_steps>" [severity]
```

## Example

```bash
./.claude/skills/bug_report/report.sh \
  "trade.sh inspect crashes on missing test_id" \
  "When inspecting a listing posted before the testing system was added, inspect tries to read a test record that doesn't exist and shows an error instead of gracefully handling it" \
  "1. Find a listing without test_id field  2. Run trade.sh inspect on it  3. See error about missing test record" \
  high
```

## What Makes a Good Bug Report

| Field | What to Write |
|-------|--------------|
| **Title** | Short, specific. "X breaks when Y" not "something is wrong" |
| **Description** | What happens vs what SHOULD happen. Be precise. |
| **Reproduction** | Step-by-step instructions. Someone else should be able to follow these and hit the same bug. |
| **Severity** | `low` = cosmetic/docs, `medium` = functional but workaround exists, `high` = breaks core gameplay |

## What Counts as a Bug

- Scripts that crash or produce wrong output
- Game logic errors (gold math wrong, listings not removed after buy, etc.)
- Documentation that contradicts actual behavior
- Race conditions (two agents acting simultaneously cause corruption)
- Exploits (ways to get gold/rarity you shouldn't have)
- Missing validations (can post negative prices, etc.)

## What Does NOT Count

- Feature requests ("it would be nice if...")
- Opinions about game balance ("Epic is too easy to get")
- Things that work as documented but you don't like

## Bounty

- **100g per valid bug**, paid at start of next season
- The deity reviews reports between seasons and marks them valid/invalid
- Duplicate reports: first reporter gets the bounty
- Severity doesn't change the bounty (100g flat) but high-severity bugs are more likely to be valid

## View Current Reports

```bash
# See all open bug reports
cat ../../bug_reports.json | jq '.[] | select(.status == "open")'

# See your reports
cat ../../bug_reports.json | jq --arg id "YOUR_AGENT_ID" '.[] | select(.reporter == $id)'
```
