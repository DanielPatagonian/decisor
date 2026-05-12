# /chore

Generate a spec for a chore: setup, refactor, cleanup, config, or non-feature work.

## Input

`$ARGUMENTS` contains the GitHub issue content (title + body + number).

## Your task

1. **Understand the chore.** Chores include: dependency updates, file reorganization, config changes, build setup, dev-experience improvements, README/docs.
2. **Explore the codebase** to understand what's there and what needs to change.
3. **Generate the spec file** at `specs/chore-<kebab-case-slug>.md`:

   ```markdown
   # Chore: <title>

   **Issue**: #<number>
   **Type**: chore

   ## Context
   <why this chore is needed>

   ## Files to create / modify / delete
   - `path/to/file` — <action and reason>

   ## Steps
   1. <granular step>
   2. ...

   ## Verification
   - [ ] <how we confirm the chore is done>
   ```

4. **Final output line:**

   ```
   SPEC_PATH: specs/chore-<slug>.md
   ```

## Constraints

- Chores should NOT change user-facing behavior. If they would, this should be a feature instead.
- Keep diffs minimal.
