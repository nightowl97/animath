# import matplotlib.pyplot as plt
from lib import *
from functools import partial

# TODO: Use OpenGL vertex buffers
# TODO: Add export to gif/mp4 functionality
# TODO: Add LateX text integration

# load_animation() requires GTK2 and throws ambiguous exceptions otherwise


# Mathematical objects: travelling waves
def sin(amp, k, w, x, t=0):
    """Transform to screen proportions, symmetric ref. frame with 4 * pi width
    and amplitude of 1 corresponds to a third of the upper half of the ref. frame
    :param amp: Amplitude
    :param k: wave number where k = 2 * pi / λ
    :param w: omega, or the temporal frequency
    :param x: x coordinate
    :param t: time coordinate
    :return: value of the wave at the point (x, t)
    """
    amp = amp * HEIGHT / 6
    k = k / (WIDTH / 4)
    return amp * np.sin(2 * PI * (k * x - w * t))


def cos(amp, k, w, x, t=0):
    amp = amp * HEIGHT / 6
    k = k / (WIDTH / 4)
    return amp * np.cos(2 * PI * (k * x - w * t))


sine1 = partial(cos, 1, 1/8, .2)  # TODO: Ugly system, find a better way to pass these to the MathFunction to the class
func1 = MathFunction(-2, 2, WIDTH, sine1)
sine2 = partial(cos, 1, -1/8, .2)
func2 = MathFunction(-2, 2, WIDTH, sine2)
func3 = func1 + func2
circ = Circle((WIDTH / 2, HEIGHT / 2), 200, thickness=2)
line = Line((WIDTH / 4, 0), (WIDTH / 2, HEIGHT / 2))

# Pyglet initialization
config = pyglet.gl.Config(sample_buffers=1, samples=16)
window = pyglet.window.Window(WIDTH, HEIGHT, config=config)
glClearColor(*WHITE, 1)


# Frame by frame logic
def update(dt):
    # TODO: Implement batch system
    func1.update(dt)
    func2.update(dt)
    func3.update(dt)


pyglet.clock.schedule_interval(update, 1./60)
text = ['f(x)', '+', "g(x)", '=', 'h(x)']
colors = [BLUE, BLACK, RED, BLACK, GREEN]
labels = []
cursor = 5
for i, word in enumerate(text):
    labels.append(pyglet.text.Label(word, font_name='Latin Modern Roman', italic=True, bold=True,
                                    font_size=24, anchor_x='left', anchor_y='top',
                                    x=cursor, y=HEIGHT - 5, color=tuple((255 * c for c in colors[i])) + (255,)))
    cursor += 12 * len(word) + 18
# svg = pyglet.image.load('fgh.png')
# svg.anchor_x, svg.anchor_y = 0, svg.height
# svgsprite = pyglet.sprite.Sprite(svg)
# svgsprite.x, svgsprite.y = 5, HEIGHT - 100

fps_display = pyglet.clock.ClockDisplay()


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
    func3.draw(GREEN)
    [label.draw() for label in labels]
    fps_display.draw()
    # circ.draw()
    # line.draw()
    # svgsprite.draw()
    # glVertexPointer(2, GL_FLOAT, 0, 0)
    # glDrawArrays(GL_POINTS, 0, 2)
    glFlush()


pyglet.app.run()
