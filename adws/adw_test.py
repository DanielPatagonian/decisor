# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""ADW: Test step.

Usage:
    uv run adws/adw_test.py <adw_id>

What it does:
1. Load state.
2. Make sure we're on the branch.
3. Run /test (typecheck + lint + build, fixing issues if possible).
4. Commit any fixes and push.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from adw_modules import agent, git_utils, state  # noqa: E402


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: uv run adws/adw_test.py <adw_id>", file=sys.stderr)
        sys.exit(2)

    adw_id = sys.argv[1]
    st = state.load(adw_id)
    st.log("adw_test started")

    if not st.branch:
        raise RuntimeError("state missing branch; run adw_plan first")

    if git_utils.current_branch() != st.branch:
        git_utils.checkout_existing(st.branch)

    result = agent.run_claude(
        prompt=agent.slash("test"),
        log_path=st.logs_dir / "04-test.log",
    )
    if result["returncode"] != 0:
        st.log("test agent exited non-zero (see log)")

    commit_msg = (
        f"test: validation for #{st.issue_number}\n\n"
        f"ADW_ID: {st.adw_id}\n\n"
        f"🤖 Generated with Claude Code\n"
        f"Co-Authored-By: Claude <noreply@anthropic.com>"
    )
    if git_utils.commit_all(commit_msg):
        st.log("committed test fixes")
        git_utils.push(st.branch)
    else:
        st.log("no test fixes to commit")

    print()
    print(f"ADW_ID: {st.adw_id}")


if __name__ == "__main__":
    main()
