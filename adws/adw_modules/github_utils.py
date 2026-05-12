"""Wrappers around the GitHub CLI (`gh`)."""
from __future__ import annotations

import json
import subprocess


def _run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\nstderr: {result.stderr}"
        )
    return result.stdout


def get_issue(issue_number: int) -> dict:
    """Return the issue as a dict with title, body, number, labels, url."""
    raw = _run([
        "gh", "issue", "view", str(issue_number),
        "--json", "number,title,body,labels,url",
    ])
    return json.loads(raw)


def issue_to_prompt_text(issue: dict) -> str:
    """Format an issue dict as a text block for an agent prompt."""
    labels = ", ".join(l["name"] for l in issue.get("labels", []))
    return (
        f"Issue #{issue['number']}: {issue['title']}\n"
        f"Labels: {labels or '(none)'}\n"
        f"URL: {issue['url']}\n\n"
        f"Body:\n{issue.get('body') or '(empty)'}"
    )


def create_or_update_pr(branch: str, title: str, body: str) -> str:
    """Create a PR if one doesn't exist for the branch, else update it.

    Returns the PR URL.
    """
    # check if PR exists
    existing = subprocess.run(
        [
            "gh", "pr", "list",
            "--head", branch,
            "--json", "url,number",
            "--state", "open",
        ],
        capture_output=True, text=True, check=False,
    )
    existing_prs = json.loads(existing.stdout or "[]") if existing.returncode == 0 else []

    if existing_prs:
        pr_url = existing_prs[0]["url"]
        _run(["gh", "pr", "edit", pr_url, "--title", title, "--body", body])
        return pr_url

    out = _run([
        "gh", "pr", "create",
        "--head", branch,
        "--title", title,
        "--body", body,
    ])
    return out.strip().splitlines()[-1]


def comment_on_issue(issue_number: int, body: str) -> None:
    _run(["gh", "issue", "comment", str(issue_number), "--body", body])
