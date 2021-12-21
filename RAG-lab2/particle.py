import random


class Particle(object):
    def __init__(self, currentTime):
        # generate random position
        self.x = random.uniform(-1, 1)
        self.y = random.uniform(-1, 1)
        self.z = random.uniform(-1, 1)

        # norm = pow(pow(self.x, 2.0) + pow(self.y, 2.0) + pow(self.z, 2.0), 0.5)
        # self.x /= norm
        # self.y /= norm
        # self.z /= norm

        # calculate random direction vector
        self.vX = random.uniform(-1, 1)
        self.vY = random.uniform(-1, 1)
        self.vZ = random.uniform(-1, 1)

        # norm = pow(pow(self.x, 2.0) + pow(self.y, 2.0) + pow(self.z, 2.0), 0.5)
        # self.vX /= norm
        # self.vY /= norm
        # self.vZ /= norm

        # generate random color
        self.R = random.uniform(0, 1)
        self.G = random.uniform(0, 1)
        self.B = random.uniform(0, 1)

        # remember creation time in ms
        self.createTime = currentTime

        # set destruction time to be [5, 10] seconds after creation
        self.destroyTime = currentTime + random.uniform(500, 1000) * 1000

        # generate random size in range [0.05, 0.3]
        self.initialSize = random.uniform(0.1, 0.5)
        self.size = self.initialSize

        # set speed in range [0, 1]
        self.speed = random.uniform(0, 0.0125)
        # self.speed = 0
        # set angle
        # self.angle = random.randint(0, 360)

        # set rotation Vector in range [-1, 1]
        self.rotVectX = random.uniform(-1, 1)
        self.rotVectY = random.uniform(-1, 1)
        self.rotVectZ = random.uniform(-1, 1)


class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
