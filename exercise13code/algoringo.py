import numpy as np

from .Polygon import Polygon
from .util import circular_pairs


def find_visibility_boundary(poly: Polygon, tolerance=1e-10):
    n = poly.n

    # find starting pivot points - bottommost and leftmost.
    # When tied, pick the ones that would immediately become the pivot
    min_x = float("inf")
    min_xy = float("inf")
    min_x_idx = None
    min_y = float("inf")
    max_yx = -float("inf")
    min_y_idx = None
    for i, (x, y) in enumerate(poly.points):
        if abs(min_x-x) < tolerance:
            if min_xy > y:
                min_xy = y
                min_x_idx = i
        elif min_x > x:
            min_x = x
            min_xy = y
            min_x_idx = i

        if abs(min_y-y) < tolerance:
            if max_yx < x:
                max_yx = x
                min_y_idx = i
        elif min_y > y:
            min_y = y
            max_yx = x
            min_y_idx = i

    slopes = []
    for (x1, y1), (x2, y2) in circular_pairs(poly.points):
        rise = y2-y1
        run = x2-x1
        if abs(run)<tolerance:
            #slopes.append(rise*float("inf"))
            slopes.append(float("inf"))
        else:
            slopes.append(rise/run)
    inverted_slopes = list(map(lambda x: -1/x if x!=0 else float("inf"), slopes))

    leading_pivot = min_y_idx
    trailing_pivot = min_x_idx
    current_slope = 0

    transitions = []
    while True:
        transitions.append((leading_pivot, trailing_pivot,
                            current_slope, -1/current_slope if current_slope!=0 else float("inf")))
        leading_slope = slopes[leading_pivot]
        inverted_trailing_slope = inverted_slopes[trailing_pivot]
        if leading_slope < inverted_trailing_slope:
            if leading_slope < current_slope <= inverted_trailing_slope:
                current_slope = inverted_trailing_slope
                trailing_pivot = (trailing_pivot + 1) % n
            else:
                current_slope = leading_slope
                leading_pivot = (leading_pivot + 1) % n
        else:
            if inverted_trailing_slope < current_slope <= leading_slope:
                current_slope = leading_slope
                leading_pivot = (leading_pivot + 1) % n
            else:
                current_slope = inverted_trailing_slope
                trailing_pivot = (trailing_pivot + 1) % n

        if leading_pivot == min_y_idx and trailing_pivot == min_x_idx:
            break

    # THINGS TRANSITIONED TO:
    # (leading_idx, trailing_idx, leading_slope, trailing_slope)

    sites = []
    for t in transitions:
        i1, i2, s1, s2 = t
        (p1x, p1y), (p2x, p2y) = poly.points[i1], poly.points[i2]
        if np.isinf(s1):
            x = p1x
            y = p2y
        elif np.isinf(s2):
            x = p2x
            y = p1y
        else:
            x = (p2y - p1y + s1 * p1x - s2 * p2x) / (s1 - s2)
            y = s1 * x + (p1y - s1 * p1x)
        sites.append((x,y))

    return transitions, sites