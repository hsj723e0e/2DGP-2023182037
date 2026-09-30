"""Timing and asset checks; no graphical window is needed."""

import unittest

from animation_viewer import (
    ANIMATION_ORDER, FRAME_SECONDS, PAUSE_SECONDS, REPEAT_COUNT, Playback, load_frames,
)


class AnimationTests(unittest.TestCase):
    def test_variable_counts_and_dimensions(self):
        animations = load_frames()
        self.assertEqual([len(animations[n]) for n in ANIMATION_ORDER], [11, 6, 8, 10])
        for frames in animations.values():
            self.assertGreater(len({(f["w"], f["h"]) for f in frames}), 1)
            self.assertTrue(all(f["w"] > 0 and f["h"] > 0 for f in frames))

    def test_five_complete_cycles_then_one_second_pause(self):
        animations = load_frames()
        player = Playback(animations)
        for _ in range(2):
            for name in ANIMATION_ORDER:
                self.assertEqual(player.name, name)
                for cycle in range(REPEAT_COUNT):
                    for index in range(len(animations[name])):
                        self.assertEqual(player.frame_index, index)
                        self.assertFalse(player.paused)
                        player.update(FRAME_SECONDS[name])
                    self.assertEqual(player.completed_cycles, cycle + 1)
                self.assertTrue(player.paused)
                self.assertEqual(player.frame_index, len(animations[name]) - 1)
                player.update(PAUSE_SECONDS - 0.001)
                self.assertTrue(player.paused)
                self.assertEqual(player.name, name)
                player.update(0.001)
                self.assertFalse(player.paused)
                self.assertEqual(player.frame_index, 0)
        self.assertEqual(player.name, "walk")

    def test_large_time_step_crosses_animation_boundaries(self):
        animations = load_frames()
        total = sum(len(animations[n]) * FRAME_SECONDS[n] * REPEAT_COUNT
                    + PAUSE_SECONDS for n in ANIMATION_ORDER)
        player = Playback(animations)
        player.update(total * 3 + FRAME_SECONDS["walk"] * 2)
        self.assertEqual(player.name, "walk")
        self.assertEqual(player.frame_index, 2)
        self.assertEqual(player.completed_cycles, 0)


if __name__ == "__main__":
    unittest.main()
