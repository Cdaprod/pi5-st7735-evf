"""Configurable raw-input to semantic-action mapping."""
from __future__ import annotations

from collections.abc import Mapping
from .actions import UIAction
from .events import InputEvent

DEFAULT_MAPPING = {
    InputEvent.BUTTON_F1: UIAction.TOGGLE_FOCUS_ASSIST,
    InputEvent.BUTTON_F2: UIAction.TOGGLE_ZEBRA,
    InputEvent.BUTTON_F3: UIAction.TOGGLE_CROSSHAIR,
    InputEvent.BUTTON_F4: UIAction.TOGGLE_HISTOGRAM,
    InputEvent.BUTTON_MENU: UIAction.MENU,
    InputEvent.ENCODER_LEFT: UIAction.PREVIOUS,
    InputEvent.ENCODER_RIGHT: UIAction.NEXT,
    InputEvent.ENCODER_PRESS: UIAction.SELECT,
    InputEvent.ENCODER_LONG_PRESS: UIAction.BACK,
}


class InputMapper:
    def __init__(self, mapping: Mapping[InputEvent, UIAction] | None = None) -> None:
        self.mapping = dict(DEFAULT_MAPPING if mapping is None else mapping)

    def map(self, event: InputEvent) -> UIAction | None:
        return self.mapping.get(event)
