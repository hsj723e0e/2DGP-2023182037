# 실습 과제 진행
from pico2d import *
import math
import time 

open_canvas(800,600)

character = load_image("character.png")

r = 100
x = 400
y = 300
angle = 0

def move_circle():
    print("CIRCLE")
    clear_canvas()
    character.draw(400,300)

    update_canvas()
    pass

def move_rectangle():
    print("RECTANGLE")
    pass

def move_triangle():
    print("TRIANGLE")
    pass

while True:
    start = time.monotonic()
    while time.monotonic() - start < 10:
        move_circle()

    start = time.monotonic()
    while time.monotonic() - start < 10:
        move_rectangle()

    start = time.monotonic()
    while time.monotonic() - start < 10:
        move_triangle()

close_canvas()