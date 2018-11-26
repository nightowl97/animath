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


class Point:
    def __init__(self, x, y, stroke=(0, 0, 0), thickness=1):
        assert type(x) == int and type(y) == int
        self.x = x
        self.y = y
        self.thickness = thickness
        self.stroke = stroke

    def draw(self, context, surface):
        assert isinstance(context, cairo.Context) and isinstance(surface, cairo.ImageSurface)
        context.save()
        context.set_source_rgb(*self.stroke)
        context.move_to(self.x, self.y)
        # There's probably a better way to do this
        context.line_to(self.x, self.y)
        context.stroke()


class Shape:
    def __init__(self, context, surface, origin, color=(0, 0, 0)):
        assert isinstance(context, cairo.Context) and isinstance(surface, cairo.ImageSurface)
        self.context = context
        self.surface = surface
        assert isinstance(origin, Point)
        self.poi = np.ndarray((self.surface.get_width(), self.surface.get_height()), dtype=np.uint32)
        self.stroke = BLACK
        self.origin = origin
        self.color = color


class Line(Shape):
    def __init__(self, context, surface, point1, point2):
        super().__init__(context, surface, point1)  # Use the first point as the origin
        assert isinstance(point2, Point)
        self.point2 = point2

    def draw(self):
        self.context.save()
        self.context.set_source_rgb(*self.color)
        self.context.move_to(self.origin.x, self.origin.y)
        self.context.line_to(self.point2.x, self.point2.y)
        self.context.stroke()


class Circle(Shape):
    pass


class Ellipse(Shape):
    pass


class Arc(Shape):
    pass
