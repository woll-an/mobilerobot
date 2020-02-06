from vehicle import Vehicle
from light import Light
from world import World

x = 100
y = 100


v = Vehicle(3, 4)
l = Light(0.1 * x, 0.1 * y)

world = World(x, y, [v], l)

v.setState(50, 50, 200)


def controlVehicle(rightMeasurement, leftMeasurement):
    if rightMeasurement > leftMeasurement:
        v.rotateRight(1)
    else:
        v.rotateLeft(1)


v.controller = controlVehicle

world.showScene(True)
