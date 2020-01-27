import numpy as np
from matplotlib import pyplot as plt

V = 5
OMEGA = 5


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
        dt = 1/20
        theta = OMEGA * (vr - vl) / self.l * dt
        x = 0
        y = V * (vl + vr) * dt
        c, s = np.cos(theta), np.sin(theta)
        T_update = np.array(((c, -s, x), (s, c, y), (0, 0, 1)))
        self.T = np.matmul(self.T, T_update)
        self.updatePatch()

    def sensorsTransformed(self):
        return np.matmul(self.T[0:2, 0:2], self.leftSensor), np.matmul(self.T[0:2, 0:2], self.rightSensor)

    def moveLight(self, lightDirection):
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
