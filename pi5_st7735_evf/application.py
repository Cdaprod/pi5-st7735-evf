from enum import Enum
from .x1301.state import SignalState


class ApplicationState(str, Enum):
    BOOTING = "BOOTING"
    NO_SOURCE = "NO_SOURCE"
    SOURCE_PRESENT = "SOURCE_PRESENT"
    VIDEO_LOCKED = "VIDEO_LOCKED"
    STREAMING = "STREAMING"
    ERROR = "ERROR"


def application_state(x1301, streaming: bool = False) -> ApplicationState:
    if x1301.signal_state is SignalState.ERROR: return ApplicationState.ERROR
    if x1301.signal_state is SignalState.DISCONNECTED: return ApplicationState.NO_SOURCE
    if x1301.signal_state in (SignalState.PRESENT_NO_SIGNAL, SignalState.MODE_CHANGE): return ApplicationState.SOURCE_PRESENT
    return ApplicationState.STREAMING if streaming else ApplicationState.VIDEO_LOCKED
