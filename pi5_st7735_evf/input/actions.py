"""Hardware-independent actions understood by EVF navigation."""
from enum import Enum


class UIAction(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    MENU = "MENU"
    BACK = "BACK"
    SELECT = "SELECT"
    PREVIOUS = "PREVIOUS"
    NEXT = "NEXT"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    INCREASE = "INCREASE"
    DECREASE = "DECREASE"
    TOGGLE_FOCUS_ASSIST = "TOGGLE_FOCUS_ASSIST"
    TOGGLE_ZEBRA = "TOGGLE_ZEBRA"
    TOGGLE_CROSSHAIR = "TOGGLE_CROSSHAIR"
    TOGGLE_HISTOGRAM = "TOGGLE_HISTOGRAM"
