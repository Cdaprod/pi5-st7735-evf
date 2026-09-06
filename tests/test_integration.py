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


FIXTURES = Path(__file__).parent / "fixtures"


class FakeClock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class FakeCapture:
    instances = []
    open_failures = 0
    fail_read = False

    def __init__(self, *args):
        self.closed = False
        self.args = args
        self.instances.append(self)

    def open(self):
        if self.open_failures:
            type(self).open_failures -= 1
            raise RuntimeError("test open failure")

    def close(self):
        self.closed = True

    def read(self):
        return (False, None) if self.fail_read else (True, object())


def state(signal=SignalState.LOCKED, *, video="/dev/video0", width=1920, height=1080,
          fps=60, configured=None, pixel_format="RGB3", mode_id=None, generation=1):
    if configured is None:
        configured = signal is SignalState.LOCKED
    if mode_id is None and signal is SignalState.LOCKED:
        mode_id = f"{width}x{height}@{fps}/148500000Hz/{pixel_format}"
    return X1301State(signal_state=signal, video_node=video, media_node="/dev/media0",
                      subdev_node="/dev/v4l-subdev0", width=width, height=height,
                      fps=fps, configured=configured, power_present=True,
                      timings_locked=signal in (SignalState.LOCKED, SignalState.MODE_CHANGE),
                      pixel_clock_hz=148_500_000, pixel_format=pixel_format,
                      mode_id=mode_id, mode_generation=generation)


class X1301ParsingTests(unittest.TestCase):
    def test_canonical_prefixed_state_file_and_typed_fields(self):
        current = X1301Client(str(FIXTURES / "locked-1080p60.env"),
                              status_command="", diagnostic_command="").read()
        self.assertTrue(current.ready)
        self.assertEqual(current.video_node, "/dev/video14")
        self.assertEqual(current.pixel_clock_hz, 148_500_000)
        self.assertEqual(current.pixel_clock_mhz, 148.5)
        self.assertEqual(current.pixel_format, "RGB3")
        self.assertEqual(current.mode_generation, 7)
        self.assertTrue(current.power_present)
        self.assertTrue(current.timings_locked)
        self.assertTrue(current.audio_present)
        self.assertEqual(current.audio_sampling_rate, 48000)
        self.assertEqual(current.driver, "rp1-cfe")
        self.assertTrue(current.rp1_cfe_detected)
        self.assertEqual(current.last_change, "2026-09-06T12:00:00+00:00")

    def test_legacy_unprefixed_and_aliases_remain_compatible(self):
        parsed = parse_env('SIGNAL_STATE="LOCKED"\nVIDEO_NODE=/dev/video9 # comment\nMEDIA_NODE=/dev/media2\nSUBDEV_NODE=/dev/v4l-subdev3\nWIDTH=1280\nHEIGHT=720\nFPS=30000/1001\nCONFIGURED=1\nPIXEL_CLOCK_MHZ=74.25\n')
        current = X1301State.from_mapping(parsed)
        self.assertTrue(current.ready)
        self.assertAlmostEqual(current.fps, 29.97, places=2)
        self.assertEqual(current.pixel_clock_hz, 74_250_000)
        self.assertEqual(current.media_node, "/dev/media2")

    def test_lower_case_runtime_json_and_unknown_fields(self):
        payload = {"X1301_STATUS_SCHEMA": 1, "signal_state": "locked",
                   "video": "/dev/dynamic", "media": "/dev/media4",
                   "subdev": "/dev/v4l-subdev4", "configured": True,
                   "pixelclock_hz": 74250000, "pixelformat": "RGB3",
                   "mode_generation": 12, "future_addition": {"ignored": True}}
        runner = lambda *a, **k: subprocess.CompletedProcess(a, 0, json.dumps(payload), "")
        current = X1301Client("/missing", runner=runner).read()
        self.assertEqual(current.video_node, "/dev/dynamic")
        self.assertEqual(current.pixel_clock_mhz, 74.25)
        self.assertEqual(current.mode_generation, 12)

    def test_direct_diagnostic_lock_is_not_capture_ready(self):
        calls = []

        def runner(args, **_):
            calls.append(args[0])
            if "runtime-status" in args[0]:
                raise subprocess.CalledProcessError(2, args)
            payload = {"X1301_STATUS_SCHEMA": 1, "signal_state": "LOCKED",
                       "video": "/dev/video2", "configured": False,
                       "timings_locked": True}
            return subprocess.CompletedProcess(args, 0, json.dumps(payload), "")

        current = X1301Client("/missing", runner=runner).read()
        self.assertEqual(calls, ["/usr/local/lib/x1301/runtime-status.sh",
                                 "/usr/local/lib/x1301/hdmi-status.sh"])
        self.assertTrue(current.timings_locked)
        self.assertFalse(current.ready)

    def test_missing_and_temporarily_malformed_state_are_safe(self):
        calls = []

        def failing_runner(args, **_):
            calls.append(args[0])
            raise FileNotFoundError(args[0])

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.env"
            client = X1301Client(str(path), runner=failing_runner)
            self.assertEqual(client.read().signal_state, SignalState.ERROR)
            path.write_text("this is not an environment file\n")
            self.assertEqual(client.read().signal_state, SignalState.ERROR)
            path.write_text((FIXTURES / "disconnected.env").read_text())
            self.assertEqual(client.read().signal_state, SignalState.DISCONNECTED)
        self.assertIn("/usr/local/lib/x1301/runtime-status.sh", calls)
        self.assertIn("/usr/local/lib/x1301/hdmi-status.sh", calls)


class CaptureLifecycleTests(unittest.TestCase):
    def setUp(self):
        FakeCapture.instances = []
        FakeCapture.open_failures = 0
        FakeCapture.fail_read = False
        self.clock = FakeClock()
        self.controller = CaptureController(factory=FakeCapture, reconnect_delay=1.0,
                                            clock=self.clock)

    def test_start_disconnected_then_full_lock_sequence(self):
        for signal in (SignalState.DISCONNECTED, SignalState.PRESENT_NO_SIGNAL,
                       SignalState.MODE_CHANGE):
            self.assertFalse(self.controller.sync(state(signal, configured=False)))
        self.assertEqual(FakeCapture.instances, [])
        self.assertTrue(self.controller.sync(state()))

    def test_timing_and_resolution_changes_reopen_same_node(self):
        self.assertTrue(self.controller.sync(state(fps=60, generation=1)))
        first = FakeCapture.instances[-1]
        self.assertTrue(self.controller.sync(state(fps=30, generation=2)))
        self.assertTrue(first.closed)
        second = FakeCapture.instances[-1]
        self.assertTrue(self.controller.sync(state(width=1280, height=720, generation=3)))
        self.assertTrue(second.closed)

    def test_disconnect_reconnect_and_changed_video_node(self):
        self.assertTrue(self.controller.sync(state()))
        first = FakeCapture.instances[-1]
        self.assertFalse(self.controller.sync(state(SignalState.DISCONNECTED, configured=False)))
        self.assertTrue(first.closed)
        self.assertTrue(self.controller.sync(state(video="/dev/video8", generation=2)))
        self.assertEqual(FakeCapture.instances[-1].args[0], "/dev/video8")

    def test_mode_generation_change_reopens_unchanged_node(self):
        self.assertTrue(self.controller.sync(state(generation=4)))
        first = FakeCapture.instances[-1]
        self.assertTrue(self.controller.sync(state(generation=5)))
        self.assertTrue(first.closed)

    def test_mode_id_and_pixel_format_changes_reopen(self):
        original = state(generation=4)
        self.assertTrue(self.controller.sync(original))
        first = FakeCapture.instances[-1]
        changed_id = state(generation=4, mode_id="replacement-mode-id")
        self.assertTrue(self.controller.sync(changed_id))
        self.assertTrue(first.closed)
        second = FakeCapture.instances[-1]
        changed_format = state(generation=4, mode_id="replacement-mode-id",
                               pixel_format="BGR3")
        self.assertTrue(self.controller.sync(changed_format))
        self.assertTrue(second.closed)

    def test_unconfigured_or_non_ready_state_closes_immediately(self):
        for signal in (SignalState.PRESENT_NO_SIGNAL, SignalState.MODE_CHANGE,
                       SignalState.ERROR):
            self.assertTrue(self.controller.sync(state()))
            active = FakeCapture.instances[-1]
            self.assertFalse(self.controller.sync(state(signal, configured=False)))
            self.assertTrue(active.closed)
        self.assertTrue(self.controller.sync(state()))
        active = FakeCapture.instances[-1]
        self.assertFalse(self.controller.sync(state(configured=False)))
        self.assertTrue(active.closed)

    def test_capture_open_failure_retries_without_blocking(self):
        FakeCapture.open_failures = 1
        self.assertFalse(self.controller.sync(state()))
        self.assertFalse(self.controller.sync(state()))
        self.assertEqual(len(FakeCapture.instances), 1)
        self.clock.advance(1.0)
        self.assertTrue(self.controller.sync(state()))
        self.assertEqual(len(FakeCapture.instances), 2)

    def test_frame_failure_closes_then_reopens_after_delay(self):
        self.assertTrue(self.controller.sync(state()))
        active = FakeCapture.instances[-1]
        FakeCapture.fail_read = True
        self.assertEqual(self.controller.read(), (False, None))
        self.assertTrue(active.closed)
        self.assertFalse(self.controller.sync(state()))
        FakeCapture.fail_read = False
        self.clock.advance(1.0)
        self.assertTrue(self.controller.sync(state()))


class ApplicationAndUiTests(unittest.TestCase):
    def test_application_state_sequence_maps_approved_screens(self):
        expected = ((SignalState.DISCONNECTED, "no-signal"),
                    (SignalState.PRESENT_NO_SIGNAL, "source-present"),
                    (SignalState.MODE_CHANGE, "mode-change"),
                    (SignalState.ERROR, "capture-error"))
        for signal, screen in expected:
            self.assertEqual(screen_for_state(application_state(state(signal), False)), screen)
        self.assertEqual(application_state(state(), False), ApplicationState.CAPTURE_ERROR)
        self.assertEqual(screen_for_state(application_state(state(), True)), "live")
        self.assertEqual(no_signal_screen(128, 128).size, (128, 128))

    def test_every_approved_screen_renders_at_native_size(self):
        for name in SCREEN_NAMES:
            with self.subTest(screen=name):
                image = render_screen(name)
                self.assertEqual(image.size, (128, 128))
                self.assertEqual(image.mode, "RGB")

    def test_menu_selection_is_clamped_and_focus_preview_updates(self):
        self.assertEqual(render_screen("menu", selected=-50).size, (128, 128))
        self.assertEqual(render_screen("menu", selected=len(MENU_ITEMS) + 50).size, (128, 128))
        low = render_screen("focus-settings", threshold=2, thickness=1)
        high = render_screen("focus-settings", threshold=9, thickness=3)
        self.assertNotEqual(low.tobytes(), high.tobytes())

    def test_display_input_and_menu(self):
        display = MockDisplayBackend()
        display.open()
        display.show(Image.new("RGB", (128, 128)))
        self.assertIsNotNone(display.last_frame)
        seen = []
        controller = InputController()
        controller.subscribe(seen.append)
        controller.dispatch(InputEvent.BUTTON_F1)
        self.assertEqual(seen, [InputEvent.BUTTON_F1])
        menu = Menu(("one", "two"))
        menu.dispatch(Action.MENU)
        menu.dispatch(Action.DOWN)
        self.assertEqual(menu.dispatch(Action.SELECT), "two")


if __name__ == "__main__":
    unittest.main()
