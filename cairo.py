import math
import cairocffi as cairo
import numpy as np

sfc = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000)
ctx = cairo.Context(sfc)

src = ctx.set_source_rgb(0, 0, 0)
ctx.set_line_width(5)

ctx.move_to(0, 500)
ctx.line_to(500, -1000)

ctx.stroke()
ctx.save()
sfc.write_to_png("example.png")

