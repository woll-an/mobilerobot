from vehicle import Vehicle
from light import Light
from world import World

x = 100
y = 100

world = World(x, y, [
    Light(0.1 * x, 0.1 * y),
    Light(0.9 * x, 0.1 * y),
    Light(0.5 * x, 0.9 * y)
], [
    Vehicle(3, 4),
    Vehicle(3, 4)
])
