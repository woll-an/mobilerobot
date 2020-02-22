from robot import Robot
from light import Light
from world import LightObstacleWorld
from obstacle import Obstacle

l = Light(x=20, y=30)

v1 = Robot(radius=3)
v1.setState(x=50, y=70, theta=200)

v2 = Robot(radius=3)
v2.setState(x=50, y=10, theta=200)

o1 = Obstacle(40, 40, 10, 10)
o2 = Obstacle(50, 40, 20, 20)


def love(robot, rightMeasurement, leftMeasurement):
    vel = 1 - rightMeasurement - leftMeasurement
    robot.moveForward(vel*0.05)
    if rightMeasurement > leftMeasurement:
        robot.rotateRight(0.1)
    elif leftMeasurement > rightMeasurement:
        robot.rotateLeft(0.1)


def hate(robot, rightMeasurement, leftMeasurement):
    vel = rightMeasurement + leftMeasurement
    robot.moveForward(vel*0.3)
    if rightMeasurement > leftMeasurement:
        robot.rotateRight(0.2)
    elif leftMeasurement > rightMeasurement:
        robot.rotateLeft(0.2)


v1.controller = love
v2.controller = hate

lworld = LightObstacleWorld(x=100, y=100, robots=[
                            v1, v2], light=l, obstacles=[o1, o2])
lworld.initAnimation()
lworld.showScene()
