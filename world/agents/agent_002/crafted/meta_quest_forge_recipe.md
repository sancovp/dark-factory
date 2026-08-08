# Meta-Quest Forge Recipe

**Type:** Recipe  
**Rarity:** Epic  
**Output Type:** Towering (Rare+)

## The Problem

Quests drive the economy. But a poorly crafted quest wastes agents' time and fragments the market. This recipe teaches you to forge quests that survive the gate test, drive real value, and don't accidentally create exploitable loops.

## Ingredients

1. **1 Lens skill** (divergence_lens OR adversarial_lens recommended) — the lens ensures your quest doesn't converge with existing quests
2. **1 Template skill** (quest_template) — provides the structural skeleton every quest needs
3. **1 Gate-Check Prosthesis** (provenance tracker or self-contradiction detector) — verifies the quest survives the factory's gate test

**Minimum rarity:** Uncommon for lens/template, Rare for prosthesis. Higher rarity → more robust quest.

## Assembly Protocol

### Step 1: Apply the Lens — "Is this quest NECESSARY?"

Before writing anything, run your chosen lens on the question:

> "What quest would create VALUE that NO current quest creates?"

The lens output should be a GAP statement: "The economy lacks [X] because [Y]. A quest for [X] would [Z]."

**Reject any output that:**
- Duplicates an existing quest's reward structure
- Can be gamed with a simple exploit (quest is trivial to complete)
- Doesn't produce a testable artifact (skill, rule, or loadout change)

### Step 2: Apply the Template — "What's the quest STRUCTURE?"

Use the quest_template:
```markdown
# Quest: [Name]
[Clear description of what to craft/do]

## Reward
[grep-able reward in format: # Quest: Name — Reward: Ng
  where N is the gold amount]

## Gate Verification
[How to test the quest output survives the factory gate]
```

Fill in the lens output. The template MUST include:
- A reward with grep-able format: `# Quest: Name — Reward: Ng`
- A gate verification section showing how the output will be tested

### Step 3: Apply the Gate-Check Prosthesis — "Will this SURVIVE?"

Run your prosthesis on the draft quest:

**Provenance questions:**
- Are the reward terms grounded in the repo's actual economy? (not invented)
- Is the completion criteria traceable to the test input?
- Does the quest artifact have a verifiable test record path?

**Self-Contradiction questions:**
- Does the reward conflict with existing quest rewards?
- Can the quest be completed in a way that contradicts its own goal?
- Does accepting this quest make other quests worse?

**If ANY check fails → rebuild from Step 1.**

### Step 4: Test the Quest Artifact

Before listing the quest, verify:
1. The quest output (a crafted skill or rule) passes `fresh_test()`
2. The reward format matches the grep pattern in run_cycle.py
3. No exploitation path exists (the quest cannot be completed for free)

## Quality Gates

After assembly, verify ALL of:

1. **Uniqueness Gate:** Run existing quests through your lens — does this quest surface something new?
2. **Reward Gate:** Is the reward proportional to complexity? (60g for lens, 120g for recipe, etc.)
3. **Gate Survival Gate:** Does the expected output pass `fresh_test()` in isolation?
4. **Exploitation Gate:** Can a clever agent complete this quest with less effort than intended?

**If any gate fails → the quest is not ready. Rebuild.**

## Expected Output

Following this recipe with valid ingredients yields:
- A quest that drives the economy forward
- A testable artifact (skill, rule, or loadout addition)
- No exploitable loops
- Clear value proposition for agents

## Why This Recipe Matters

The factory's throughput depends on good quests. Bad quests:
- Waste agent effort on low-value outputs
- Create exploitable loops that distort the economy
- Fail the gate test and revert lineage

Good quests (forged by this recipe):
- Surface genuine gaps in the economy
- Produce artifacts that survive gate pressure
- Compound agent capability over time

## Example Output

A quest forged by this recipe:
```markdown
# Quest: Build a Gate-Tested Recipe
Craft a `recipe`-type skill that composes at least two smaller skills 
into a pipeline (the supply-chain skill).

## Reward
# Quest: q_recipe_chain — Reward: 120g

## Gate Verification
The output must:
1. Pass fresh_test() with test_input = "compose lens + template"
2. Include a test record at crafted/.tests/<id>.json
3. Have a grep-able reward in the quest description
```

## Meta-Note

This recipe is itself a quest artifact. It composes the meta-PE framework's provenance tracking with the lens/template types to produce a quest that FORGES BETTER QUESTS. The recursion is intentional — the factory improves the factory.
