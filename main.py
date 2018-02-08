import subprocess as sp
import numpy as np
import sys
from PIL import Image
from shapes import *
import lib, os

FFMPEG_BIN = "ffmpeg.exe"

original = Image.open("albert.jpg")
width = 1920
height = 1080
ori_arr = np.full((height, width, 3), 255, dtype='uint8')

# feed = np.array(feed)
arr = np.array(original)

command = [
    FFMPEG_BIN,
    '-y',                               # overwrite output if it exists
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-s', '%dx%d'%(width, height),      # frame size
    '-pix_fmt', 'rgb24',
    '-r', '60',                         # FPS
    '-i', '-',                          # input from pipe
    '-an',                              # no audio
    '-vcodec', 'mpeg',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-loglevel', 'error',
    'outputfile.mp4'
]

pipe = sp.Popen(command, stdin=sp.PIPE)

print(ori_arr.shape)

for i in range(180):
    pipe.stdin.write(ori_arr)

line = Line(Point(900, 20), Point(width // 2, height // 2), 1, lib.RED)
circ = Circle(Point(width//2, height//2), 100, lib.GREEN, 0,)
for j in range(120):
    pipe.stdin.write(circ.inst_draw([ori_arr])[0])

pipe.stdin.close()
pipe.wait()
pipe = sp.Popen(os.getcwd() + "\outputfile.mp4", shell=True)