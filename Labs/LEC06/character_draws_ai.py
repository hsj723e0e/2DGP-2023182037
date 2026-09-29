# AI로 구현한 도형 경로 이동 실습
import math
from pathlib import Path

from pico2d import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
SPEED = 25
FRAME_DELAY = 0.1
RADIUS = 200

RECT_LEFT, RECT_RIGHT = 50, 750
RECT_BOTTOM, RECT_TOP = 50, 550
TRI_TOP = (400, 500)
TRI_RIGHT = (700, 200)
TRI_LEFT = (100, 200)


def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(FRAME_DELAY)


def move_circle():
    print("CIRCLE")
    for degrees in range(0, 360, SPEED):
        radians = math.radians(degrees)
        x = CANVAS_WIDTH / 2 + RADIUS * math.cos(radians)
        y = CANVAS_HEIGHT / 2 + RADIUS * math.sin(radians)
        draw_character(x, y)


def main():
    global character
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        image_path = Path(__file__).resolve().with_name("character.png")
        character = load_image(str(image_path))
        move_circle()
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
