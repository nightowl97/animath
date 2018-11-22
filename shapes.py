import numpy as np
from lib import *
import cairocffi as cairo


class Scene:
    """
    """
    def __init__(self, width=1080, height=720):
        self.t = 0
        self.objects = {}
        self.width, self.height = width, height
        self.fps = 30
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.context = cairo.Context(self.surface)
        self.context.set_source_rgb(1, 1, 1)
        self.context.rectangle(0, 0, self.width, self.height)

    def show_add(self, obj):
        assert isinstance(obj, Shape)
        # self.objects[]


class Arrow:
    def __init__(self, context, x0, y0, x1, y1):
        pass


class Graph:
    def __init__(self, context, width, height, origin=(0, 0), xlim=(-2,2), ylim=(-2,2)):
        self.context = context
        self.width = width
        self.height = height
        self.origin = origin
        self.xlim = xlim
        self.ylim = ylim
        self.axis_colors = (0, 0, 0)
        self.xmargin = width / 20
        self.ymargin = width / 20

    def show_axis(self):
        self.context.set_source_rgb(0, 0, 0)
        # self.


class Point:

    def __init__(self, x, y, stroke=(0, 0, 0), thickness=1):
        assert type(x) == int and type(y) == int
        self.x = x
        self.y = y
        self.thickness = thickness
        self.stroke = stroke


class Shape:
    def __init__(self, origin):
        assert isinstance(origin, Point)
        self.poi = np.array([])
        self.stroke = BLACK
        self.origin = origin

    def inst_draw(self, frame_array_list):
        """
        :param frame_array_list: list of frames as numpy arrays
        :return: same frame arrays but with object drawn
        flips the y coordinate of each frame, adds the geometric shape
        and returns the frames list.
        """
        raise Exception("inst_draw isn't implemented in parent class")


class Line(Shape):
    pass


class Circle(Shape):
    pass


class Ellipse(Shape):
    pass


class Arc(Shape):
    pass
