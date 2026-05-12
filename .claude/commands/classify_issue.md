# /classify_issue

Classify a GitHub issue as `feature`, `chore`, or `bug`.

## Input

`$ARGUMENTS` contains the issue title + body.

## Heuristics

- **bug**: Describes broken behavior, "doesn't work", error messages, unexpected output.
- **feature**: Describes new user-facing functionality, "add", "implement", "create".
- **chore**: Setup, refactor, dependencies, config, docs, tooling. No user-facing change.

If the issue has labels like `bug`, `feature`, `enhancement`, `chore`, prefer the label.

## Output

Respond with EXACTLY one line, nothing else:

```
CLASSIFICATION: feature|chore|bug
```
