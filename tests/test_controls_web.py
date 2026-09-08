import json
import threading
import time
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import numpy as np
from PIL import Image

from pi5_st7735_evf.input import InputEvent, InputMapper, UIAction
from pi5_st7735_evf.config import build_parser, from_args
from pi5_st7735_evf.navigation import MENU_ITEMS, NavigationState
from pi5_st7735_evf.web import SharedStateHub, WebServer


class InputAndNavigationTests(unittest.TestCase):
    def test_partial_button_configuration(self):
        with patch.dict("os.environ", {"EVF_BUTTON_F1_GPIO": "5",
                                       "EVF_BUTTON_MENU_GPIO": "6"}, clear=True):
            config = from_args(build_parser().parse_args([]))
        self.assertEqual(config.button_pins, (("F1", 5), ("MENU", 6)))

    def test_default_and_unmapped_mapping(self):
        mapper = InputMapper()
        self.assertEqual(mapper.map(InputEvent.BUTTON_F1), UIAction.TOGGLE_FOCUS_ASSIST)
        self.assertEqual(mapper.map(InputEvent.ENCODER_RIGHT), UIAction.NEXT)
        self.assertIsNone(InputMapper({}).map(InputEvent.BUTTON_F1))

    def test_runtime_menu_navigation_wrap_and_return(self):
        nav = NavigationState(current_screen="no-signal")
        nav.dispatch(UIAction.MENU)
        self.assertEqual(nav.current_screen, "menu")
        nav.dispatch(UIAction.PREVIOUS)
        self.assertEqual(nav.menu_index, len(MENU_ITEMS) - 1)
        nav.dispatch(UIAction.NEXT)
        nav.dispatch(UIAction.BACK)
        self.assertEqual(nav.current_screen, "no-signal")

    def test_subscreens_toggles_threshold_and_shutdown_confirmation(self):
        nav = NavigationState(current_screen="live")
        for action, attr in ((UIAction.TOGGLE_FOCUS_ASSIST, "focus_assist_enabled"),
                             (UIAction.TOGGLE_ZEBRA, "zebra_enabled"),
                             (UIAction.TOGGLE_CROSSHAIR, "crosshair_enabled"),
                             (UIAction.TOGGLE_HISTOGRAM, "histogram_enabled")):
            nav.dispatch(action); self.assertTrue(getattr(nav, attr))
        nav.dispatch(UIAction.MENU); nav.menu_index = MENU_ITEMS.index("System Info")
        nav.dispatch(UIAction.SELECT); self.assertEqual(nav.current_screen, "system-info")
        nav.dispatch(UIAction.BACK); self.assertEqual(nav.current_screen, "menu")
        nav.menu_index = MENU_ITEMS.index("Focus Settings"); nav.dispatch(UIAction.SELECT)
        old = nav.focus_threshold; nav.dispatch(UIAction.INCREASE)
        self.assertGreater(nav.focus_threshold, old)
        nav.dispatch(UIAction.BACK); nav.menu_index = MENU_ITEMS.index("Shutdown")
        nav.dispatch(UIAction.SELECT)
        self.assertEqual(nav.current_screen, "shutdown"); self.assertFalse(nav.shutdown_requested)
        nav.dispatch(UIAction.SELECT); self.assertTrue(nav.shutdown_requested)

    def test_runtime_updates_do_not_destroy_menu(self):
        nav = NavigationState(current_screen="live")
        nav.dispatch(UIAction.MENU)
        nav.set_runtime_screen("no-signal", connected=False, streaming=False)
        self.assertEqual(nav.current_screen, "menu")
        nav.dispatch(UIAction.BACK)
        self.assertEqual(nav.current_screen, "no-signal")


class WebTests(unittest.TestCase):
    def setUp(self):
        self.hub = SharedStateHub()
        self.actions = []
        self.hub.publish(source_frame=np.zeros((20, 30, 3), np.uint8),
                         ui_image=Image.new("RGB", (128, 128)),
                         navigation=NavigationState(current_screen="live", streaming=True))
        self.server = WebServer(self.hub, self.actions.append, "127.0.0.1", 0)
        self.server.start()
        self.base = f"http://127.0.0.1:{self.server.address[1]}"

    def tearDown(self): self.server.close()

    def test_index_status_ui_and_video(self):
        self.assertIn(b"EVF Monitor", urlopen(self.base + "/", timeout=2).read())
        status = json.load(urlopen(self.base + "/api/status", timeout=2))
        self.assertEqual(status["screen"], "live")
        self.assertTrue(urlopen(self.base + "/ui.png", timeout=2).read().startswith(b"\x89PNG"))
        stream = urlopen(self.base + "/video.mjpg", timeout=2)
        self.assertIn(b"--frame", stream.read(256)); stream.close()

    def test_action_validation(self):
        request = Request(self.base + "/api/action", method="POST",
                          data=b'{"action":"MENU"}', headers={"Content-Type": "application/json"})
        self.assertEqual(urlopen(request, timeout=2).status, 202)
        self.assertEqual(self.actions, [UIAction.MENU])
        bad = Request(self.base + "/api/action", method="POST",
                      data=b'{"action":"SHELL"}', headers={"Content-Type": "application/json"})
        with self.assertRaises(HTTPError) as raised: urlopen(bad, timeout=2)
        self.assertEqual(raised.exception.code, 400)

    def test_hotplug_latest_frame_semantics(self):
        before = self.hub.status()["generation"]
        self.hub.publish(source_frame=None, navigation=NavigationState(current_screen="no-signal"))
        self.hub.publish(source_frame=np.ones((2, 2, 3), np.uint8),
                         navigation=NavigationState(current_screen="live", streaming=True))
        self.assertGreater(self.hub.status()["generation"], before)
        self.assertTrue(self.hub.status()["streaming"])
        self.assertGreater(len(self.hub.jpeg()), 0)


if __name__ == "__main__": unittest.main()
