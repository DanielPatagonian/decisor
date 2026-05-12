# /test

Run the test/validation suite for the project and report results in a standardized JSON format.

## Your task

Run these checks in order, capturing pass/fail for each:

1. **TypeScript compilation**
   ```bash
   npx tsc --noEmit
   ```

2. **Lint**
   ```bash
   npm run lint
   ```

3. **Production build**
   ```bash
   npm run build
   ```

For each check:
- If it passes, record `"status": "pass"` and `"output": ""`.
- If it fails, record `"status": "fail"` and `"output": "<first 30 lines of stderr/stdout showing the error>"`.

## Resolution attempt (if any check fails)

If any check fails:
1. Read the error carefully and identify the root cause file.
2. Fix the smallest thing necessary to make the check pass.
3. Re-run the failed check.
4. If it still fails after one fix attempt, leave it as `fail` and move on.

## Output

End your response with EXACTLY this JSON block (no other text after it):

```json
TEST_RESULTS:
{
  "typecheck": {"status": "pass|fail", "output": ""},
  "lint": {"status": "pass|fail", "output": ""},
  "build": {"status": "pass|fail", "output": ""},
  "fixes_applied": ["<short description of any fix>"]
}
```

## Constraints

- Do NOT modify tests/configs to make checks pass. Fix the code.
- Do NOT commit. The ADW script handles git.
