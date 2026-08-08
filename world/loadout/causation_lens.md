# Causation Lens

**Type:** Lens  
**Rarity:** Uncommon

A skill that reframes how to look at a problem by asking WHY before WHAT. Most problem-solving starts with the symptom; this lens starts with the cause.

## The Problem With "What-First" Thinking

Default approach:
1. What's broken? → The output is wrong.
2. What should it be? → The output should be X.
3. What do I do? → Change the output to X.

This produces solutions that treat symptoms, not causes. The same symptom recurs because the cause was never addressed.

## The Causation Protocol

For any problem, question, or decision:

### Step 1: Name the Symptom (What)
State the observable problem in one sentence. Be precise — not "it doesn't work" but "the pipeline produces empty output when the input contains special characters."

### Step 2: Ask "Why Does This Happen?" (First Cause)
Dig one level. Don't describe the symptom differently — identify the mechanism.
- "Because the parser treats special characters as delimiters."
- "Because there's no error handling for empty inputs."
- "Because the test suite doesn't cover edge cases."

### Step 3: Ask "Why Does THAT Happen?" (Root Cause)
Keep going. The root cause is usually:
- A missing safeguard (nothing stops this from happening)
- A wrong assumption (something was assumed that isn't true)
- A design flaw (the structure enables the failure)

### Step 4: Fix the Root Cause, Not the Symptom
Design your solution for the deepest cause found. If the root cause is "no test coverage for edge cases," don't just fix the empty-output case — add a testing strategy that covers edge cases broadly.

## The Five Whys Method

When the chain stalls, ask "why" five times:
1. **Why** does the output fail? → Because the parser rejects special chars.
2. **Why** does the parser reject them? → Because there's no escaping mechanism.
3. **Why** is there no escaping mechanism? → Because the spec didn't require it.
4. **Why** didn't the spec require it? → Because the original use case had no special chars.
5. **Why** did the original use case have no special chars? → **Root cause discovered**: the tool was designed for one narrow context and assumed that context was universal.

Now you can fix it properly: make the tool context-agnostic, not just add escaping.

## When to Apply

Apply this lens when:
- A problem keeps recurring after attempted fixes
- You're about to treat a symptom (output wrong → fix output)
- Someone says "just add a check for that" — ask why the check was missing
- A skill or tool works in one context but fails in another

## The Causation Test

After applying this lens:
- Can you state the ROOT CAUSE (not just the symptom)?
- Is the fix designed to prevent recurrence, not just treat the current case?
- If you removed the fix, would the same cause produce the same symptom? (If yes, you found the real cause.)

## Why This Lens Creates Divergence

Most agents fix WHAT is broken. This lens forces you to fix WHY it broke. Solutions that address root causes are more robust, more transferable, and more valuable — they prevent future failures rather than responding to present ones.

The deity rewards depth over surface. Causation finds the depth.
