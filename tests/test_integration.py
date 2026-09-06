import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from pi5_st7735_evf.application import ApplicationState, application_state, screen_for_state
from pi5_st7735_evf.capture import CaptureController
from pi5_st7735_evf.display import MockDisplayBackend
from pi5_st7735_evf.input.controller import InputController
from pi5_st7735_evf.input.events import InputEvent
from pi5_st7735_evf.ui.menu import Action, Menu
from pi5_st7735_evf.ui.status import no_signal_screen
from pi5_st7735_evf.ui.screens import MENU_ITEMS, SCREEN_NAMES, render_screen
from pi5_st7735_evf.x1301.client import X1301Client, parse_env
from pi5_st7735_evf.x1301.state import SignalState, X1301State


class FakeCapture:
    instances = []
    fail_read = False
    def __init__(self, *args): self.closed = False; self.args = args; self.instances.append(self)
    def open(self): pass
    def close(self): self.closed = True
    def read(self): return (False, None) if self.fail_read else (True, object())


def state(signal=SignalState.LOCKED, width=1920):
    return X1301State(signal, "/dev/test-video", "/dev/test-media", "/dev/test-subdev",
                      width, 1080, 30, signal is SignalState.LOCKED)


class IntegrationTests(unittest.TestCase):
    def setUp(self): FakeCapture.instances = []; FakeCapture.fail_read = False

    def test_env_parsing_and_state_file(self):
        parsed = parse_env('SIGNAL_STATE="LOCKED"\nVIDEO_NODE=/dev/video9 # comment\nWIDTH=1280\nHEIGHT=720\nFPS=30000/1001\nCONFIGURED=1\n')
        self.assertEqual(parsed["VIDEO_NODE"], "/dev/video9")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.env"; path.write_text("\n".join(f"{k}={v}" for k, v in parsed.items()))
            current = X1301Client(str(path)).read()
        self.assertTrue(current.ready); self.assertAlmostEqual(current.fps, 29.97, places=2)

    def test_json_fallback(self):
        payload = {"signal_state": "locked", "video_node": "/dev/dynamic", "configured": True}
        runner = lambda *a, **k: subprocess.CompletedProcess(a, 0, json.dumps(payload), "")
        current = X1301Client("/missing", runner=runner).read()
        self.assertEqual(current.video_node, "/dev/dynamic")

    def test_application_and_no_signal(self):
        self.assertEqual(application_state(state(SignalState.DISCONNECTED)), ApplicationState.NO_SOURCE)
        self.assertEqual(application_state(state(SignalState.PRESENT_NO_SIGNAL)), ApplicationState.SOURCE_PRESENT)
        self.assertEqual(no_signal_screen(128, 128).size, (128, 128))
        self.assertEqual(application_state(state(SignalState.MODE_CHANGE)), ApplicationState.MODE_CHANGE)
        self.assertEqual(screen_for_state(ApplicationState.VIDEO_LOCKED), "mode-change")

    def test_every_approved_screen_renders_at_native_size(self):
        for name in SCREEN_NAMES:
            with self.subTest(screen=name):
                image = render_screen(name)
                self.assertEqual(image.size, (128, 128))
                self.assertEqual(image.mode, "RGB")

    def test_menu_selection_is_clamped_and_focus_preview_updates(self):
        self.assertEqual(render_screen("menu", selected=-50).size, (128, 128))
        self.assertEqual(render_screen("menu", selected=len(MENU_ITEMS)+50).size, (128, 128))
        low = render_screen("focus-settings", threshold=2, thickness=1)
        high = render_screen("focus-settings", threshold=9, thickness=3)
        self.assertNotEqual(low.tobytes(), high.tobytes())

    def test_capture_open_mode_change_reopen_and_failure(self):
        controller = CaptureController(factory=FakeCapture)
        self.assertTrue(controller.sync(state()))
        first = FakeCapture.instances[-1]
        self.assertFalse(controller.sync(state(SignalState.MODE_CHANGE)))
        self.assertTrue(first.closed)
        self.assertTrue(controller.sync(state(width=1280)))
        FakeCapture.fail_read = True
        self.assertEqual(controller.read(), (False, None)); self.assertFalse(controller.streaming)

    def test_display_input_and_menu(self):
        display = MockDisplayBackend(); display.open(); display.show(Image.new("RGB", (128, 128)))
        self.assertIsNotNone(display.last_frame)
        seen = []; controller = InputController(); controller.subscribe(seen.append)
        controller.dispatch(InputEvent.BUTTON_F1); self.assertEqual(seen, [InputEvent.BUTTON_F1])
        menu = Menu(("one", "two")); menu.dispatch(Action.MENU); menu.dispatch(Action.DOWN)
        self.assertEqual(menu.dispatch(Action.SELECT), "two")


if __name__ == "__main__": unittest.main()
