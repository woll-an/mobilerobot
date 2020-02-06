import numpy as np
import utilities


class Vehicle:
    def __init__(self, l, h):
        self.__T = utilities.stateToTransformationMatrix(0, 0, 0)
        self.__pointsV = [[0, h/2], [-l/2, -h/2], [l/2, -h/2]]
        self.controller = None

    def setState(self, x, y, theta):
        self.__T = utilities.stateToTransformationMatrix(x, y, theta)

    def getState(self):
        return utilities.transformationMatrixToState(self.__T)

    def getCorners(self):
        points_transformed = []
        for p in self.__pointsV:
            points_transformed.append(np.matmul(self.__T, p+[1])[0:2])
        return points_transformed

    def moveForward(self, distance):
        T_update = utilities.stateToTransformationMatrix(0, distance, 0)
        self.__T = np.matmul(self.__T, T_update)

    def rotateLeft(self, angle):
        T_update = utilities.stateToTransformationMatrix(0, 0, angle)
        self.__T = np.matmul(self.__T, T_update)

    def rotateRight(self, angle):
        T_update = utilities.stateToTransformationMatrix(0, 0, -angle)
        self.__T = np.matmul(self.__T, T_update)

    def lightMeasurement(self, light):
        v_sensor = np.matmul(self.__T[0:2, 0:2], np.array((0, 1)))
        print(np.degrees(utilities.angle_between(light, v_sensor)))

    def moveWithLight(self, light):
        self.lightMeasurement(light)
        return self.controller(1, 2)
