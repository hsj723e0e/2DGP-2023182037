import json
from pathlib import Path

import pico2d as p

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
BASE_DIR = Path(__file__).resolve().parent


def main():
    with open(BASE_DIR / "kyo_animation.json", "r", encoding="utf-8") as file:
        animations = json.load(file)["animations"]

    print("loaded animations:", list(animations.keys()))

    p.open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    try:
        sprite_sheet = p.load_image(str(BASE_DIR / "kyo_animation.png"))
        print("sprite sheet size:", sprite_sheet.w, sprite_sheet.h)
        p.clear_canvas()
        p.update_canvas()
        p.delay(0.2)
    finally:
        p.close_canvas()


if __name__ == "__main__":
    main()
