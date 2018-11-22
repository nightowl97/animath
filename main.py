import subprocess as sp
import numpy as np1
from shapes import *
import lib
import os
import cairocffi as cairo
from PIL import Image

# Check out wand

FFMPEG_BIN = "ffmpeg"

width = 1080
height = 720

command = [
    FFMPEG_BIN,
    '-y',                               # overwrite output if it exists
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-s', '%dx%d' % (width, height),    # frame size
    '-pix_fmt', 'rgb32',
    '-r', '30',                         # FPS
    '-i', '-',                          # input from pipe
    '-an',                              # no audio
    '-vcodec', 'mpeg',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-loglevel', 'error',
    'outputfile.mp4'
]

# #### CAIRO STUFF #### #
sfc = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(sfc)
ctx.set_source_rgb(1, 1, 1)
ctx.rectangle(0, 0, width, height)
ctx.fill()


lib.arrow(ctx, (0, 0, 0), 20, height / 2, width - 20, height / 2)
lib.arrow(ctx, (0, 0, 0), width / 2, height - 20, width / 2, 20)
lib.arrow(ctx, (0, 0, 0), width / 1.21, height / 1.21, 100, 100)

# function
ctx.set_source_rgb(1, 0, 0)
left_margin = - (width / 2) + 20
x = np.linspace(left_margin, (width / 2) - 20, 500)
ctx.translate(width / 2, height / 2)
ctx.move_to(left_margin, - 200 * np.cos(left_margin / 40))

pipe = sp.Popen(command, stdin=sp.PIPE)
for val in x:
    ctx.set_source_rgb(1, 0, 0)
    ctx.line_to(val, -(200 * np.cos(val / 40)))
    ctx.stroke_preserve()
    buffer = sfc.get_data()
    arr = np.ndarray(shape=(width, height), dtype=np.uint32, buffer=buffer)
    pipe.stdin.write(arr)

ctx.move_to(left_margin, np.exp(left_margin))
for val in x:
    ctx.line_to(val, - np.exp(val / 30))
    ctx.stroke_preserve()
    buffer = sfc.get_data()
    arr = np.ndarray(shape=(width, height), dtype=np.uint32, buffer=buffer)
    pipe.stdin.write(arr)

ctx.stroke()
ctx.save()
# write

# ##################### #

pipe.stdin.close()
#pipe.wait()
#print(os.getcwd())
sp.run(["vlc", "outputfile.mp4"])
