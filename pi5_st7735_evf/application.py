from enum import Enum
from .x1301.state import SignalState


class ApplicationState(str, Enum):
    BOOTING = "BOOTING"
    NO_SOURCE = "NO_SOURCE"
    SOURCE_PRESENT = "SOURCE_PRESENT"
    VIDEO_LOCKED = "VIDEO_LOCKED"
    STREAMING = "STREAMING"
    MODE_CHANGE = "MODE_CHANGE"
    CAPTURE_ERROR = "CAPTURE_ERROR"
    ERROR = "ERROR"


def application_state(x1301, streaming: bool = False) -> ApplicationState:
    if x1301.signal_state is SignalState.ERROR: return ApplicationState.ERROR
    if x1301.signal_state is SignalState.DISCONNECTED: return ApplicationState.NO_SOURCE
    if x1301.signal_state is SignalState.MODE_CHANGE: return ApplicationState.MODE_CHANGE
    if x1301.signal_state is SignalState.PRESENT_NO_SIGNAL: return ApplicationState.SOURCE_PRESENT
    if not x1301.ready:
        return ApplicationState.CAPTURE_ERROR
    return ApplicationState.STREAMING if streaming else ApplicationState.CAPTURE_ERROR


def screen_for_state(state: ApplicationState) -> str:
    """Map runtime application state to the approved visual state."""
    return {
        ApplicationState.BOOTING: "boot", ApplicationState.NO_SOURCE: "no-signal",
        ApplicationState.SOURCE_PRESENT: "source-present", ApplicationState.VIDEO_LOCKED: "mode-change",
        ApplicationState.STREAMING: "live", ApplicationState.MODE_CHANGE: "mode-change",
        ApplicationState.CAPTURE_ERROR: "capture-error", ApplicationState.ERROR: "capture-error",
    }[state]
