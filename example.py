from vehicle import Vehicle
from light import Light
from world import World
from obstacle import Obstacle

l = Light(x=20, y=30)

v1 = Vehicle(radius=3)
v1.setState(x=50, y=70, theta=200)

v2 = Vehicle(radius=3)
v2.setState(x=50, y=10, theta=200)

o1 = Obstacle(40, 40, 10, 10)
o2 = Obstacle(50, 40, 20, 20)


def love(vehicle, rightMeasurement, leftMeasurement, free):
    vel = 1 - rightMeasurement - leftMeasurement
    vehicle.moveForward(vel*0.05, free)
    if rightMeasurement > leftMeasurement:
        vehicle.rotateRight(0.1)
    elif leftMeasurement > rightMeasurement:
        vehicle.rotateLeft(0.1)


def hate(vehicle, rightMeasurement, leftMeasurement, free):
    vel = rightMeasurement + leftMeasurement
    vehicle.moveForward(vel*0.3, free)
    if rightMeasurement > leftMeasurement:
        vehicle.rotateRight(0.2)
    elif leftMeasurement > rightMeasurement:
        vehicle.rotateLeft(0.2)


v1.controller = love
v2.controller = hate

world = World(x=100, y=100, vehicles=[v1, v2], light=l, obstacles=[o1, o2])
world.showScene(animate=True)