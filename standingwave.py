# import matplotlib.pyplot as plt
import ctypes as ct
from lib import *
from functools import partial

# TODO: Use OpenGL vertex buffers
# TODO: Add export to gif/mp4 functionality

# load_animation() requires GTK2 and throws ambiguous exceptions otherwise

# Math objects
sine1 = partial(sin, 1, 1, 1)  # TODO: Ugly system, find a better way to pass these to the Function to the class
func1 = Function(-2, 2, WIDTH, sine1)
sine2 = partial(sin, 1, 2, - 1)
func2 = Function(-2, 2, WIDTH, sine2)

# Pyglet initialization
config = pyglet.gl.Config(sample_buffers=1, samples=16)
window = pyglet.window.Window(WIDTH, HEIGHT, config=config)
glClearColor(*WHITE, 1)


# GL section
# VBO_ID = GLuint(0)
# glGenBuffers(1, ct.pointer(VBO_ID))  # Create a Vertex Buffer Object
# data = (Vertex * len(graph.items()))(*convert_to_ctype(list(graph.items())))
# glBindBuffer(GL_ARRAY_BUFFER, VBO_ID)
# glBufferData(GL_ARRAY_BUFFER, ct.sizeof(data), data, GL_DYNAMIC_DRAW)


# Frame by frame logic
def update(dt):
    # TODO: Implement batch system
    func1.update(dt)
    func2.update(dt)


pyglet.clock.schedule_interval(update, 1./60)


@window.event
def on_draw():
    window.clear()

    # Draw X-axis
    glClear(GL_COLOR_BUFFER_BIT)
    glLineWidth(2)
    glColor3f(0, 0, 0)
    glBegin(GL_LINE_STRIP)
    glVertex2f(0, HEIGHT / 2)
    glVertex2f(WIDTH, HEIGHT / 2)
    glEnd()
    # glEnableClientState(GL_VERTEX_ARRAY)
    # Draw function points
    func1.draw(BLUE)
    func2.draw(RED)
    # glVertexPointer(2, GL_FLOAT, 0, 0)
    # glDrawArrays(GL_POINTS, 0, 2)
    glFlush()


pyglet.app.run()
