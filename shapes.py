import math
import numpy as np
from lib import *
import aggdraw


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
    def __init__(self, point1, point2, thickness, stroke, infinite=False):
        assert isinstance(point1, Point) and isinstance(point2, Point)
        Shape.__init__(self, origin=point1)
        self.stroke = stroke
        self.thickness = thickness
        self.originp = point1
        self.endp = point2
        self.infinite = infinite
        if self.originp.x == self.endp.x:                            # If line is vertical
            self.slope = np.inf
            self.angle = PI / 2
            self.y_inter = None
        else:
            self.slope = (self.endp.y - self.originp.y) / (self.endp.x - self.originp.x)
            self.length = math.sqrt(((self.endp.y - self.originp.y) ** 2) + ((self.endp.x - self.originp.x) ** 2))
            self.angle = np.arctan(self.slope)
            # Check both points give correct y_intercept
            if (point1.y - point1.x * self.slope) - (point2.y - point2.x * self.slope) <= 1:
                self.y_inter = int((point1.y - point1.x * self.slope))

    def inst_draw(self, frame_array_list):
        drawn_frames = []
        for frame in frame_array_list:
            adjusted_frame = frame[::-1, :, :]
            if self.infinite:
                for x in range(frame.width):
                    y = int(self.slope * x + self.y_inter)
                    adjusted_frame[y, x] = self.stroke
            else:
                for x in range(min(self.originp.x, self.endp.x), max(self.originp.x, self.endp.x) + 1):
                    y = int(self.slope * x + self.y_inter)
                    adjusted_frame[y, x] = self.stroke
            drawn_frames.append(adjusted_frame[::-1, :, :])
        return drawn_frames


class Circle(Shape):
    def __init__(self, origin, radius, stroke, fill, thickness=1, points=1000):
        Shape.__init__(self, origin)
        self.radius = radius
        self.thickness = thickness
        self.stroke = stroke
        self.fill = fill
        self.num_points = points

    def inst_draw(self, frame_array_list):
        drawn_frames = []
        width = frame_array_list[0].shape[1]
        height = frame_array_list[0].shape[0]
        for frame in frame_array_list:
            adj_frame = frame[::-1, :, :]
            for theta in np.linspace(0, 2 * PI, int(2 * PI * self.radius)):
                x = int(self.origin.x + np.cos(theta) * self.radius)
                y = int(self.origin.y + np.sin(theta) * self.radius)
                thickness_dr = math.ceil(self.thickness / 2)
                if 0 <= x <= width and 0 <= y <= height:
                    adj_frame[y, x] = self.stroke
                x = int(self.origin.x + np.cos(theta) * (self.radius + thickness_dr))
                y = int(self.origin.y + np.sin(theta) * (self.radius + thickness_dr))
                if x <= width and y <= height:
                    adj_frame[y, x] = self.stroke
                x = int(self.origin.x + np.cos(theta) * (self.radius + thickness_dr))
                y = int(self.origin.y + np.sin(theta) * (self.radius + thickness_dr))
                if x <= width and y <= height:
                    adj_frame[y, x] = self.stroke
            drawn_frames.append(adj_frame[::-1, :, :])
        return drawn_frames


class Ellipse(Shape):
    pass


class Arc(Shape):
    pass
