from vehicle import Vehicle
from world import SimpleWorld


v1 = Vehicle(radius=3)
v1.setState(x=50, y=70, theta=200)


def move(vehicle):
    vehicle.moveForward(0.05)


v1.controller = move

sworld = SimpleWorld(x=100, y=100, vehicles=[v1])
sworld.showScene(animate=True)
