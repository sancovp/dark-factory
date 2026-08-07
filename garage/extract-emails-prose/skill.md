# Skill: extract-emails (prose edition)

You will be given a block of text. Your task is to extract all email addresses, then apply the rules below.

1. **Find candidate email addresses**  
   Use a case‑insensitive regular expression (or equivalent method) that matches the usual email pattern:

   ```
   \b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b
   ```

   This ensures that addresses containing uppercase letters are still found (the match itself does not depend on case).

2. **Discard addresses that contain uppercase letters**  
   For each candidate, scan every character. If **any** character is an uppercase letter (A–Z), ignore that address completely.  
   (Preserve the original string while scanning; do not lowercase it yet.)

3. **Lowercase the remaining addresses**  
   Convert each kept address to lowercase.

4. **Remove duplicates and sort**  
   After lowercasing, treat two addresses as identical regardless of the original case. Remove any duplicate entries, then sort the unique addresses alphabetically (lexicographically, using the usual order of the lowercased strings).

5. **Produce the final output**  
   Join the sorted addresses with commas and no spaces. If the list is empty, output an empty line (i.e., nothing).

**Examples**

- Input: `mixed Bob@X.com and carol@z.net today`  
  - Candidate addresses: `Bob@X.com`, `carol@z.net`  
  - `Bob@X.com` contains uppercase letters → discard.  
  - `carol@z.net` kept, lowercased → `carol@z.net`.  
  - Result: `carol@z.net`.

- Input: `UPPER ADMIN@SITE.ORG only`  
  - Candidate: `ADMIN@SITE.ORG`. Contains uppercase letters → discard.  
  - No addresses left → empty output.
