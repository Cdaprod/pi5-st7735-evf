from collections import deque
from collections.abc import Callable
from .events import InputEvent


class InputController:
    def __init__(self) -> None: self._handlers: list[Callable[[InputEvent], None]] = []
    def subscribe(self, handler: Callable[[InputEvent], None]) -> None: self._handlers.append(handler)
    def dispatch(self, event: InputEvent) -> None:
        for handler in tuple(self._handlers): handler(event)


class MockInputBackend:
    def __init__(self, events=()) -> None: self.events = deque(events)
    def poll(self) -> InputEvent | None: return self.events.popleft() if self.events else None
