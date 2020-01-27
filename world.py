import numpy as np


class World:
    def __init__(self, x, y, lights, vehicles):
        self.lights = lights
        self.vehicles = vehicles
        self.width = x
        self.height = y

    def getIntensity(self):
        z = np.zeros((self.width, self.height))
        for i in range(self.width):
            for j in range(self.height):
                for l in self.lights:
                    intensity = l.getIntensity(i, j)
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
                vector_current = l.getIntensityVector(
                    v.T[0, 2], v.T[1, 2])
                vector += vector_current
            v.moveLight(vector)
            v.animate()
        return []
