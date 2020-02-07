import numpy as np


def stateToTransformationMatrix(x, y, theta):
    thetaRad = np.radians(theta)
    c, s = np.cos(thetaRad), np.sin(thetaRad)
    return np.array(((c, -s, x), (s, c, y), (0, 0, 1)))


def transformationMatrixToState(T):
    x = T[0, 2]
    y = T[1, 2]
    thetaRad = np.arccos(np.clip(T[0, 0], -1, 1))
    theta = np.degrees(thetaRad)
    return x, y, theta


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
