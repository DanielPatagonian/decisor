"""Wrapper around `claude -p` (programmable mode)."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional


def run_claude(
    prompt: str,
    log_path: Path,
    model: str = "sonnet",
    cwd: Optional[Path] = None,
) -> dict:
    """Run `claude -p` with the given prompt.

    Streams stdout to ``log_path`` and returns a dict with ``returncode`` and
    the combined ``output`` text. Uses ``--dangerously-skip-permissions`` so
    the agent can edit files and run commands without prompting (yolo mode).
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "claude",
        "-p", prompt,
        "--model", model,
        "--dangerously-skip-permissions",
    ]

    output_chunks: list[str] = []
    with log_path.open("w", encoding="utf-8") as log:
        log.write(f"=== prompt ===\n{prompt}\n\n=== output ===\n")
        log.flush()

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=str(cwd) if cwd else None,
            bufsize=1,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            log.write(line)
            log.flush()
            output_chunks.append(line)
            # echo to console so the human can follow along
            print(line, end="")
        proc.wait()

    return {
        "returncode": proc.returncode,
        "output": "".join(output_chunks),
    }


def slash(command: str, arguments: str = "") -> str:
    """Build a slash-command prompt string.

    Example: ``slash("feature", issue_text)`` -> ``"/feature <issue_text>"``.
    """
    if arguments:
        return f"/{command} {arguments}"
    return f"/{command}"
