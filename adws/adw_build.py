# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""ADW: Build step.

Usage:
    uv run adws/adw_build.py <adw_id>

What it does:
1. Load state for the ADW_ID (set up by adw_plan.py).
2. Make sure we're on the branch.
3. Run /implement with the spec path.
4. Commit any changes and push.
5. Create or update the PR.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from adw_modules import agent, git_utils, github_utils, state  # noqa: E402


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: uv run adws/adw_build.py <adw_id>", file=sys.stderr)
        sys.exit(2)

    adw_id = sys.argv[1]
    st = state.load(adw_id)
    st.log("adw_build started")

    if not st.branch or not st.spec_path:
        raise RuntimeError("state is missing branch or spec_path; run adw_plan first")

    # 1. checkout branch (may already be on it)
    if git_utils.current_branch() != st.branch:
        git_utils.checkout_existing(st.branch)
    st.log(f"on branch {st.branch}")

    # 2. /implement
    impl = agent.run_claude(
        prompt=agent.slash("implement", st.spec_path),
        log_path=st.logs_dir / "03-implement.log",
        model="sonnet",
    )
    if impl["returncode"] != 0:
        raise RuntimeError("/implement agent failed")
    st.log("implementation complete")

    # 3. commit + push
    issue = github_utils.get_issue(st.issue_number)
    commit_msg = (
        f"{st.issue_class}: implement #{st.issue_number} {issue['title']}\n\n"
        f"ADW_ID: {st.adw_id}\n"
        f"Spec: {st.spec_path}\n"
        f"Issue: {issue['url']}\n\n"
        f"🤖 Generated with Claude Code\n"
        f"Co-Authored-By: Claude <noreply@anthropic.com>"
    )
    if git_utils.commit_all(commit_msg):
        st.log("committed implementation")
    else:
        st.log("no implementation changes to commit")
    git_utils.push(st.branch)
    st.log("pushed branch")

    # 4. PR
    pr_body = (
        f"Closes #{st.issue_number}\n\n"
        f"**ADW_ID**: `{st.adw_id}`\n"
        f"**Spec**: `{st.spec_path}`\n"
        f"**Class**: `{st.issue_class}`\n\n"
        f"This PR was authored by an AI Developer Workflow (plan → build → test).\n"
        f"See `adws/` for the orchestration scripts and `.claude/commands/` for the agent prompts.\n\n"
        f"---\n"
        f"🤖 Generated with Claude Code"
    )
    pr_url = github_utils.create_or_update_pr(
        branch=st.branch,
        title=f"{st.issue_class}: {issue['title']} (#{st.issue_number})",
        body=pr_body,
    )
    st.pr_url = pr_url
    st.save()
    st.log(f"PR ready: {pr_url}")

    print()
    print(f"ADW_ID: {st.adw_id}")
    print(f"PR_URL: {pr_url}")


if __name__ == "__main__":
    main()
