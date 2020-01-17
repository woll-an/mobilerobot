import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import random

INTERVAL = 20
FRAMES = 1000
V = 5
OMEGA = 5
MAX_SPEED = 1.41
X = 200
Y = 200


class Light:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getIntensity(self, x, y):
        diff = np.hstack((x-self.x, y-self.y))
        mag = np.linalg.norm(diff)
        return np.exp(-mag/20), diff/mag*np.exp(-mag/20)


class Vehicle:
    def __init__(self, x, y, thetaDeg, l, h, behavior):
        self.pointsV = [[0, h/2], [-l/2, -h/2], [l/2, -h/2]]
        self.rightSensor = np.array((1, 0))
        self.leftSensor = np.array((-1, 0))
        self.patch = plt.Polygon([[0.0, 0.0]])
        self.behavior = behavior
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

    def moveForward(self, vl, vr):
        dt = 1.0/INTERVAL
        theta = OMEGA * (vr - vl) / self.l * dt
        x = 0
        y = V * (vl + vr) * dt
        c, s = np.cos(theta), np.sin(theta)
        T_update = np.array(((c, -s, x), (s, c, y), (0, 0, 1)))
        self.T = np.matmul(self.T, T_update)
        self.updatePatch()

    def sensorsTransformed(self):
        return np.matmul(self.T[0:2, 0:2], self.leftSensor), np.matmul(self.T[0:2, 0:2], self.rightSensor)

    def move(self, lightDirection):
        leftT, rightT = self.sensorsTransformed()
        leftMeasurement = np.linalg.norm(
            lightDirection - leftT)
        rightMeasurement = np.linalg.norm(
            lightDirection - rightT)
        leftWheel, rightWheel = self.behavior(
            leftMeasurement, rightMeasurement)
        self.moveForward(leftWheel, rightWheel)

    def animate(self):
        return self.patch,


class Map:
    def __init__(self, lights, vehicles):
        self.lights = lights
        self.vehicles = vehicles

    def getIntensity(self):
        z = np.zeros((X, Y))
        for i in range(X):
            for j in range(Y):
                for l in self.lights:
                    intensity, _ = l.getIntensity(i, j)
                    z[i][j] += intensity/len(self.lights)
        return z

    def getPatches(self):
        patches = []
        for v in self.vehicles:
            patches.append(v.patch)
        return patches

    def animate(self, i):
        for v in self.vehicles:
            vector = np.zeros(2)
            for l in self.lights:
                _, vector_current = l.getIntensity(
                    v.T[0, 2], v.T[1, 2])
                vector += vector_current
            v.move(vector)
            v.animate()
        return []


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

map = Map([
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

for p in map.getPatches():
    ax.add_patch(p)

im = ax.pcolormesh(map.getIntensity())
fig.colorbar(im, ax=ax)

anim = animation.FuncAnimation(fig, map.animate,
                               frames=FRAMES,
                               interval=INTERVAL,
                               blit=True)

plt.show()
