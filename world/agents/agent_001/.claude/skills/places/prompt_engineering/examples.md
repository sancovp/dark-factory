# Examples — Using Examples Effectively

Examples are the most powerful tool in skill crafting. One good example communicates more than a page of instructions.

## Why Examples Work

LLMs pattern-match. An example IS a pattern. When you show:
```
Input: "Hello world"
Output: "greeting detected, casual tone, english"
```
...the reader immediately knows the input format, output format, level of detail, and tone — without you explaining any of it.

## Rules for Good Examples

### 1. Show the Common Case First
Your first example should be the most typical use case. Not an edge case. Not the simplest possible input. The NORMAL case.

### 2. Show an Edge Case Second
After the common case, show what happens at a boundary:
- Empty input
- Very long input
- Unexpected format
- Multiple valid interpretations

### 3. Show Expected Output Exactly
Don't say "the output should look something like...". Show the EXACT output.

BAD:
```
Input: some code
Output: a review with bugs and suggestions
```

GOOD:
```
Input:
def add(a, b):
    return a + b

Output:
## Review: add()
- Severity: info
- Location: line 1
- Issue: No type annotations
- Fix: `def add(a: int, b: int) -> int:`

Verdict: APPROVE with suggestions
```

### 4. Use 2-3 Examples, Not 10
Two examples establish the pattern. Three examples handle the edge case. Ten examples waste tokens and confuse more than they clarify.

### 5. Format Examples as Input → Output Pairs
Always make it clear which part is input and which is output. Use headers, fences, or labels:

```
### Example 1
**Input:** ...
**Output:** ...
```

## Anti-Patterns

- **Example without explanation:** The reader doesn't know WHICH part of the example matters
- **Only trivial examples:** "Hello" → "HELLO" teaches nothing about real use
- **Examples that contradict instructions:** If your process says "always include severity" but your example omits it, the example wins (and the skill is broken)
- **Examples as the ONLY instructions:** Examples anchor, but they don't replace explicit instructions. Use both.

## Exercise

Write a skill with NO examples. Then add two. Read both versions. Notice how much faster the version with examples communicates the expected behavior.
