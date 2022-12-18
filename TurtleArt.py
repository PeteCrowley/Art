import os
import turtle
from turtle import *
from ChaosGame import *
import math
from GeometryHelp import regular_polygon, triangle_from_trapezoid

# Turtle Setup
X_MAX = 10
Y_MAX = 10
WIDTH, HEIGHT = 800, 800
screen = Screen()
screen.setup(WIDTH, HEIGHT)
screen.setworldcoordinates(-X_MAX, - Y_MAX, X_MAX, Y_MAX)

shape("turtle")
# hideturtle()
speed(8)
# tracer(0, 0)

# Star Parameters
STEP = 0.1
POINTS = 300
STAR_INSIDE_CIRCLE = False

# Koch's Triangle Parameters
BEST_LENGTHS = [0, 0, 0, 16, 9.8, 7.5, 5.5, 4.9, 4, 3.4, 3, 2.7, 2.5, 2.3, 2.15, 2, 1.9, 1.8, 1.7, 1.6, 1.5]
POSITION_SCALARS = [0, 0, 0, 0.288, 0.5, 0.625, 0.875, 1, 1.25, 1.375, 1.5, 1.625, 1.75, 2, 2.25, 2.4, 2.6,
                    2.75, 2.9, 3.05, 3.2]
KOCH_DEPTH = 3     # 3 -> 5, 4-14 -> 4, 15-20 -> 3
SIDES = 20         # 3 <= SIDES

# Triangle Fractal Parameters
SIERPINSKI_DEPTH = 6
P1, P2, P3 = ((0, -Y_MAX * 7.5/10 + X_MAX * 9/10 * math.sqrt(3)), (-X_MAX * 9/10, -Y_MAX * 7.5/10),
              (X_MAX * 9/10, -Y_MAX * 7.5/10))

# Chaos Game Stuff
EQ_TRIANGLE = regular_polygon(3, X_MAX * 9 / 10)
SQUARE = regular_polygon(4, X_MAX * 9 / 10, start_angle=math.pi/4)
PENTAGON = regular_polygon(5, X_MAX * 9 / 10)
HEXAGON = regular_polygon(6, X_MAX * 9 / 10, start_angle=0)
Quad = [(-X_MAX * 9/10, -Y_MAX * 9/10), (X_MAX * 9/10, -Y_MAX * 9/10),
        (-X_MAX * 1/10, Y_MAX * 4/10), (-X_MAX * 5/10, Y_MAX * 4/10)]
from_trap = triangle_from_trapezoid(Quad)


ATTRACTIVE = EQ_TRIANGLE
GAME = ChaosGame
rule = "no repeats"
ITERATIONS = 100000
phi = (1 + math.sqrt(5)) / 2
# cool = n/(n+3)
JUMP = .5

# Image Saving Parameters
SAVE_IMAGE = False
SAVE_FILE_PATH = "Images/Chaos_Game/" + "Octagon_.6_Jump" + ".jpg"


def fancy_star():
    max_distance_from_center = X_MAX * 9/10 if STAR_INSIDE_CIRCLE else (X_MAX / (2 / math.sqrt(2))) * 9/10
    max_distance_from_center -= max_distance_from_center % STEP
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


def draw_attractive_points(attractive_points):
    penup()
    color("Red")
    for point in attractive_points:
        goto(point)
        dot(10)
    color("Black")


def chaos_game(attractive_points, iterations=5000, draw_triangle=False):
    draw_attractive_points(attractive_points)
    if GAME.__name__.__contains__("Special"):
        cg = GAME(attractive_points, rule=rule)
    else:
        cg = GAME(attractive_points)
    cg.jump = JUMP
    points = cg.get_point_list(iterations=iterations)
    penup()
    for i in range(iterations):
        goto(points[i])
        dot(3)
    if len(attractive_points) == 3 and draw_triangle:
        color("red")
        turtle.pensize(2)
        sierpinski_triangle(SIERPINSKI_DEPTH, attractive_points[0], attractive_points[1], attractive_points[2])
        color("black")


def sierpinski_triangle(depth, p1, p2, p3):
    if depth == 0:
        penup()
        goto(p1)
        pendown()
        goto(p2)
        goto(p3)
        goto(p1)
        return
    new_p1 = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    new_p2 = (p1[0] + p3[0]) / 2, (p1[1] + p3[1]) / 2
    new_p3 = (p3[0] + p2[0]) / 2, (p3[1] + p2[1]) / 2
    sierpinski_triangle(depth-1, p1, new_p1, new_p2)
    sierpinski_triangle(depth - 1, p2, new_p1, new_p3)
    sierpinski_triangle(depth - 1, p3, new_p2, new_p3)


def draw_cool_stuff():
    # koch_snowflake(SIDES, BEST_LENGTHS[SIDES] if SIDES <= 20 else 1.5)
    # fancy_star()
    chaos_game(ATTRACTIVE, iterations=ITERATIONS, draw_triangle=True)
    # sierpinski_triangle(SIERPINSKI_DEPTH, P1, P2, P3)
    screen.update()
    if SAVE_IMAGE:
        save_image()
    screen.mainloop()


def save_image():
    ts = getscreen()
    ts.getcanvas().postscript(file="Images/Art.eps")
    os.system(("magick -density 400 Images/Art.eps -quality 95 " + SAVE_FILE_PATH))
    os.remove("Images/Art.eps")


if __name__ == '__main__':
    draw_cool_stuff()


