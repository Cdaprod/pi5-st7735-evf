"""Persistent UI state and the single semantic action dispatcher."""
from __future__ import annotations

from dataclasses import dataclass
from .input.actions import UIAction

MENU_ITEMS = ("Focus Assist", "Focus Settings", "Zebra", "Crosshair",
              "Histogram", "System Info", "Return to Live", "Shutdown")
RUNTIME_SCREENS = {"live", "no-signal", "source-present", "capture-error", "mode-change"}


@dataclass
class NavigationState:
    current_screen: str = "boot"
    previous_screen: str = "no-signal"
    menu_index: int = 0
    focus_assist_enabled: bool = False
    zebra_enabled: bool = False
    crosshair_enabled: bool = False
    histogram_enabled: bool = False
    source_connected: bool = False
    streaming: bool = False
    focus_threshold: int = 90
    shutdown_confirming: bool = False
    shutdown_requested: bool = False

    def set_runtime_screen(self, screen: str, *, connected: bool, streaming: bool) -> None:
        self.source_connected, self.streaming = connected, streaming
        if self.current_screen in RUNTIME_SCREENS or self.current_screen == "boot":
            self.current_screen = screen
        elif self.current_screen in ("menu", "focus-settings", "system-info", "shutdown"):
            self.previous_screen = screen

    def dispatch(self, action: UIAction) -> None:
        if action is UIAction.MENU:
            if self.current_screen == "menu":
                self.current_screen = self.previous_screen
            else:
                if self.current_screen in RUNTIME_SCREENS:
                    self.previous_screen = self.current_screen
                self.current_screen = "menu"
            return
        toggles = {UIAction.TOGGLE_FOCUS_ASSIST: "focus_assist_enabled",
                   UIAction.TOGGLE_ZEBRA: "zebra_enabled",
                   UIAction.TOGGLE_CROSSHAIR: "crosshair_enabled",
                   UIAction.TOGGLE_HISTOGRAM: "histogram_enabled"}
        if action in toggles:
            name = toggles[action]
            setattr(self, name, not getattr(self, name))
            return
        if self.current_screen == "menu":
            if action is UIAction.BACK:
                self.current_screen = self.previous_screen
            elif action in (UIAction.PREVIOUS, UIAction.LEFT):
                self.menu_index = (self.menu_index - 1) % len(MENU_ITEMS)
            elif action in (UIAction.NEXT, UIAction.RIGHT):
                self.menu_index = (self.menu_index + 1) % len(MENU_ITEMS)
            elif action in (UIAction.SELECT, UIAction.PRIMARY):
                self._activate_menu_item()
        elif self.current_screen == "focus-settings":
            if action is UIAction.BACK:
                self.current_screen = "menu"
            elif action in (UIAction.INCREASE, UIAction.NEXT, UIAction.RIGHT):
                self.focus_threshold = min(255, self.focus_threshold + 5)
            elif action in (UIAction.DECREASE, UIAction.PREVIOUS, UIAction.LEFT):
                self.focus_threshold = max(0, self.focus_threshold - 5)
        elif self.current_screen in ("system-info", "shutdown") and action is UIAction.BACK:
            self.shutdown_confirming = False
            self.current_screen = "menu"
        elif self.current_screen == "shutdown" and action in (UIAction.SELECT, UIAction.PRIMARY):
            self.shutdown_requested = True

    def _activate_menu_item(self) -> None:
        item = MENU_ITEMS[self.menu_index]
        if item == "Focus Assist": self.focus_assist_enabled = not self.focus_assist_enabled
        elif item == "Focus Settings": self.current_screen = "focus-settings"
        elif item == "Zebra": self.zebra_enabled = not self.zebra_enabled
        elif item == "Crosshair": self.crosshair_enabled = not self.crosshair_enabled
        elif item == "Histogram": self.histogram_enabled = not self.histogram_enabled
        elif item == "System Info": self.current_screen = "system-info"
        elif item == "Return to Live": self.current_screen = self.previous_screen
        elif item == "Shutdown":
            self.shutdown_confirming = True
            self.current_screen = "shutdown"
