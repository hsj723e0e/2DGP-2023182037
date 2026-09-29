# 실습 과제 진행
import math
from pico2d import *

open_canvas(800,600)

character = load_image("character.png")

speed = 25

radius = 200

Top_start, Top_End = 50, 750
right_start, right_End = 550, 50
bottom_start, bottom_End = 750, 50
left_start, left_End = 50, 550

triangle_top_x, triangle_top_y = 400, 500
triangle_right_x, triangle_right_y = 700, 200
triangle_left_x, triangle_left_y = 100, 200

def move_circle():
    print("CIRCLE")
    for deg in range(0,360,speed):
        rad = math.radians(deg)
        x = 400 + radius * math.cos(rad)
        y = 300 + radius * math.sin(rad)
        draw_character(x,y)
    pass

def draw_top():
    print("Top")
    for x in range(Top_start, Top_End, speed):
        draw_character(x, right_start)
    pass

def draw_right():
    print("RIGHT")
    for y in range(right_start, right_End, -speed):
        draw_character(Top_End, y)
    pass

def draw_bottom():
    print("BOTTOM")
    for x in range(bottom_start, bottom_End, -speed):
        draw_character(x, right_End)
    pass

def draw_left():
    print("LEFT")
    for y in range(left_start, left_End, speed):
        draw_character(bottom_End, y)
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
    for x in range(triangle_top_x,triangle_right_x + 1,speed):
        y = (triangle_top_x + triangle_top_y) - x
        draw_character(x,y)
    pass #(400,500)에서 출발 -> #(700,200)도착
def draw_right_To_Left():
    for x in range(triangle_right_x, triangle_left_x - 1, -speed):
        draw_character(x, triangle_right_y)
    pass #(700,200)에서 출발 -> #(100,200)에 도착
def draw_left_To_Top():
    for x in range(triangle_left_x,triangle_top_x + 1,speed):
        y = x + (triangle_left_y - triangle_left_x)
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

close_canvas()