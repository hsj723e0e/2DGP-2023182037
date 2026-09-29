# 실습 과제 진행
import math
from pico2d import *

open_canvas(800,600)

character = load_image("character.png")



def move_circle():
    print("CIRCLE")
    for deg in range(0,360,5):
        rad = math.radians(deg)
        x = 400 + 200 * math.cos(rad)
        y = 300 + 200 * math.sin(rad)
        draw_character(x,y)
    pass

def draw_top():
    print("Top")
    for x in range(50,750,5):
        draw_character(x,550)
    pass

def draw_character(x, y):
    clear_canvas()
    character.draw(x,y)
    update_canvas()
    delay(0.1)

def draw_right():
    print("RIGHT")
    pass

def draw_left():
    print("LEFT")
    pass

def draw_bottom():
    print("BOTTOM")
    pass


def move_rectangle():
    print("RECTANGLE")
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()

    pass

def move_triangle():
    print("TRIANGLE")
    pass

while True:
    
    move_circle()
    move_rectangle()
    move_triangle()
    break;

close_canvas()