from matplotlib import pyplot as plt


class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.patch = plt.Rectangle((x, y), width, height, fc='k')

    def isOutside(self, x, y, r):
        return (x + r) < self.x or (x - r) > (self.x + self.width) or (y + r) < self.y or (y - r) > (self.y + self.height)
