import numpy as np
from enum import Enum
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.colors import ListedColormap

INTERVAL = 30
COMPUTATIONS = 30


class Space(Enum):
    BLOCKED = 0
    FREE = 1
    GOAL = 2
    START = 3
    EXPLORED = 4
    PATH = 5


class RobotPlot:
    def __init__(self, robot):
        self.robot = robot
        r = self.robot.radius
        self.circle = plt.Circle(
            (0, 0), radius=r, fc=None, ec='#fca31c', fill=False)
        self.points = [
            [0, r], [-r*np.sqrt(2)/2, -r*np.sqrt(2)/2], [r*np.sqrt(2)/2, -r*np.sqrt(2)/2]]
        self.triangle = plt.Polygon(self.points, fc='#fca31c')
        self.updatePatches()

    def updatePatches(self):
        points_transformed = []
        T = self.robot.T
        for p in self.points:
            p_aug = p+[1]
            points_transformed.append(np.matmul(T, p_aug)[0:2])
        self.triangle.set_xy(points_transformed)
        self.circle.center = T[0:2, 2]

class World:
    def __init__(self, x, y):
        self.width = x
        self.height = y

        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(0, self.width), ylim=(
            0, self.height), xlabel='x', ylabel='y')
        plt.gca().set_aspect('equal', adjustable='box')
        self.cm = None

    def setBackground(self, field):
        self.ax.pcolormesh(np.transpose(field), cmap=self.cm)

    def showScene(self):
        plt.show()

    def freeSpace(self, x, y, r):
        return (x - r) >= 0 and (y - r) >= 0 and (x +
                                                  r) <= self.width and (y + r) <= self.height


class ObstacleWorld(World):
    def __init__(self, x, y, obstacles=[], **kw):
        super(ObstacleWorld, self).__init__(x=x, y=y, **kw)
        self.obstacles = obstacles
        for o in self.obstacles:
            self.ax.add_patch(o.patch)

    def freeSpace(self, x, y, r):
        result = True
        for o in self.obstacles:
            result &= o.isOutside(x, y, r)
        return result and super().freeSpace(x, y, r)

class SpaceWorld(ObstacleWorld):
    def __init__(self, x, y, obstacles=[], **kw):
        super(SpaceWorld, self).__init__(x=x, y=y, obstacles=obstacles, **kw)
        colors = [''] * len(Space)
        colors[Space.BLOCKED.value] = '#885053'
        colors[Space.FREE.value] = '#C6ECAE'
        colors[Space.GOAL.value] = '#94C9A9'
        colors[Space.START.value] = '#FE5F55'
        colors[Space.EXPLORED.value] = '#777DA7'
        colors[Space.PATH.value] = '#1446A0'
        self.cm = ListedColormap(colors)

class RobotWorld(World):
    def __init__(self, x, y, robots=[], **kw):
        super(RobotWorld, self).__init__(x=x, y=y, **kw)
        self.robots = [RobotPlot(v) for v in robots]
        for v in self.robots:
            v.robot.collisionFree = self.freeSpace
            self.ax.add_patch(v.circle)
            self.ax.add_patch(v.triangle)

    def initAnimation(self, frames=100):
        return animation.FuncAnimation(
            self.fig, self.animate, interval=INTERVAL, frames=frames, blit=True)

    def animate(self, i):
        for j, v in enumerate(self.robots):
            for i in range(COMPUTATIONS):
                v.robot.moveBlindly()
            v.updatePatches()
        return []


class LightWorld(RobotWorld):
    def __init__(self, x, y, robots=[], light=None, **kw):
        super(LightWorld, self).__init__(x=x, y=y, robots=robots, **kw)
        self.light = light
        if self.light:
            field = self.light.getIntensityField(
                self.width, self.height)
            self.setBackground(field)

    def animate(self, i):
        for j, v in enumerate(self.robots):
            for i in range(COMPUTATIONS):
                if self.light:
                    v.robot.moveWithLight(self.light)
            v.updatePatches()
        return []

class LightObstacleWorld(LightWorld, ObstacleWorld):
    def __init__(self, x, y, robots=[], light=None, obstacles=[]):
        super(LightObstacleWorld, self).__init__(x=x, y=y, light=light, robots=robots, obstacles=obstacles)


