"""Read the loosely-coupled X1301 runtime contract."""
from __future__ import annotations

import json
from pathlib import Path
import shlex
import subprocess
from typing import Callable

from .state import SignalState, X1301State


def parse_env(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        parts = shlex.split(value, comments=True)
        values[key.strip()] = parts[0] if parts else ""
    return values


class X1301Client:
    def __init__(self, state_file: str = "/run/x1301/state.env", status_command: str = "hdmi-status.sh",
                 runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> None:
        self.state_file = Path(state_file)
        self.status_command = status_command
        self._runner = runner

    def read(self) -> X1301State:
        try:
            if self.state_file.is_file():
                return X1301State.from_mapping(parse_env(self.state_file.read_text(encoding="utf-8")))
            result = self._runner([self.status_command, "--json"], capture_output=True, text=True,
                                  check=True, timeout=3)
            payload = json.loads(result.stdout)
            return X1301State.from_mapping(payload.get("state", payload))
        except Exception as exc:
            return X1301State(signal_state=SignalState.ERROR, error=str(exc))
