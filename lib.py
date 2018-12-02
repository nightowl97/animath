import numpy as np
from pyglet.gl import *

# Helper functions, classes for various mathematical objects and geometric shapes

PI = np.pi

WIDTH = 720
HEIGHT = 480

WHITE = (1, 1, 1)
BLACK = (0, 0, 0)
RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)


def build_text_labels(text, colors, x=0, y=0):
    """
    Takes a list of strings "words" and a list of colors and builds labels or
    :param text: List of strings that make up the phrase
    :param colors: List of colors for each string
    :param x: x coordinate
    :param y: y coordinate
    :return:
    """
    cursor = x
    labels = []
    for i, word in enumerate(text):
        if x > WIDTH - 10:
            y -= 50  # new line
            cursor = 5
        if i > 0:
            prev_length = 10 * len(text[i - 1]) + 5
            cursor += prev_length
            labels.append(pyglet.text.Label(word,
                                            font_name='Latin Modern Roman', italic=True, bold=True,
                                            anchor_x='left', anchor_y='top',
                                            font_size=24,
                                            x=cursor, y=y,
                                            color=colors[i].append([255])))

        else:
            labels.append(pyglet.text.Label(word,
                                            font_name="Latin Modern Roman", italic=True, bold=True,
                                            anchor_x='left', anchor_y='top',
                                            font_size=24,
                                            x=cursor, y=y, color=(colors[i], 255)))


class MathFunction:
    # TODO: Pass the scaling and normalization logic to a different 'CartPlane' class
    def __init__(self, start, stop, n, f=None):
        """
        This will draw and keep track of the state of the 2D graph.
        A Function can be defined analytically, or as the superposition of a bunch of harmonics,
        which are also MathFunction objects. MathFunctions need to be continuous almost everywhere
        :param f: The function to graph
        :param start: Lower bound
        :param stop: Upper bound
        :param n: Number of discretisation points
        """
        self.f = f  # A
        self.terms = []  #
        self.n = n
        # Initial conditions
        self.t = 0
        if f is None:
            self.start = start
            self.stop = stop
            self.x = np.linspace(self.start, self.stop, self.n)
            self.y = np.ndarray(shape=(len(self.x),))
            self.graph_from_terms()
        else:
            self.start = start * WIDTH / 4  # Normalization factors, if defined analytically
            self.stop = stop * WIDTH / 4  # xaxis limit being the coordinate (2, 0)
            self.x = np.linspace(self.start, self.stop, self.n)
            self.y = self.f(0, self.x)
            self.graph = dict(zip(self.x, self.y))

    def draw(self, color=BLUE, linewidth=5):
        glPointSize(linewidth)
        glColor3f(*color)
        glBegin(GL_POINTS)
        for x, y in self.graph.items():  # may not be the best way to draw a graph
            glVertex2f(x + (WIDTH / 2), y + (HEIGHT / 2))
        glEnd()

    def update(self, dt):
        self.t += dt
        if self.f is not None:
            self.y = self.f(self.x, self.t)
            self.graph = dict(zip(self.x, self.y))
        else:
            self.graph_from_terms()

    def graph_from_terms(self):
        if len(self.terms) > 0:
            self.y = sum(fct.y for fct in self.terms)
            self.graph = dict(zip(self.x, self.y))

    def __add__(self, other):
        # Make sure intervals align and have same number of discretisation points
        if (self.start != other.start) or (self.stop != other.stop):
            raise Exception('Intervals do not align')
        assert(self.n == other.n)
        new = MathFunction(self.start, self.stop, self.n)
        new.terms.append(self)  # Probably ressource taxing, works for now
        new.terms.append(other)
        return new


# Shapes
class Circle:
    def __init__(self, origin, radius, thickness=2, color=(0, 0, 0, 1), fill=False, fill_color=(0, 0, 0, 1)):
        self.origin = origin
        self.r = radius
        self.thickness = thickness
        self.color = color
        self.fill = fill
        self.fill_color = fill_color
        self.n = 2 * np.pi * self.r  # Number of drawn points should be a function of its perimeter
        print(self.n)

    def draw(self):
        glPointSize(self.thickness)
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        for theta in np.linspace(0, 2 * np.pi, self.n):
            x = self.origin[0] + self.r * np.cos(theta)
            y = self.origin[1] + self.r * np.sin(theta)
            glVertex2f(x, y)
        glEnd()


class Line:
    def __init__(self, point1, point2, thickness=2,color=(0, 0, 0, 1)):
        assert(len(point1) == 2 and len(point2) == 2)
        self.point1 = point1
        self.point2 = point2
        self.slope = (point2[1] - point1[1])/(point2[0] - point1[0])
        self.angle = np.arctan(self.slope)
        self.thickness = thickness
        self.color = color

    def draw(self):
        glPointSize(self.thickness)
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        y_intercept = self.point1[1] - self.slope * self.point1[0]
        for i in range(WIDTH):
            glVertex2f(i, self.slope * i + y_intercept)
        glEnd()
