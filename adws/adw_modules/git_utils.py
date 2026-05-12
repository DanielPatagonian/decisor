"""Git helpers for ADW scripts."""
from __future__ import annotations

import re
import subprocess


def _run(cmd: list[str], check: bool = True) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\nstderr: {result.stderr}"
        )
    return result.stdout.strip()


def slugify(text: str, max_len: int = 40) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return s[:max_len].rstrip("-")


def branch_name(issue_class: str, issue_number: int, title: str) -> str:
    return f"{issue_class}/{issue_number}-{slugify(title)}"


def current_branch() -> str:
    return _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])


def checkout_new_branch(name: str) -> None:
    _run(["git", "checkout", "-b", name])


def checkout_existing(name: str) -> None:
    _run(["git", "checkout", name])


def has_uncommitted_changes() -> bool:
    out = _run(["git", "status", "--porcelain"])
    return bool(out)


def commit_all(message: str) -> bool:
    """Stage everything and commit. Returns True if a commit was made."""
    _run(["git", "add", "-A"])
    if not has_uncommitted_changes():
        # `git add` may have moved things into index without porcelain changes;
        # re-check via diff-index
        diff = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            capture_output=True, text=True, check=False,
        )
        if diff.returncode == 0:
            return False
    _run(["git", "commit", "-m", message])
    return True


def push(branch: str) -> None:
    _run(["git", "push", "-u", "origin", branch])
