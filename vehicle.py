import numpy as np
import utilities


class Vehicle:
    def __init__(self):
        self.T = utilities.stateToTransformationMatrix(0, 0, 0)
        self.controller = None

    def setState(self, x, y, theta):
        self.T = utilities.stateToTransformationMatrix(x, y, theta)

    def getState(self):
        return utilities.transformationMatrixToState(self.T)

    def getCorners(self):
        points_transformed = []
        for p in self.__pointsV:
            points_transformed.append(np.matmul(self.T, p+[1])[0:2])
        return points_transformed

    def moveForward(self, distance):
        T_update = utilities.stateToTransformationMatrix(0, distance, 0)
        self.T = np.matmul(self.T, T_update)

    def rotateLeft(self, angle):
        T_update = utilities.stateToTransformationMatrix(0, 0, angle)
        self.T = np.matmul(self.T, T_update)

    def rotateRight(self, angle):
        T_update = utilities.stateToTransformationMatrix(0, 0, -angle)
        self.T = np.matmul(self.T, T_update)

    def lightMeasurement(self, light):
        v_sensor_r = np.matmul(self.T[0:2, 0:2], np.array((1, 0)))
        v_sensor_l = np.matmul(self.T[0:2, 0:2], np.array((-1, 0)))
        angle_r = np.degrees(utilities.angle_between(light, v_sensor_r))
        intensity = np.linalg.norm(light)
        right_meas = (angle_r/180) * intensity
        left_meas = (1-angle_r/180) * intensity
        return right_meas, left_meas

    def moveWithLight(self, light):
        right, left = self.lightMeasurement(light)
        return self.controller(self, right, left)
