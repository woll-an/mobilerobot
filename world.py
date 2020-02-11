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


class World:
    def __init__(self, x, y, vehicles, light, obstacles):
        self.__light = light
        self.__vehicles = [VehiclePlot(v) for v in vehicles]
        self.__obstacles = obstacles
        self.__width = x
        self.__height = y

    def showScene(self, animate=False):
        fig = plt.figure()
        ax = plt.axes(xlim=(0, self.__width), ylim=(0, self.__height))
        plt.gca().set_aspect('equal', adjustable='box')

        for v in self.__vehicles:
            ax.add_patch(v.circle)
            ax.add_patch(v.triangle)

        for o in self.__obstacles:
            ax.add_patch(o.patch)

        im = ax.pcolormesh(self.__light.getIntensityField(
            self.__width, self.__height))
        fig.colorbar(im, ax=ax)

        if animate:
            anim = animation.FuncAnimation(fig, self.animate, interval=INTERVAL,
                                           blit=True)
        plt.show()

    def animate(self, i):
        for j, v in enumerate(self.__vehicles):
            for i in range(10):
                x, y, _ = v.vehicle.getState()
                v.vehicle.moveWithLight(
                    self.__light.getIntensityVector(x, y), self.free)
            v.updatePatches()
        return []

    def free(self, x, y, r):
        result = (x - r) >= 0 and (y - r) >= 0 and (x +
                                                    r) <= self.__width and (y + r) <= self.__height
        for o in self.__obstacles:
            result &= o.isOutside(x, y, r)
        return result
