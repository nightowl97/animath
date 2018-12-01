import numpy as np
from pyglet.gl import *

# Helper functions, classes for various mathematical objects and geometric shapes

PI = np.pi

WIDTH = 1280
HEIGHT = 800

WHITE = (1, 1, 1)
BLACK = (0, 0, 0)
RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)


# travelling waves
def sin(amp, wavelength, w, t, x):
    # Transform to screen proportions, symmetric ref. frame with 4 * pi width
    # and amplitude of 1 corresponds to a third of the upper half of the ref. frame
    amp = amp * HEIGHT / 6
    wavelength = wavelength * (WIDTH / 4)
    return amp * np.sin((2 * PI * x) / wavelength - w * t)


def cos(amp, wavelength, w, t, x):
    amp = amp * HEIGHT / 6
    wavelength = wavelength * (WIDTH / 4)
    return amp * np.cos((2 * PI * x) / wavelength - w * t)


class Function:
    def __init__(self, start, stop, n, f=None):
        """
        This will draw and keep track of the state of the 2D graph
        :param f: The function to graph
        :param start: Lower bound
        :param stop: Upper bound
        :param n: Number of discretisation points
        """
        assert callable(f)
        self.f = f
        self.n = n
        self.start = start * WIDTH / 4  # Normalisation factors,
        self.stop = stop * WIDTH / 4    # xaxis limit being the coordinate (2, 0)
        self.x = np.linspace(self.start, self.stop, n)
        # Initial conditions
        self.t = 0
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
        self.y = self.f(self.t, self.x)
        self.graph = dict(zip(self.x, self.y))

    def __add__(self, other):
        # Make sure intervals align and have same number of discretisation points
        if (self.start != other.start) or (self.stop != other.stop):
            raise Exception('Intervals do not align')
        assert(self.n == other.n)
        # x = np.linspace(self.start, self.stop, self.n)
        # TODO: Make functions addable
