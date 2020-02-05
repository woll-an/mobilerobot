import numpy as np
import utilities

V = 5
OMEGA = 5


class Vehicle:
    def __init__(self, l, h):
        self.__pointsV = [[0, h/2], [-l/2, -h/2], [l/2, -h/2]]
        self.__x = 0
        self.__y = 0
        self.__theta = 0
        self.__rightSensor = np.array((1, 0))
        self.__leftSensor = np.array((-1, 0))
        self.__length = l

    # def moveForward(self, vl, vr):
    #     dt = 1/20
    #     theta = OMEGA * (vr - vl) / self.l * dt
    #     x = 0
    #     y = V * (vl + vr) * dt
    #     c, s = np.cos(theta), np.sin(theta)
    #     T_update = np.array(((c, -s, x), (s, c, y), (0, 0, 1)))
    #     self.T = np.matmul(self.T, T_update)
    #     self.updatePatch()

    def sensorsTransformed(self):
        return np.matmul(self.T[0:2, 0:2], self.leftSensor), np.matmul(self.T[0:2, 0:2], self.rightSensor)

    def setState(self, x, y, theta):
        self.__x = x
        self.__y = y
        self.__theta = theta

    def setT(self, T):
        self.__x, self.__y, self.__theta = utilities.transformationMatrixToState(
            T)

    def getT(self):
        return utilities.stateToTransformationMatrix(self.__x, self.__y, self.__theta)

    def getMeasurements(self, lightVector):
        leftT, rightT = self.sensorsTransformed()
        leftMeasurement = np.linalg.norm(
            lightDirection - leftT)
        rightMeasurement = np.linalg.norm(
            lightDirection - rightT)
        return leftMeasurement, rightMeasurement

    def getPoints(self):
        points_transformed = []
        T = utilities.stateToTransformationMatrix(
            self.__x, self.__y, self.__theta)
        for p in self.__pointsV:
            points_transformed.append(np.matmul(T, p+[1])[0:2])
        return points_transformed

    def moveForward(self, distance):
        T_update = np.array(((1, 0, 0), (0, 1, distance), (0, 0, 1)))
        self.setT(np.matmul(self.getT(), T_update))

    def rotateLeft(self, angle):
        # thetaRad = np.radians(theta)
        # c, s = np.cos(thetaRad), np.sin(thetaRad)
        # T_update = np.array(((1, 0, 0), (0, 1, distance), (0, 0, 1)))
        self.__theta += angle

    def rotateRight(self, angle):
        self.__theta -= angle
