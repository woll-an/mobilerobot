import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

INTERVAL = 20
FRAMES = 1000


class World:
    def __init__(self, x, y, lights, vehicles):
        self.__lights = lights
        self.__vehicles = vehicles
        self.__width = x
        self.__height = y
        self.__patches = []

        fig = plt.figure()
        ax = plt.axes(xlim=(0, x), ylim=(0, y))
        plt.gca().set_aspect('equal', adjustable='box')

        for v in vehicles:
            patch = plt.Polygon(v.getPoints())
            self.__patches.append(patch)
            ax.add_patch(patch)

        im = ax.pcolormesh(self.getIntensity())
        fig.colorbar(im, ax=ax)
        anim = animation.FuncAnimation(fig, self.animate,
                                       frames=FRAMES,
                                       interval=INTERVAL,
                                       blit=True)
        plt.show()

    def getIntensity(self):
        z = np.zeros((self.__width, self.__height))
        numLights = len(self.__lights)
        for i in range(self.__width):
            for j in range(self.__height):
                for l in self.__lights:
                    intensity = l.getIntensity(i, j)
                    z[i][j] += intensity/numLights
        return z

    def getPatches(self):
        patches = []
        for v in self.__vehicles:
            patches.append(v.getPatch())
        return patches

    def animate(self, i):
        for j, v in enumerate(self.__vehicles):
            # vector = np.zeros(2)
            # for l in self.__lights:
            #     T = v.getTransformationMatrix()
            #     vector_current = l.getIntensityVector(
            #         T[0, 2], T[1, 2])
            #     vector += vector_current
            v.setState(50, 50, 0)
            self.__patches[j].set_xy(v.getPoints())
        return []
