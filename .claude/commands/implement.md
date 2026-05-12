# /implement

Implement a spec produced by `/feature`, `/chore`, or `/bug`.

## Input

`$ARGUMENTS` contains the path to the spec file (e.g. `specs/feat-add-spin-button.md`).

## Your task

1. **Read the spec completely** before writing any code.
2. **Follow the spec literally.** Create/modify exactly the files listed. Do the steps in order.
3. **Match the existing codebase style:**
   - TypeScript strict mode, no `any` unless unavoidable
   - Functional components, hooks
   - Tailwind classes (no inline styles, no separate CSS files)
   - File names: PascalCase for components, kebab-case for routes
4. **Verify your work as you go:**
   - After each file change, re-read the file you just wrote
   - Run `npx tsc --noEmit` after substantial changes to catch type errors
   - Run `npm run lint` if available
5. **Do NOT** commit, push, or open a PR. The ADW script handles git operations.

## Output

After implementing, produce a brief summary in this format:

```
IMPLEMENTATION_SUMMARY:
- Created: <list of new files>
- Modified: <list of changed files>
- Notes: <any deviations from spec, with justification>
```

## Constraints

- If the spec is ambiguous or wrong, fix the smallest thing necessary and note it in `Notes`. Do not redesign the feature.
- If you encounter an error you cannot resolve, stop and report it in `Notes` instead of papering over it.
- Never delete user content or specs.
