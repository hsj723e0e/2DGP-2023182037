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

def draw_right():
    print("RIGHT")
    for y in range(550,50,-5):
        draw_character(750,y)
    pass

def draw_bottom():
    print("BOTTOM")
    for x in range(750,50,-5):
        draw_character(x,50)
    pass

def draw_left():
    print("LEFT")
    for y in range(50,550,5):
        draw_character(50,y)
    pass


def draw_character(x, y):
    clear_canvas()
    character.draw(x,y)
    update_canvas()
    delay(0.1)

def move_rectangle():
    print("RECTANGLE")
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()

    pass


def draw_top_To_Right():
    for x in range(400,701,5):
        y = 900 - x
        draw_character(x,y)
    pass #(400,500)에서 출발 -> #(700,200)도착
def draw_right_To_Left():
    for x in range(700, 99, -5):
        draw_character(x, 200)
    pass #(700,200)에서 출발 -> #(100,200)에 도착
def draw_left_To_Top():
    for x in range(100,401,5):
        y = x + 100
        draw_character(x, y)
    pass #(100,200)에 출발 -> #(400,500)에 도착

def move_triangle():
    print("TRIANGLE")
    draw_top_To_Right()
    draw_right_To_Left()
    draw_left_To_Top()
    pass

while True:
    
    move_circle()
    move_rectangle()
    move_triangle()
    break;

close_canvas()