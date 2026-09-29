from pico2d import *
import math

open_canvas(800, 600)

# 여기를 채우시오.
character = load_image("character.png")
grass = load_image('grass.png')

r = 100
x = 400
y = 300
angle = 0
theta = math.radians(angle)
while 1:
    clear_canvas()
    character.draw(x + r * math.cos(angle), y + r * math.sin(angle))
    update_canvas()
    angle +=0.1
    

    grass.draw(400,30)
    
    delay(0.1)


close_canvas()

