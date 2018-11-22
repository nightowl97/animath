import math
import cairocffi as cairo
import numpy as np
from shapes import *

sfc = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000)
ctx = cairo.Context(sfc)

src = ctx.set_source_rgb(0, 0, 0)
ctx.set_line_width(5)

ctx.move_to(0, 500)
ctx.line_to(500, -1000)

ctx.stroke()
ctx.save()
sfc.write_to_png("example.png")



# sc = Scene();
# l = Line(x, y, slope)
# g = graph(0, 1, 2, 4, xbounds=(-1, 2), ybounds=(-1, 1))
# g.add_func(sin)
# g.add_func(exp)


sc.show_add(l)
sc.show_add(g)