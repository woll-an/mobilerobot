import numpy as np
from world import SpaceWorld
from world import Space
from obstacle import Obstacle

o1 = Obstacle(10, 20, 30, 5)
o2 = Obstacle(10, 20, 5, 15)
o3 = Obstacle(35, 20, 5, 15)

start=(25, 40)
goal=(25, 10)

width = 50
height = 50

world = SpaceWorld(width, height, obstacles=[o1,o2,o3])
field = np.zeros((width,height))
for i in range(width):
  for j in range(height):
    if world.freeSpace(i,j,3):
      field[i, j] = Space.FREE.value

exploring = [start]
field[start] = Space.EXPLORED.value
parents = [[None for i in range(width)] for j in range(height)]
count = 0

def exploreCell(x, y, parent):
  if field[x][y] == Space.FREE.value:
    field[x][y] = Space.EXPLORED.value
    exploring.append((x,y))
    parents[x][y] = parent

def getParent(p):
  (x,y) = p
  return parents[x][y]

while len(exploring) > 0 and count < 2000:
  (x, y) = exploring.pop(0)
  if (x,y) == goal:
    break
  exploreCell(x+1, y, (x,y))
  exploreCell(x-1, y, (x,y))
  exploreCell(x, y+1, (x,y))
  exploreCell(x, y-1, (x,y))
  count += 1

current = goal
while current is not None:
  (x, y) = current
  field[x][y] = Space.PATH.value
  current = getParent(current)

field[start] = Space.START.value
field[goal] = Space.GOAL.value

world.setBackground(field)
world.showScene()