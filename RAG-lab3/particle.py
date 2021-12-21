import random


class Particle(object):
    def __init__(self, currentTime):
        # generate random position
        self.x = random.uniform(-1, 1)
        self.y = random.uniform(-1, 1)
        self.z = random.uniform(-1, 1)

        # calculate random direction vector
        self.vX = random.uniform(-1, 1)
        self.vY = random.uniform(-1, 1)
        self.vZ = random.uniform(-1, 1)

        # generate random color
        self.R = random.uniform(0, 1)
        self.G = random.uniform(0, 1)
        self.B = random.uniform(0, 1)

        # remember creation time in ms
        self.createTime = currentTime

        # set destruction time to be [5, 10] seconds after creation
        self.destroyTime = currentTime + random.uniform(500, 1000) * 1000

        # set size to 0.04
        self.initialSize = 0.04
        self.size = self.initialSize

        # set speed to 0.005
        self.speed = 0.005


class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
