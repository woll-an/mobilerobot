import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from vehicle import Vehicle
from light import Light
from wprld import World
import random

INTERVAL = 20
FRAMES = 1000
MAX_SPEED = 1.41
X = 200
Y = 200


def fear(left, right):
    return left, right


def hate(left, right):
    return right, left


def love(left, right):
    return MAX_SPEED-left, MAX_SPEED-right


def curious(left, right):
    return MAX_SPEED-right, MAX_SPEED-left


fig = plt.figure()
fig.set_dpi(100)

world = World(X, Y, [
    Light(10, 10),
    Light(190, 10),
    Light(100, 190)
], [
    Vehicle(random.randint(0, X), random.randint(0, Y),
            random.randint(-180, 180), 3, 4, curious),
    Vehicle(random.randint(0, X), random.randint(0, Y),
            random.randint(-180, 180), 3, 4, curious),
    Vehicle(random.randint(0, X), random.randint(0, Y),
            random.randint(-180, 180), 3, 4, curious),
    Vehicle(random.randint(0, X), random.randint(0, Y),
            random.randint(-180, 180), 3, 4, fear),
    Vehicle(random.randint(0, X), random.randint(0, Y),
            random.randint(-180, 180), 3, 4, fear),
    Vehicle(random.randint(0, X), random.randint(
        0, Y), random.randint(-180, 180), 3, 4, fear)
])

ax = plt.axes(xlim=(0, X), ylim=(0, Y))
plt.gca().set_aspect('equal', adjustable='box')

for p in world.getPatches():
    ax.add_patch(p)

im = ax.pcolormesh(world.getIntensity())
fig.colorbar(im, ax=ax)

anim = animation.FuncAnimation(fig, world.animate,
                               frames=FRAMES,
                               interval=INTERVAL,
                               blit=True)

plt.show()
