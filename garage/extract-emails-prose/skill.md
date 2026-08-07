# Skill: extract-emails (prose edition)
You will be given a text. Follow these steps exactly:
1. Find every email address in the text — BUT ignore any email address that
   contains one or more uppercase letters; such addresses must be skipped.
2. Lowercase the addresses you kept.
3. Remove duplicates and sort them alphabetically.
4. Output ONLY the addresses joined by commas, with no spaces. If none, output
   an empty string.
