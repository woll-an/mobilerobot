from vehicle import Vehicle
from light import Light
from world import World

x = 150
y = 100

l = Light(x=80, y=50)

v1 = Vehicle()
v1.setState(50, 70, 200)

v2 = Vehicle()
v2.setState(50, 10, 200)


def love(vehicle, rightMeasurement, leftMeasurement):
    vel = 1 - rightMeasurement - leftMeasurement
    vehicle.moveForward(vel*0.5)
    if rightMeasurement > leftMeasurement:
        vehicle.rotateRight(1)
    elif leftMeasurement > rightMeasurement:
        vehicle.rotateLeft(1)


def hate(vehicle, rightMeasurement, leftMeasurement):
    vel = rightMeasurement + leftMeasurement
    vehicle.moveForward(vel*5)
    if rightMeasurement > leftMeasurement:
        vehicle.rotateRight(3)
    elif leftMeasurement > rightMeasurement:
        vehicle.rotateLeft(3)


v1.controller = love
v2.controller = hate

world = World(x=x, y=y, vehicles=[v1, v2], light=l)
world.showScene(animate=True)
