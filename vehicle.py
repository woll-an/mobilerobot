import numpy as np
import utilities


class Vehicle:
    def __init__(self, radius=3):
        self.T = utilities.stateToTransformationMatrix(0, 0, 0)
        self.radius = radius
        self.controller = None
        self.collisionFree = None

    def setState(self, x, y, theta):
        self.T = utilities.stateToTransformationMatrix(x, y, theta)

    def getState(self):
        return utilities.transformationMatrixToState(self.T)

    def moveForward(self, distance):
        T_update = utilities.stateToTransformationMatrix(0, distance, 0)
        T_new = np.matmul(self.T, T_update)
        x = T_new[0, 2]
        y = T_new[1, 2]
        if self.collisionFree(x, y, self.radius):
            self.T = T_new
            return True
        else:
            return False

    def rotateLeft(self, angle):
        T_update = utilities.stateToTransformationMatrix(0, 0, angle)
        self.T = np.matmul(self.T, T_update)

    def rotateRight(self, angle):
        T_update = utilities.stateToTransformationMatrix(0, 0, -angle)
        self.T = np.matmul(self.T, T_update)

    def lightMeasurement(self, light):
        R = self.T[0:2, 0:2]
        v_sensor_r = np.matmul(R, np.array((1, 0)))
        angle_r = np.degrees(utilities.angle_between(light, v_sensor_r))
        intensity = np.linalg.norm(light)
        right_meas = (angle_r/180) * intensity
        left_meas = (1-angle_r/180) * intensity
        return right_meas, left_meas

    def moveWithLight(self, light):
        right, left = self.lightMeasurement(light)
        return self.controller(self, right, left)

    def moveBlindly(self):
        self.controller(self)
