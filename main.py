import os
from turtle import *
import math

# Turtle Setup
X_MAX = 10
Y_MAX = 10
WIDTH_HEIGHT = 800, 800
screen = Screen()
screen.setup(800, 800)
setworldcoordinates(-X_MAX, - Y_MAX, X_MAX, Y_MAX)

shape("turtle")
hideturtle()
speed(0)
tracer(0, 0)

# Star Parameters
STEP = 0.1
POINTS = 300
STAR_INSIDE_CIRCLE = False

# Koch's Triangle Parameters
BEST_LENGTHS = [0, 0, 0, 16, 9.8, 7.5, 5.5, 4.9, 4, 3.4, 3, 2.7, 2.5, 2.3, 2.15, 2, 1.9, 1.8, 1.7, 1.6, 1.5]
POSITION_SCALARS = [0, 0, 0, 0.288, 0.5, 0.625, 0.875, 1, 1.25, 1.375, 1.5, 1.625, 1.75, 2, 2.25, 2.4, 2.6, 2.75, 2.9, 3.05, 3.2]
KOCH_DEPTH = 3     # 3 -> 5, 4-14 -> 4, 15-20 -> 3
SIDES = 20         # 3 <= SIDES

# Image Saving Parameters
SAVE_IMAGE = True
SAVE_FILE_PATH = "Images/Koch_" + str(SIDES) + "-gon.jpg"


def fancy_star():
    max_distance_from_center = X_MAX * 9/10 if STAR_INSIDE_CIRCLE else (X_MAX / (2 / math.sqrt(2))) * 9/10
    for i in range(0, int(max_distance_from_center/STEP)+1):
        n = i * STEP
        penup()
        setposition(n, 0)
        pendown()
        goto(0, max_distance_from_center-n)
        goto(-n, 0)
        goto(0, -max_distance_from_center+n)
        goto(n, 0)
    radius = max_distance_from_center if STAR_INSIDE_CIRCLE else max_distance_from_center * (2 / math.sqrt(2))
    connect_points(radius)


def connect_points(radius):
    for i in range(POINTS // 4):
        penup()
        goto(0, 0)
        start_angle = i * 360 / POINTS
        setheading(start_angle)
        forward(radius)
        pendown()
        for x in range(1, 5):
            goto(radius*math.cos(math.radians(start_angle+90*x)), radius*math.sin(math.radians(start_angle+90*x)))
        circle_and_square(radius)


def circle_and_square(radius):
    penup()
    goto(radius, 0)
    setheading(90)
    pendown()
    circle(radius, steps=POINTS)
    penup()
    goto(radius, radius)
    pendown()
    for (x, y) in [(-1, 1), (-1, -1), (1, -1), (1, 1)]:
        goto(x*radius, y*radius)


def draw_koch_side(depth, length, sides):
    if depth <= 0:
        forward(length)
        return
    draw_koch_side(depth - 1, length / 3, sides)
    angle = 180 * (sides - 2) / sides
    left(angle)
    for i in range(sides-1):
        draw_koch_side(depth - 1, length / 3, sides)
        right(180 - angle)
    right(180)
    draw_koch_side(depth - 1, length / 3, sides)


def choose_start_height(sides, length):
    if 3 <= sides <= 20:
        return length * POSITION_SCALARS[sides]
    return length * 3.2


def koch_snowflake(sides, length):
    start_x = - length / 2
    start_y = choose_start_height(sides, length)

    penup()
    goto(start_x, start_y)
    pendown()
    for _ in range(sides):
        draw_koch_side(KOCH_DEPTH, length, sides)
        right(180-180 * (sides - 2) / sides)


def draw_cool_stuff():
    koch_snowflake(SIDES, BEST_LENGTHS[SIDES] if SIDES <= 20 else 1.5)
    update()
    if SAVE_IMAGE:
        save_image()
    mainloop()


def save_image():
    ts = getscreen()
    ts.getcanvas().postscript(file="Images/Art.eps")
    os.system(("magick -density 400 Images/Art.eps -quality 95 " + SAVE_FILE_PATH))
    os.remove("Images/Art.eps")


if __name__ == '__main__':
    draw_cool_stuff()



