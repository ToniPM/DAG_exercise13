from typing import List
import itertools

import cairo

from .Box import Box
from .geometric_primitives import Point


class Polygon:
    def __init__(self, points: List[Point]):
        self.points = points

    @property
    def n(self):
        return len(self.points)

    def diagonal_pairs(self):
        for p1, p2 in itertools.combinations(self.points, 2):
            yield p1, p2

    def draw_on(self, ctx: cairo.Context, fill=False):
        ctx.move_to(*self.points[-1])
        for p in self.points:
            ctx.line_to(*p)
        ctx.line_to(*self.points[-1])
        if fill:
            raise NotImplementedError()
        ctx.stroke()

    @property
    def bounding_box(self):
        mnx = float("inf")
        mxx = -float("inf")
        mny = float("inf")
        mxy = -float("inf")
        for x,y in self.points:
            if mnx > x: mnx = x
            if mxx < x: mxx = x
            if mny > y: mny = y
            if mxy < y: mxy = y
        return Box(mnx, mxx, mny, mxy)

