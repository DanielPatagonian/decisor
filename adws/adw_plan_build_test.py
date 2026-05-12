# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""ADW: Composed plan → build → test.

Usage:
    uv run adws/adw_plan_build_test.py <issue_number>

This is just glue: it kicks off the three isolated UV scripts back to back,
passing the ADW_ID along. Importance of standalone scripts is that they can
also be run individually or composed differently.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(cmd: list[str]) -> str:
    print(f"\n$ {' '.join(cmd)}\n")
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    assert proc.stdout is not None
    output = []
    for line in proc.stdout:
        print(line, end="")
        output.append(line)
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"Step failed: {' '.join(cmd)}")
    return "".join(output)


def extract_adw_id(text: str) -> str:
    m = re.search(r"ADW_ID:\s*(\S+)", text)
    if not m:
        raise RuntimeError("could not find ADW_ID in plan output")
    return m.group(1)


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: uv run adws/adw_plan_build_test.py <issue_number>", file=sys.stderr)
        sys.exit(2)
    issue_number = sys.argv[1]

    plan_out = run(["uv", "run", str(HERE / "adw_plan.py"), issue_number])
    adw_id = extract_adw_id(plan_out)
    print(f"\n=== plan done, ADW_ID={adw_id} ===\n")

    run(["uv", "run", str(HERE / "adw_build.py"), adw_id])
    print(f"\n=== build done ===\n")

    run(["uv", "run", str(HERE / "adw_test.py"), adw_id])
    print(f"\n=== test done ===\n")

    print(f"\nADW complete. ADW_ID={adw_id}")


if __name__ == "__main__":
    main()
