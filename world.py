import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

INTERVAL = 20
FRAMES = 1000


class World:
    def __init__(self, x, y, vehicles, light=None):
        self.__light = light
        self.__vehicles = vehicles
        self.__width = x
        self.__height = y
        self.__patches = []

    def getLightIntensity(self):
        z = np.zeros((self.__width, self.__height))
        if self.__light:
            for i in range(self.__width):
                for j in range(self.__height):
                    z[i][j] = self.__light.getIntensity(i, j)
        return z

    def showScene(self, animate=False):
        fig = plt.figure()
        ax = plt.axes(xlim=(0, self.__width), ylim=(0, self.__height))
        plt.gca().set_aspect('equal', adjustable='box')

        for v in self.__vehicles:
            patch = plt.Polygon(v.getPoints())
            self.__patches.append(patch)
            ax.add_patch(patch)

        im = ax.pcolormesh(self.getLightIntensity())
        fig.colorbar(im, ax=ax)
        if animate:
            anim = animation.FuncAnimation(fig, self.animate,
                                           frames=FRAMES,
                                           interval=INTERVAL,
                                           blit=True)
        plt.show()

    def getPatches(self):
        patches = []
        for v in self.__vehicles:
            patches.append(v.getPatch())
        return patches

    def animate(self, i):
        for j, v in enumerate(self.__vehicles):
            v.moveForward(0.1)
            v.rotateRight(1)
            self.__patches[j].set_xy(v.getPoints())
        return []
