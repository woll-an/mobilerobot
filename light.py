import numpy as np


class Light:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getIntensity(self, x, y):
        diff = np.hstack((x-self.x, y-self.y))
        mag = np.linalg.norm(diff)
        return np.exp(-mag/20)

    def getIntensityVector(self, x, y):
        diff = np.hstack((x-self.x, y-self.y))
        mag = np.linalg.norm(diff)
        if mag == 0.0:
            return diff
        else: 
            return diff/mag*self.getIntensity(x, y)

    def getIntensityField(self, x, y):
        z = np.zeros((x, y))
        for i in range(x):
            for j in range(y):
                z[i][j] = self.getIntensity(i, j)
        return z
