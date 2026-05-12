# /feature

Generate a detailed implementation spec for a new feature based on a GitHub issue.

## Input

`$ARGUMENTS` contains the GitHub issue content (title + body + number).

## Your task

1. **Read the issue carefully.** Identify the user-facing goal and any acceptance criteria.
2. **Explore the codebase.** Read `package.json`, `app/page.tsx`, `app/layout.tsx`, and any existing components in `components/` or `app/`. Understand the current architecture before proposing changes.
3. **Identify all files to create or modify.** Be explicit. No vague "update related files".
4. **Generate the spec file** at `specs/feat-<kebab-case-slug>.md`. Use this exact structure:

   ```markdown
   # Feature: <title>

   **Issue**: #<number>
   **Type**: feature

   ## Context
   <2-3 sentences: what is this feature and why>

   ## Files to create
   - `path/to/new/file.tsx` — <what it does>

   ## Files to modify
   - `path/to/existing/file.tsx` — <what changes>

   ## Implementation steps
   1. <granular, ordered step>
   2. ...

   ## Acceptance criteria
   - [ ] <verifiable criterion>
   - [ ] ...

   ## Out of scope
   - <thing we explicitly are NOT doing>
   ```

5. **Final output line.** End your response with EXACTLY this line (nothing after it):

   ```
   SPEC_PATH: specs/feat-<slug>.md
   ```

## Constraints

- The spec will be handed to a separate implementer agent. Be precise — vague specs produce vague code.
- Reference existing code patterns (e.g. "follow the pattern in `components/Button.tsx`").
- Keep specs scoped to the issue. Do not invent unrequested features.
- Use TypeScript and Tailwind conventions consistent with the existing codebase.
