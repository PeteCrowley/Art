import random
import math
import matplotlib.pyplot as plt
from ChaosGame import *
from GeometryHelp import regular_polygon, triangle_from_trapezoid

SIERPINSKI_DEPTH = 5

# Chaos Game Stuff
EQ_TRIANGLE = regular_polygon(3, 1)
SQUARE = regular_polygon(4, 1, start_angle=math.pi/4)
PENTAGON = regular_polygon(5, 1)
HEXAGON = regular_polygon(6, 1, start_angle=0)
Quad = [(-1, -1), (1, -1),
        (0.2, 0.4), (-0.2, 0.4)]
OCTAGON = regular_polygon(8, 1, start_angle=0)
from_trap = triangle_from_trapezoid(Quad)


ATTRACTIVE = Quad
GAME = ChaosGameSpecialRule
rule = "no repeats"
ITERATIONS = 1_000_000
phi = (1 + math.sqrt(5)) / 2
# cool = n/(n+3)
JUMP = .5

# Image Saving Parameters
SAVE_IMAGE = True
SAVE_FILE_PATH = "Images/Chaos_Game/" + "Trapezoid_No_Repeats" + ".jpg"

my_dpi = 100
plt.figure(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
plt.axis("off")
plt.title("Starting Shape: " + "Trapezoid" + ", Jump: " + str(round(JUMP, 3)) + ", Special Rules: " + (rule if
                                                            GAME.__name__.__contains__("Special") else "None"))

def draw_attractive_points(attractive_points):
    x, y = map(list, zip(*attractive_points))
    plt.plot(x, y, "ro")


def chaos_game(attractive_points, iterations=5000, draw_triangle=False):
    draw_attractive_points(attractive_points)
    if GAME.__name__.__contains__("Special"):
        cg = GAME(attractive_points, rule=rule)
    else:
        cg = GAME(attractive_points)
    cg.jump = JUMP
    points = cg.get_point_list(iterations=iterations)
    x, y = map(list, zip(*points))
    plt.plot(x, y, ",")


def sierpinski_triangle(depth, p1, p2, p3):
    if depth == 0:
        plt.plot([p1[0], p2[0], p3[0], p1[0]], [p1[1], p2[1], p3[1], p1[1]], "r")
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
    # sierpinski_triangle(SIERPINSKI_DEPTH, P1, P2, P3)
    chaos_game(ATTRACTIVE, iterations=ITERATIONS, draw_triangle=True)
    # sierpinski_triangle(SIERPINSKI_DEPTH, from_trap[0], from_trap[1], from_trap[2])
    if SAVE_IMAGE:
        plt.savefig(SAVE_FILE_PATH, bbox_inches="tight", dpi=my_dpi*5)


if __name__ == '__main__':
    draw_cool_stuff()

    plt.show()



