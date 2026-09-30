import json
from pathlib import Path

import pico2d as p

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
ANIMATION_ORDER = ["walk", "run", "jump", "attack"]
BASE_DIR = Path(__file__).resolve().parent


def main():
    with open(BASE_DIR / "kyo_animation.json", "r", encoding="utf-8") as file:
        animations = json.load(file)["animations"]

    print("actions:", ANIMATION_ORDER)
    for name in ANIMATION_ORDER:
        print(name, len(animations[name]))

    p.open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    try:
        sprite_sheet = p.load_image(str(BASE_DIR / "kyo_animation.png"))
        sprite_sheet.draw(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        p.update_canvas()
        p.delay(0.3)
    finally:
        p.close_canvas()


if __name__ == "__main__":
    main()
