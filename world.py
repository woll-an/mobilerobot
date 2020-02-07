import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

INTERVAL = 20
FRAMES = 1000


class VehiclePlot:
    def __init__(self, vehicle, dimension):
        self.vehicle = vehicle
        self.circle = plt.Circle(
            (0, 0), radius=dimension/2, fc=None, ec='k', fill=False)
        r = dimension/2
        self.points = [
            [0, r], [-r*np.sqrt(2)/2, -r*np.sqrt(2)/2], [r*np.sqrt(2)/2, -r*np.sqrt(2)/2]]
        self.triangle = plt.Polygon(self.points)
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
    def __init__(self, x, y, vehicles, light=None):
        self.__light = light
        self.__vehicles = [VehiclePlot(v, 5) for v in vehicles]
        self.__width = x
        self.__height = y

    def getLightIntensity(self):
        z = np.zeros((self.__height, self.__width))
        if self.__light:
            for i in range(self.__height):
                for j in range(self.__width):
                    z[i][j] = self.__light.getIntensity(j, i)
        return z

    def showScene(self, animate=False):
        fig = plt.figure()
        ax = plt.axes(xlim=(0, self.__width), ylim=(0, self.__height))
        plt.gca().set_aspect('equal', adjustable='box')

        for v in self.__vehicles:
            ax.add_patch(v.circle)
            ax.add_patch(v.triangle)

        im = ax.pcolormesh(self.getLightIntensity())
        fig.colorbar(im, ax=ax)
        if animate:
            anim = animation.FuncAnimation(fig, self.animate,
                                           frames=FRAMES,
                                           interval=INTERVAL,
                                           blit=True)
        plt.show()

    def animate(self, i):
        for j, v in enumerate(self.__vehicles):
            x, y, _ = v.vehicle.getState()
            v.vehicle.moveWithLight(self.__light.getIntensityVector(x, y))
            v.updatePatches()
        return []
