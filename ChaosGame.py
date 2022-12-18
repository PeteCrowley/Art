import math

from GeometryHelp import point_in_polygon
import random


class ChaosGame:
    """
    Polygons should be defined in an ordered list going counter-clockwise
    """
    def __init__(self, attractive_points, start_polygon=None, jump=1/2):
        self.start_polygon = attractive_points if start_polygon is None else start_polygon
        self.attractive_points = attractive_points
        self.position = self.x, self.y = self.choose_start_position()
        self.jump = jump

    def choose_start_position(self):
        return point_in_polygon(self.start_polygon)

    def move(self):
        attractive_x, attractive_y = random.choice(self.attractive_points)
        self.position = self.x, self.y = attractive_x * self.jump + self.x * (1-self.jump), attractive_y * self.jump + self.y * (1-self.jump)

    def get_point_list(self, iterations=1000) -> [float]:
        points = [self.position]
        for i in range(iterations-1):
            self.move()
            points.append(self.position)
        return points


class ChaosGameSpecialRule(ChaosGame):
    def __init__(self, attractive_points, start_polygon=None, jump=1/2, rule="no repeat"):
        super().__init__(attractive_points, start_polygon=start_polygon, jump=jump)
        self.legal_attractive_points = self.attractive_points
        if rule == "no repeats":
            self.r = 0
        elif rule == "no counter-clockwise":
            self.r = -1
        elif rule == "no clockwise":
            self.r = 1
        elif rule == "no opposite" and len(self.attractive_points) % 2 == 0:
            self.r = len(self.attractive_points) // 2

    def move(self):
        reference_x, reference_y = random.choice(self.legal_attractive_points)
        self.legal_attractive_points = [self.attractive_points[x] for x in range(len(self.attractive_points)) if
                                        self.attractive_points[(x+self.r) % len(self.attractive_points)] !=
                                        (reference_x, reference_y)]
        self.position = ((self.position[0] + reference_x) / 2, (self.position[1] + reference_y) / 2)


