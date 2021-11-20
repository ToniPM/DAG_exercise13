from matplotlib import pyplot as plt
from math import atan2

import numpy as np
import cairo

from exercise13code.Box import Box
from exercise13code.Circle import Circle
from exercise13code.Polygon import Polygon
from exercise13code.algoringo import find_visibility_boundary
from exercise13code.util import circular_pairs


def surface_to_ndarray(surface):
    buf = surface.get_data()
    array = np.ndarray (shape=(surface.get_height(),surface.get_width(),4), dtype=np.uint8, buffer=buf)
    # return np.mean(array[:,:,:-1],axis=-1)
    return array[:,:,:-1]

if __name__ == '__main__':
    points = list(map(np.asarray,[(1,1),(6,2),(7,4),(6,5),(3,5),(2,4),(1,2)]))
    #points = list(map(np.asarray,[(1,1),(6,2),(7,4),(7,6),(3,5),(2,4),(1,2)]))
    #points = list(map(np.asarray,[(0,0),(1,0),(1,1),(0,1)]))
    #points = list(map(np.asarray,[(-1,0),(1,0),(1,1),(0,1)]))
    p = Polygon(points)
    bbox = Box.padded(p.bounding_box,2)

    im_width, im_height = 500, 500
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, im_width, im_height)
    ctx = cairo.Context(surface)
    res = max(im_width,im_height)/max(bbox.width, bbox.height)
    ctx.scale(res, res)
    ctx.translate(-bbox.min_x, -bbox.min_y)
    ctx.set_source_rgba(0, 0, 0, 1)
    ctx.rectangle(0,0,bbox.width,bbox.height)
    ctx.fill()
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(0.05)

    p.draw_on(ctx)

    """
    diagonal_pairs = list(p.diagonal_pairs())
    diagonal_pairs = diagonal_pairs[1:2]
    for p1, p2 in diagonal_pairs:
        Circle.diameter_of(p1, p2).draw_on(ctx)
    """

    transitions, sites = find_visibility_boundary(p)
    for site in sites:
        plt.scatter(*site, c="r")

    """
    for i1, i2, *_ in transitions:
        Circle.diameter_of(p.points[i1], p.points[i2]).draw_on(ctx)
    """

    for (i1, i2, *_),(p1, p2) in zip(transitions,circular_pairs(sites)):
        c = Circle.diameter_of(p.points[i1], p.points[i2])
        ctx.move_to(*p1)
        d1 = p1 - c.center
        d2 = p2 - c.center
        ctx.arc(*c.center, c.radius, atan2(*d1[::-1]), atan2(*d2[::-1]))
    ctx.stroke()

    d = 0.5/max(im_width,im_height)
    m = max(bbox.width, bbox.height)
    extent = [bbox.min_x - d, bbox.min_x + m + d, bbox.min_y - d, bbox.min_y + m + d]
    plt.imshow(np.flip(surface_to_ndarray(surface),axis=0), extent=extent)
    plt.show()