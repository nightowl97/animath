from lib import *
import pyglet

# initialize
config = pyglet.gl.Config(sample_buffers=1, samples=16)
window = pyglet.window.Window(WIDTH, HEIGHT, config=config)
glClearColor(*WHITE, 1)

# Animation objects
horizon = Line((- WIDTH / 2, 0), (WIDTH / 2, 0), color=(.7, .7, .7, 1))

# Conduction objects
N = 100
xaxis = np.linspace(0, 1, N)
dx = xaxis[1] - xaxis[0]
# u = np.exp(-100 * (xaxis - .5) ** 2)  # Gaussian distribution
# u_n = np.exp(-100 * (xaxis - .5) ** 2)
u = np.zeros(N)
u_n = np.zeros(N)
coeff_cond = 90


def update(dt):
    global xaxis, dx, u, u_n
    delta_t = .0000005
    fourier = coeff_cond * (delta_t / dx ** 2)
    for i in range(1, len(xaxis) - 1):
        u[i] = u_n[i] + fourier * (u_n[i - 1] - 2 * u_n[i] + u_n[i + 1])  # Finite difference
    u[0] = 0  # Initial conditions
    u[-1] = 1
    u_n = u


pyglet.clock.schedule_interval(update, 1./60)
fpsdisplay = pyglet.clock.ClockDisplay()


@window.event
def on_draw():
    window.clear()
    glClear(GL_COLOR_BUFFER_BIT)
    horizon.draw()
    glLineWidth(4)
    glColor3f(1, 0, 0, 1)
    glBegin(GL_LINE_STRIP)
    for i, x in enumerate(xaxis):
        glVertex2f(x * WIDTH, (HEIGHT / 2) + u[i] * 3 * HEIGHT / 8)
    glEnd()
    glFlush()


pyglet.app.run()
