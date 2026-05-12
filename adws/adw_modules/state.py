"""ADW state management.

Each AI Developer Workflow run gets a unique ADW_ID. The state for that run
lives in ``agents/<adw_id>/state.json`` and is read/written by the workflow
scripts as they hand off between plan / build / test.
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
AGENTS_DIR = REPO_ROOT / "agents"


@dataclass
class AdwState:
    adw_id: str
    issue_number: int
    issue_class: Optional[str] = None  # feature | chore | bug
    branch: Optional[str] = None
    spec_path: Optional[str] = None
    pr_url: Optional[str] = None
    history: list[str] = field(default_factory=list)

    @property
    def dir(self) -> Path:
        return AGENTS_DIR / self.adw_id

    @property
    def state_file(self) -> Path:
        return self.dir / "state.json"

    @property
    def logs_dir(self) -> Path:
        return self.dir / "logs"

    def save(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(asdict(self), indent=2))

    def log(self, message: str) -> None:
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"[{stamp}] {message}")
        self.save()
        print(f"[ADW {self.adw_id}] {message}")


def new_adw_id() -> str:
    """Short, sortable-ish, unique ID."""
    return f"{int(time.time())}-{uuid.uuid4().hex[:6]}"


def load(adw_id: str) -> AdwState:
    path = AGENTS_DIR / adw_id / "state.json"
    if not path.exists():
        raise FileNotFoundError(f"No state file for ADW_ID={adw_id} at {path}")
    raw = json.loads(path.read_text())
    return AdwState(**raw)


def create(issue_number: int) -> AdwState:
    state = AdwState(adw_id=new_adw_id(), issue_number=issue_number)
    state.save()
    return state
