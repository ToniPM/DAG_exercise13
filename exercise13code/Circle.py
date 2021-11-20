import numpy as np

import cairo

from .Box import Box
from .geometric_primitives import Point


class Circle:
    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius

    @classmethod
    def diameter_of(cls, p1: Point, p2: Point):
        center = (p1+p2)/2
        radius = np.linalg.norm(p1-center)
        return cls(center, radius)

    def contains(self, p: Point):
        return np.linalg.norm(self.center-p) <= self.radius

    def draw_on(self, ctx: cairo.Context, fill=False):
        ctx.move_to(*self.center+np.asarray((self.radius,0)))
        ctx.arc(*self.center, self.radius, 0, 2*np.pi)
        if fill:
            raise NotImplementedError()
        ctx.stroke()

    @property
    def bounding_box(self):
        cx, cy = self.center
        r = self.radius
        return Box(cx-r, cx+r, cy-r, cy+r)
