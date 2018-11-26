import subprocess as sp
import cairocffi as cairo
import numpy as np
import shapes

FFMPEG_BIN = "ffmpeg"
WIDTH = 720
HEIGHT = 480

command = [FFMPEG_BIN,
           '-y',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-s', '%dx%d' % (WIDTH, HEIGHT),
           '-pix_fmt', 'rgb32',
           '-r', '30',
           '-i', '-',
           '-an',
           '-vcodec', 'mpeg',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-loglevel', 'error',
           'outputtest.mp4'
           ]

frames = []
for j in range(150):  # 5 seconds' worth of frames
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    context = cairo.Context(surface)
    context.translate(0, HEIGHT)  # Bring origin down to bottom left
    context.scale(1, -1)  # Flip the y axis upwards
    context.set_source_rgb(1, 1, 1)
    context.paint()
    # Draw on the scene
    leftp = shapes.Point(10, HEIGHT // 2, thickness=4)
    rightp = shapes.Point(WIDTH - 10, HEIGHT // 2, thickness=4)
    horizontal_line = shapes.Line(context, surface, leftp, rightp)
    horizontal_line.draw()
    context.save()

    # Draw the sine waves
    context.set_source_rgb(1, 0, 0)
    context.new_path()
    print('frame: ' + str(j))
    phi = 3
    for i in range(10, WIDTH - 9, 4):
        context.line_to(i,               # Arbitrary scaling of amplitude and frequency
                       (HEIGHT / 2) + (200 * np.cos(i / 80 + (phi * j))))
        context.stroke_preserve()
    buffer = surface.get_data()
    frames.append(np.ndarray(shape=(WIDTH, HEIGHT), dtype=np.uint32, buffer=buffer))
    context.restore()

# Feed data to ffmpe
p = sp.Popen(command, stdin=sp.PIPE)
for frame in frames:
    p.stdin.write(frame)


p.stdin.close()
sp.run(['vlc', 'outputtest.mp4'])

