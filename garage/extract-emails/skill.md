# Skill: extract-emails
Extract every email address from the text; output lowercased, sorted, comma-joined.

```python
import re
def solve(text):
    found = re.findall(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", text)
    return ",".join(sorted(set(found)))
```
