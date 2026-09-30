import json
import math
import time
from pathlib import Path

import pico2d as p


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

ANIMATION_ORDER = ["walk", "run", "jump", "attack"]

ANIMATION_FRAME_COUNT = {
    "walk": 11,
    "run": 6,
    "jump": 8,
    "attack": 10,
}

FRAME_TIME = {
    "walk": 0.10,
    "run": 0.09,
    "jump": 0.12,
    "attack": 0.10,
}

ANIMATION_SPEED = {
    "walk": 1.0,
    "run": 2.0,
    "jump": 1.0,
    "attack": 1.0,
}

ANIMATION_REPEAT = {
    "walk": 1,
    "run": 2,
    "jump": 1,
    "attack": 1,
}

REPEAT_COUNT = 5
PAUSE_TIME = 1.0

BASE_DIR = Path(__file__).resolve().parent


def main():
    with open(BASE_DIR / "kyo_animation.json", "r", encoding="utf-8") as file:
        animations = json.load(file)["animations"]

    for name in ANIMATION_ORDER:
        actual = len(animations[name])
        expected = ANIMATION_FRAME_COUNT[name]
        if actual != expected:
            print(f"[Warning] {name}: expected {expected} frames, got {actual}")

    all_frames = [frame for name in ANIMATION_ORDER for frame in animations[name]]
    minimum_height = min(frame["h"] for frame in all_frames)
    scale = (SCREEN_HEIGHT / 2) / minimum_height

    p.open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)

    try:
        sprite_sheet = p.load_image(str(BASE_DIR / "kyo_animation.png"))

        font_path = Path(p.__file__).resolve().parent / "data" / "ConsolaMalgun.ttf"
        font = p.load_font(str(font_path), 22)

        animation_index = 0
        frame_index = 0
        repeat_count = 0
        cycle_count = {name: 0 for name in ANIMATION_ORDER}
        paused = False
        elapsed = 0.0
        previous_time = time.perf_counter()

        while True:
            for event in p.get_events():
                if event.type == p.SDL_QUIT:
                    return
                elif event.type == p.SDL_KEYDOWN and event.key == p.SDLK_ESCAPE:
                    return

            current_time = time.perf_counter()
            elapsed += current_time - previous_time
            previous_time = current_time

            while True:
                if paused:
                    if elapsed < PAUSE_TIME:
                        break
                    elapsed -= PAUSE_TIME
                    paused = False
                    animation_index = 0
                    frame_index = 0
                    repeat_count = 0
                    cycle_count = {name: 0 for name in ANIMATION_ORDER}
                    continue

                name = ANIMATION_ORDER[animation_index]
                frames = animations[name]
                total_frames = len(frames)

                duration = FRAME_TIME[name] / ANIMATION_SPEED[name]

                if elapsed < duration:
                    break

                elapsed -= duration

                if frame_index + 1 < total_frames:
                    frame_index += 1
                else:
                    frame_index = 0
                    cycle_count[name] += 1

                    if cycle_count[name] >= ANIMATION_REPEAT[name]:
                        cycle_count[name] = 0
                        animation_index += 1

                        if animation_index >= len(ANIMATION_ORDER):
                            animation_index = 0
                            repeat_count += 1

                            if repeat_count >= REPEAT_COUNT:
                                paused = True
                                animation_index = len(ANIMATION_ORDER) - 1
                                frame_index = len(animations["attack"]) - 1
                                break

            name = ANIMATION_ORDER[animation_index]
            frames = animations[name]
            frame = frames[frame_index]

            source_x = frame["x"]
            source_y = frame["y"]
            source_width = frame["w"]
            source_height = frame["h"]

            base_scale = 1.0
            if name == "attack":
                total_attack_frames = len(frames)
                if total_attack_frames > 1:
                    phase = frame_index / (total_attack_frames - 1)
                    base_scale = 1.0 + 0.30 * math.sin(phase * math.pi)
                else:
                    base_scale = 1.0

            source_bottom = sprite_sheet.h - source_y - source_height
            draw_width = round(source_width * scale * base_scale)
            draw_height = round(source_height * scale * base_scale)

            p.clear_canvas()

            sprite_sheet.clip_draw(
                source_x,
                source_bottom,
                source_width,
                source_height,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                draw_width,
                draw_height,
            )

            if paused:
                remaining = max(0.0, PAUSE_TIME - elapsed)
                status = f"PAUSE: {remaining:.1f}s"
            else:
                status = f"SEQ {repeat_count + 1}/{REPEAT_COUNT}"

            font.draw(25, SCREEN_HEIGHT - 25, f"{name.upper()}   {status}", (30, 30, 30))
            font.draw(25, 25, f"FRAME: {frame_index + 1}/{len(frames)}   SIZE: {source_width}x{source_height}   ESC: EXIT", (30, 30, 30))

            p.update_canvas()
            p.delay(0.01)

    finally:
        p.close_canvas()


if __name__ == "__main__":
    main()
