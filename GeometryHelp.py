import math
import random


def regular_polygon(sides, radius, start_angle=math.pi/2):
    polygon = []
    for v in range(sides):
        angle = start_angle + 2 * math.pi / sides * v
        polygon.append((radius*math.cos(angle), radius*math.sin(angle)))
    return polygon


def point_in_polygon(vertices):
    triangles = [(vertices[0], vertices[x], vertices[x+1]) for x in range(1, len(vertices)-1)]
    triangle_areas = [area_of_triangle(triangles[x]) for x in range(len(triangles))]
    total_area = sum(triangle_areas)
    odds_list = [(triangle_areas[x] + sum(triangle_areas[0:x]))/total_area for x in range(len(triangles))]
    n = random.random()
    for i in range(len(triangles)):
        if n <= odds_list[i]:
            return point_in_triangle(triangles[i][0], triangles[i][1], triangles[i][2])
    return None


def area_of_triangle(vertices):
    (x1, y1), (x2, y2), (x3, y3) = vertices
    l1 = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    l2 = math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2)
    l3 = math.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)
    p = (l1 + l2 + l3) / 2
    area = math.sqrt(p * (p - l1) * (p - l2) * (p - l3))
    return area


def point_in_triangle(pt1, pt2, pt3):
    """
    https://stackoverflow.com/questions/47410054/generate-random-locations-within-a-triangular-domain
    Random point on the triangle with vertices pt1, pt2 and pt3.
    """
    x, y = sorted([random.random(), random.random()])
    s, t, u = x, y - x, 1 - y
    return (s * pt1[0] + t * pt2[0] + u * pt3[0],
            s * pt1[1] + t * pt2[1] + u * pt3[1])


def triangle_from_trapezoid(trapezoid):
    for i in range(len(trapezoid)):
        for x in range(i+1, len(trapezoid)):
            if trapezoid[i][0] == trapezoid[x][0] or trapezoid[i][1] == trapezoid[x][1]:
                p1, p2 = trapezoid[i], trapezoid[x]
                p3 = trapezoid[(x+1) % len(trapezoid)]
                p4 = trapezoid[(i - 1) % len(trapezoid)]
                m1 = (p1[1] - p4[1]) / (p1[0] - p4[0])
                # y1 = m1(x-p1[0]) + p1[1]
                m2 = (p2[1] - p3[1]) / (p2[0] - p3[0])
                # y2 = m2(x-p2[0]) + p2[1]
                # m1(x-p1[0]) + p1[1] = m2(x-p2[0]) + p2[1]
                # m1x-m1p1[0]+p1[1] = m2x-m2p2[0]+p2[1]
                # m1x - m2x = -m2p2[0]+p2[1] - (-m1p1[0]+p1[1])
                x = (-m2 * p2[0] + p2[1] + m1 * p1[0] - p1[1]) / (m1 - m2)
                y = m2 * (x-p2[0]) + p2[1]
                difference = y - p3[1]
                new_p1 = (p1[0] + difference/m1, p1[1] + difference)
                new_p2 = (p2[0] + difference/m2, p2[1] + difference)
                short_triangle = shift_triangle([new_p1, new_p2, (x, y)], (0.8, -difference))
                return [p1, p2, (x, y)]


def shift_triangle(triangle, shift):
    new_triangle = []
    for point in triangle:
        new_triangle.append((point[0]+shift[0], point[1]+shift[1]))
    return new_triangle

