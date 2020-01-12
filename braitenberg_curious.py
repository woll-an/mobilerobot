import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import random

INTERVAL = 20
FRAMES = 1000


class Light:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getIntensity(self, x, y):
        diff = np.hstack((x-self.x, y-self.y))
        mag = np.linalg.norm(diff)
        return np.exp(-mag/30), diff/mag


class Vehicle:
    def __init__(self, x, y, thetaDeg, l, h):
        self.pointsV = [[0, h/2], [-l/2, -h/2], [l/2, -h/2]]
        self.rightSensor = np.array((1, 0))
        self.leftSensor = np.array((-1, 0))
        self.patch = plt.Polygon([[0.0, 0.0]])
        self.l = l
        theta = np.radians(thetaDeg)
        c, s = np.cos(theta), np.sin(theta)
        self.T = np.array(((c, -s, x), (s, c, y), (0, 0, 1)))
        self.updatePatch()

    def updatePatch(self):
        points_transformed = []
        for p in self.pointsV:
            points_transformed.append(np.matmul(self.T, p+[1])[0:2])
        self.patch.set_xy(points_transformed)

    def move(self, vl, vr):
        dt = 1.0/INTERVAL
        theta = (vr - vl) / self.l * dt
        x = 0
        y = (vl + vr) * dt
        c, s = np.cos(theta), np.sin(theta)
        T_update = np.array(((c, -s, x), (s, c, y), (0, 0, 1)))
        self.T = np.matmul(self.T, T_update)
        self.updatePatch()

    def moveLight(self, light):
        intensity, vec = light.getIntensity(self.T[0, 2], self.T[1, 2])
        speed = intensity*5
        leftTransformed = np.matmul(self.T[0:2, 0:2], self.leftSensor)
        rightTransformed = np.matmul(self.T[0:2, 0:2], self.rightSensor)
        left = np.linalg.norm(leftTransformed + vec)
        right = np.linalg.norm(rightTransformed + vec)
        self.move(right*speed, left*speed)


fig = plt.figure()
fig.set_dpi(100)

light = Light(20, 20)

ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
plt.gca().set_aspect('equal', adjustable='box')
vehicle = Vehicle(random.randint(0, 100), random.randint(0, 100), 0.0, 3, 4)
ax.add_patch(vehicle.patch)

z = np.zeros((100, 100))
for i in range(100):
    for j in range(100):
        intensity, _ = light.getIntensity(i, j)
        z.itemset((i, j), intensity)

im = ax.pcolormesh(z)
fig.colorbar(im, ax=ax)


def animate(i):
    vehicle.moveLight(light)
    return vehicle.patch,


anim = animation.FuncAnimation(fig, animate,
                               frames=FRAMES,
                               interval=INTERVAL,
                               blit=True)

plt.show()
