import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

INTERVAL = 10


class VehiclePlot:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        r = self.vehicle.radius
        self.circle = plt.Circle(
            (0, 0), radius=r, fc=None, ec='#a19d97', fill=False)
        self.points = [
            [0, r], [-r*np.sqrt(2)/2, -r*np.sqrt(2)/2], [r*np.sqrt(2)/2, -r*np.sqrt(2)/2]]
        self.triangle = plt.Polygon(self.points, fc='#fca31c')
        self.updatePatches()

    def updatePatches(self):
        points_transformed = []
        T = self.vehicle.T
        for p in self.points:
            p_aug = p+[1]
            points_transformed.append(np.matmul(T, p_aug)[0:2])
        self.triangle.set_xy(points_transformed)
        self.circle.center = T[0:2, 2]


class SimpleWorld:
    def __init__(self, x, y, vehicles=[]):
        self.width = x
        self.height = y
        self.vehicles = [VehiclePlot(v) for v in vehicles]
        for v in self.vehicles:
            v.vehicle.collisionFree = self.freeSpace

        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(0, self.width), ylim=(
            0, self.height), xlabel='x', ylabel='y')
        plt.gca().set_aspect('equal', adjustable='box')
        for v in self.vehicles:
            self.ax.add_patch(v.circle)
            self.ax.add_patch(v.triangle)

    def initAnimation(self, frames=100):
        return animation.FuncAnimation(
            self.fig, self.animate, interval=INTERVAL, frames=frames, blit=True)

    def showScene(self):
        plt.show()

    def freeSpace(self, x, y, r):
        return (x - r) >= 0 and (y - r) >= 0 and (x +
                                                  r) <= self.width and (y + r) <= self.height

    def animate(self, i):
        for j, v in enumerate(self.vehicles):
            for i in range(10):
                v.vehicle.moveBlindly()
            v.updatePatches()
        return []


class LightWorld(SimpleWorld):
    def __init__(self, x, y, vehicles=[], light=None):
        super().__init__(x, y, vehicles)
        self.light = light
        if self.light:
            self.ax.pcolormesh(self.light.getIntensityField(
                self.width, self.height))

    def animate(self, i):
        for j, v in enumerate(self.vehicles):
            for i in range(10):
                x, y, _ = v.vehicle.getState()
                if self.light:
                    v.vehicle.moveWithLight(
                        self.light.getIntensityVector(x, y))
            v.updatePatches()
        return []


class LightObstacleWorld(LightWorld):
    def __init__(self, x, y, vehicles=[], light=None, obstacles=[]):
        super().__init__(x, y, vehicles, light)
        self.obstacles = obstacles
        for o in self.obstacles:
            self.ax.add_patch(o.patch)

    def freeSpace(self, x, y, r):
        result = True
        for o in self.obstacles:
            result &= o.isOutside(x, y, r)
        return result and super().freeSpace(x, y, r)
