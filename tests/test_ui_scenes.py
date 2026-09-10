"""Hardware-free coverage for the reusable scene/widget renderer."""
import unittest
from dataclasses import replace

from PIL import ImageChops

from pi5_st7735_evf.navigation import NavigationState
from pi5_st7735_evf.ui.screens import render_screen
from pi5_st7735_evf.x1301 import SignalState, X1301State


class SceneRendererTests(unittest.TestCase):
    def assert_native(self, image):
        self.assertEqual(image.size, (128,128)); self.assertEqual(image.mode,"RGB")

    def test_boot_is_native_and_phase_changes_output(self):
        first=render_screen("boot",phase=0); second=render_screen("boot",phase=1)
        self.assert_native(first); self.assertIsNotNone(ImageChops.difference(first,second).getbbox())

    def test_source_present_accepts_missing_and_partial_runtime(self):
        self.assert_native(render_screen("source-present",runtime=None))
        self.assert_native(render_screen("source-present",runtime=object()))

    def test_source_present_reflects_lock_and_configuration(self):
        base=X1301State(SignalState.PRESENT_NO_SIGNAL,power_present=True)
        locked=replace(base,timings_locked=True); configured=replace(locked,configured=True)
        self.assertIsNotNone(ImageChops.difference(render_screen("source-present",runtime=base),render_screen("source-present",runtime=locked)).getbbox())
        self.assertIsNotNone(ImageChops.difference(render_screen("source-present",runtime=locked),render_screen("source-present",runtime=configured)).getbbox())

    def test_menu_cursor_moves_and_out_of_range_selection_is_safe(self):
        items=(("One","OFF"),("Two","ON"),("Three","3"))
        first=render_screen("menu",items=items,selected=0); second=render_screen("menu",items=items,selected=1)
        self.assert_native(first); self.assertIsNotNone(ImageChops.difference(first,second).getbbox())
        self.assert_native(render_screen("menu",items=items,selected=-100))
        self.assert_native(render_screen("menu",items=items,selected=100))

    def test_menu_values_are_live_without_navigation_mutation(self):
        navigation=NavigationState(menu_index=1); before=replace(navigation)
        off=render_screen("menu",navigation=navigation,selected=navigation.menu_index,items=(("Focus","OFF"),("Zebra","OFF")))
        on=render_screen("menu",navigation=navigation,selected=navigation.menu_index,items=(("Focus","OFF"),("Zebra","ON")))
        self.assertEqual(navigation,before); self.assertIsNotNone(ImageChops.difference(off,on).getbbox())

    def test_compatibility_entry_point_keeps_three_scenes_native(self):
        for scene in ("boot","source-present","menu"):
            with self.subTest(scene=scene): self.assert_native(render_screen(scene))


if __name__ == "__main__": unittest.main()
