# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""ADW: Plan step.

Usage:
    uv run adws/adw_plan.py <issue_number> [adw_id]

What it does:
1. Fetch the GitHub issue (uses `gh`).
2. Ask Claude to classify it as feature / chore / bug.
3. Create a new branch.
4. Run the matching slash command (/feature, /chore, /bug) to generate a spec.
5. Commit the spec on the branch and push.
6. Print the ADW_ID (use it to chain into adw_build.py).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# allow importing adw_modules when run as a script
sys.path.insert(0, str(Path(__file__).resolve().parent))

from adw_modules import agent, git_utils, github_utils, state  # noqa: E402


VALID_CLASSES = {"feature", "chore", "bug"}


def parse_classification(output: str) -> str:
    m = re.search(r"CLASSIFICATION:\s*(feature|chore|bug)", output)
    if not m:
        raise RuntimeError(f"Could not parse classification from agent output:\n{output[-500:]}")
    return m.group(1)


def parse_spec_path(output: str) -> str:
    m = re.search(r"SPEC_PATH:\s*(\S+\.md)", output)
    if not m:
        raise RuntimeError(f"Could not parse SPEC_PATH from agent output:\n{output[-500:]}")
    return m.group(1)


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: uv run adws/adw_plan.py <issue_number> [adw_id]", file=sys.stderr)
        sys.exit(2)

    issue_number = int(sys.argv[1])
    adw_id_arg = sys.argv[2] if len(sys.argv) > 2 else None

    if adw_id_arg:
        st = state.load(adw_id_arg)
    else:
        st = state.create(issue_number)
    st.log(f"adw_plan started for issue #{issue_number}")

    # 1. fetch the issue
    issue = github_utils.get_issue(issue_number)
    issue_text = github_utils.issue_to_prompt_text(issue)
    st.log(f"fetched issue: {issue['title']}")

    # 2. classify
    classification_output = agent.run_claude(
        prompt=agent.slash("classify_issue", issue_text),
        log_path=st.logs_dir / "01-classify.log",
    )
    if classification_output["returncode"] != 0:
        raise RuntimeError("classify_issue agent failed")
    issue_class = parse_classification(classification_output["output"])
    if issue_class not in VALID_CLASSES:
        raise RuntimeError(f"Unexpected class: {issue_class}")
    st.issue_class = issue_class
    st.save()
    st.log(f"classified as: {issue_class}")

    # 3. create branch
    branch = git_utils.branch_name(issue_class, issue_number, issue["title"])
    git_utils.checkout_new_branch(branch)
    st.branch = branch
    st.save()
    st.log(f"created branch: {branch}")

    # 4. plan: run the matching slash command
    plan_output = agent.run_claude(
        prompt=agent.slash(issue_class, issue_text),
        log_path=st.logs_dir / "02-plan.log",
    )
    if plan_output["returncode"] != 0:
        raise RuntimeError(f"/{issue_class} agent failed")
    spec_path = parse_spec_path(plan_output["output"])
    if not Path(spec_path).exists():
        raise RuntimeError(f"Spec file does not exist: {spec_path}")
    st.spec_path = spec_path
    st.save()
    st.log(f"spec generated: {spec_path}")

    # 5. commit spec
    commit_msg = (
        f"plan: spec for #{issue_number} {issue['title']}\n\n"
        f"ADW_ID: {st.adw_id}\n"
        f"Issue: {issue['url']}\n\n"
        f"🤖 Generated with Claude Code\n"
        f"Co-Authored-By: Claude <noreply@anthropic.com>"
    )
    if git_utils.commit_all(commit_msg):
        st.log("committed spec")
        git_utils.push(branch)
        st.log(f"pushed branch {branch}")
    else:
        st.log("nothing to commit (spec already in tree?)")

    # 6. final line: emit ADW_ID for chaining
    print()
    print(f"ADW_ID: {st.adw_id}")


if __name__ == "__main__":
    main()
