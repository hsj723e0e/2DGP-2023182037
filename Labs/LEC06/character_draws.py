# 실습 과제 진행
from pico2d import *
import math

open_canvas(800,600)

character = load_image("character.png")

r = 100
x = 400
y = 300
angle = 0
theta = math.radians(angle)

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
    move_circle()
    move_rectangle()
    move_triangle()
    pass

close_canvas()