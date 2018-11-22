import numpy as np
from enum import Enum
import cairocffi as cairo

PI = np.pi

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def arrow(context, rgbcolor, x0, y0, x1, y1):
    assert isinstance(context, cairo.Context)

    length = np.sqrt((y1 - y0) ** 2 + (x1 - x0) ** 2)
    if x1 != x0:
        angle = - np.arctan((y1 - y0) / (x1 - x0))
    else:
        angle = np.pi / 2
    arrowheadlen = length / 50
    lineheadx = x1 - arrowheadlen * np.cos(angle)
    lineheady = y1 + arrowheadlen * np.sin(angle)
    a1 = arrowheadlen / 2 * np.cos(np.pi / 2 - angle)
    b1 = arrowheadlen / 2 * np.sin(np.pi / 2 - angle)
    a2 = - arrowheadlen / 2 * np.sin(angle)
    b2 = - arrowheadlen / 2 * np.cos(angle)

    context.set_source_rgb(*rgbcolor)
    context.move_to(x0, y0)
    context.line_to(lineheadx, lineheady)
    context.stroke_preserve()
    context.rel_line_to(a1, b1)
    context.line_to(x1, y1)
    context.line_to(lineheadx + a2, lineheady + b2)
    context.line_to(lineheadx, lineheady)
    context.fill()

