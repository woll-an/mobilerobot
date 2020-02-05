import numpy as np


def stateToTransformationMatrix(x, y, theta):
    thetaRad = np.radians(theta)
    c, s = np.cos(thetaRad), np.sin(thetaRad)
    return np.array(((c, -s, x), (s, c, y), (0, 0, 1)))


def transformationMatrixToState(T):
    x = T[0, 2]
    y = T[1, 2]
    thetaRad = np.arccos(T[0, 0])
    theta = np.degrees(thetaRad)
    return x, y, theta
