from robot import Robot
from world import RobotWorld


v1 = Robot(radius=3)
v1.setState(x=50, y=70, theta=200)


def move(robot):
    robot.moveForward(0.05)


v1.controller = move

sworld = RobotWorld(x=100, y=100, robots=[v1])
sworld.initAnimation()
sworld.showScene()
