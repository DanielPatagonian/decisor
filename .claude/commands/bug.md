# /bug

Diagnose a bug and generate a fix spec from a GitHub issue.

## Input

`$ARGUMENTS` contains the GitHub issue content (title + body + number).

## Your task

1. **Reproduce the bug mentally** from the issue description. What's the expected vs actual behavior?
2. **Locate the root cause.** Read the relevant files, trace through the logic. Do NOT guess — read the actual code.
3. **Generate the spec file** at `specs/bug-<kebab-case-slug>.md`:

   ```markdown
   # Bug fix: <title>

   **Issue**: #<number>
   **Type**: bug

   ## Symptom
   <what the user sees / experiences>

   ## Root cause
   <the actual cause, with file:line references>

   ## Files to modify
   - `path/to/file.tsx` — <what changes and why>

   ## Fix steps
   1. <granular step>
   2. ...

   ## Verification
   - [ ] <how we know the bug is gone>
   - [ ] <regression check — what else to verify still works>
   ```

4. **Final output line:**

   ```
   SPEC_PATH: specs/bug-<slug>.md
   ```

## Constraints

- The fix should be minimal. Do not refactor unrelated code.
- Always include a regression check in verification.
