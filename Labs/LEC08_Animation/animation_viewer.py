import json
import time
from pathlib import Path

import pico2d as p

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
ANIMATION_ORDER = ["walk", "run", "jump", "attack"]
FRAME_TIME = {"walk": 0.10, "run": 0.09, "jump": 0.12, "attack": 0.10}
BASE_DIR = Path(__file__).resolve().parent


def main():
    with open(BASE_DIR / "kyo_animation.json", "r", encoding="utf-8") as file:
        animations = json.load(file)["animations"]

    p.open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    try:
        sprite_sheet = p.load_image(str(BASE_DIR / "kyo_animation.png"))
        animation_index = 0
        frame_index = 0
        previous_time = time.perf_counter()

        while True:
            for event in p.get_events():
                if event.type == p.SDL_QUIT:
                    return
                elif event.type == p.SDL_KEYDOWN and event.key == p.SDLK_ESCAPE:
                    return

            current_time = time.perf_counter()
            elapsed = current_time - previous_time
            previous_time = current_time

            if elapsed >= FRAME_TIME[ANIMATION_ORDER[animation_index]]:
                frame_index = (frame_index + 1) % len(animations[ANIMATION_ORDER[animation_index]])

            name = ANIMATION_ORDER[animation_index]
            frame = animations[name][frame_index]
            source_x = frame["x"]
            source_y = frame["y"]
            source_w = frame["w"]
            source_h = frame["h"]
            source_bottom = sprite_sheet.h - source_y - source_h

            p.clear_canvas()
            sprite_sheet.clip_draw(source_x, source_bottom, source_w, source_h, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            p.update_canvas()
            p.delay(0.01)
    finally:
        p.close_canvas()


if __name__ == "__main__":
    main()
