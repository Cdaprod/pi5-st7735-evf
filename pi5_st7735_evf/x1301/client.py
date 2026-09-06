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
    def __init__(self, state_file: str = "/run/x1301/state.env",
                 status_command: str = "/usr/local/lib/x1301/runtime-status.sh",
                 diagnostic_command: str = "/usr/local/lib/x1301/hdmi-status.sh",
                 runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> None:
        self.state_file = Path(state_file)
        self.status_command = status_command
        self.diagnostic_command = diagnostic_command
        self._runner = runner

    def read(self) -> X1301State:
        errors: list[str] = []
        try:
            if self.state_file.is_file():
                mapping = parse_env(self.state_file.read_text(encoding="utf-8"))
                if not any(key in mapping for key in
                           ("X1301_SIGNAL_STATE", "SIGNAL_STATE", "signal_state", "STATE", "state")):
                    raise ValueError("state file has no signal state")
                return X1301State.from_mapping(mapping)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"state file: {exc}")

        # The cached runtime command is preferred. The direct query is only a
        # diagnostic fallback and cannot make capture ready by itself because
        # its contract reports configured=false.
        for command in (self.status_command, self.diagnostic_command):
            if not command:
                continue
            try:
                result = self._runner([command, "--json"], capture_output=True, text=True,
                                      check=True, timeout=3)
                payload = json.loads(result.stdout)
                mapping = payload.get("state", payload)
                if not isinstance(mapping, dict) or "signal_state" not in mapping:
                    raise ValueError("JSON has no signal_state")
                return X1301State.from_mapping(mapping)
            except (OSError, subprocess.SubprocessError, json.JSONDecodeError,
                    TypeError, ValueError) as exc:
                errors.append(f"{command}: {exc}")
        return X1301State(signal_state=SignalState.ERROR,
                          error="; ".join(errors) or "X1301 runtime state unavailable")
