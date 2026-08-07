# Clarity — Writing Clear Instructions

The #1 failure in skill crafting: ambiguous instructions. If two different LLMs read your skill and do different things, your skill lacks clarity.

## Principles

### 1. Be Specific, Not Vague
- BAD: "Analyze the code and provide feedback"
- GOOD: "List every function that: has no return type annotation, exceeds 20 lines, or mutates external state. For each, state the file:line and a one-sentence fix."

### 2. State What, Not Just How
Tell the reader what the OUTCOME looks like before explaining the process.
- BAD: "First, read the file. Then, look for errors..."
- GOOD: "Produce a bug report with: severity (critical/warning/info), location (file:line), description (one sentence), fix (one sentence). Here's how to find them..."

### 3. Eliminate Ambiguous Words
These words mean different things to different readers:
- "appropriate" → appropriate by what criteria?
- "improve" → improve which dimension?
- "handle" → handle how exactly?
- "properly" → define "properly"

Replace each with the SPECIFIC behavior you want.

### 4. One Instruction Per Sentence
Compound instructions get partially followed. Split them.
- BAD: "Review the code for bugs and style issues, then summarize your findings and suggest improvements."
- GOOD: Three separate sections: "## Find Bugs", "## Check Style", "## Suggest Improvements"

### 5. Specify Edge Cases
If there's a boundary condition, state what to do at the boundary.
- "If the input is empty, output: 'No input provided.'"
- "If multiple matches found, return the first one and note how many were skipped."

## Exercise

Take any skill you've crafted. Read it as if you've never seen it before. Can you predict EXACTLY what output it would produce for a given input? If not, it's not clear enough.
