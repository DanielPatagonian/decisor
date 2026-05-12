#!/usr/bin/env bash
# Create the 5 Decisor issues on GitHub.
# Run from the repo root after `gh auth login` and after the repo has a remote
# pointing at the GitHub repo.
#
#   bash scripts/create-issues.sh
#
set -euo pipefail

cd "$(dirname "$0")/.."

create_issue() {
    local title="$1"
    local file="$2"
    local label="$3"
    echo "Creating: $title"
    gh issue create \
        --title "$title" \
        --body-file "$file" \
        --label "$label" 2>/dev/null || \
    gh issue create \
        --title "$title" \
        --body-file "$file"
}

# If labels don't exist yet, create them (ignore errors if they already do).
gh label create chore --color "ededed" --description "Setup, refactor, tooling" 2>/dev/null || true
gh label create feature --color "0e8a16" --description "New user-facing functionality" 2>/dev/null || true
gh label create bug --color "d73a4a" --description "Something is broken" 2>/dev/null || true

create_issue "chore: replace boilerplate with Decisor landing"  issues/01-chore-landing.md      chore
create_issue "feat: add and list options"                       issues/02-feat-options-list.md  feature
create_issue "feat: Decidir button with spin animation"         issues/03-feat-spin.md          feature
create_issue "feat: persist options in localStorage"            issues/04-feat-persistence.md   feature
create_issue "feat: dark mode toggle"                           issues/05-feat-dark-mode.md     feature

echo
echo "Done. List them with:"
echo "  gh issue list"
