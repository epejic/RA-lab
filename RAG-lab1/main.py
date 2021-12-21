import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math

from pyglet.gl import glTranslatef

import objLoad as graphics
import numpy as np

# periodic segment of Cube Spline curve
bSplineBMatrix = np.matrix([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
bSplineBMatrixTang = np.matrix([[-1, 3, -3, 1], [2, -4, 2, 0], [-1, 0, 1, 0]])
bSplineTangGlobalIterator = 0  # used for iterating over tangents


class objItem(object):

    def __init__(self):
        self.angle = 0
        self.vertices = []
        self.faces = []
        self.coordinates = [0, 0, -65]  # [x,y,z]
        self.position = [0, 0, -50]
        self.teddy = graphics.ObjLoader(
            "C:\\Users\\emanuel.pejic\\Documents\\FER\\Racunalna grafika\\1.lab\\0036506428A\\data\\teddy.obj", 0)
        f = open(
            "C:\\Users\\emanuel.pejic\\Documents\\FER\\Racunalna grafika\\1.lab\\0036506428A\\data\\"
            "settings-spline.txt", "r")

        bSplineVert = []  # Bspline curve vertices, pulled from settings-bspline.txt
        bSplineIterPoints = []  # Bspline curve points, got after iterating 0<i<1 for every segment
        bSplineIterTang = []  # Bspline curve tangents

        # get vertices from settings file
        for line in f:
            xyz = line.split(" ")
            xyz.pop()  # remove "("
            xyz.pop(0)  # remove ")\n"
            xyz = [float(iterator) for iterator in xyz]
            bSplineVert.append(xyz)

        # find all points on the curve and tangents in those points
        for i in range(1, np.shape(bSplineVert)[0] - 2):
            for t in np.arange(0, 1, 0.1):
                # get points
                tMatrix = np.mat([pow(t, 3), pow(t, 2), pow(t, 1), 1])
                rMatrix = np.mat([bSplineVert[i - 1], bSplineVert[i], bSplineVert[i + 1], bSplineVert[i + 2]])
                p = np.matmul(tMatrix, bSplineBMatrix)
                p = 1 / 6 * np.matmul(p, rMatrix)
                bSplineIterPoints.append(p)

                # get tangents
                tMatrix = np.mat([pow(t, 2), pow(t, 1), 1])
                p = np.matmul(tMatrix, bSplineBMatrixTang)
                p = 1 / 2 * np.matmul(p, rMatrix)
                bSplineIterTang.append(p)

        self.bSpline = graphics.ObjLoader(bSplineIterPoints, 1)
        self.tangents = graphics.ObjLoader([bSplineIterTang, bSplineIterPoints], 2)

    def render_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0.902, 0.902, 1, 0.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 0, math.sin(math.radians(self.angle)), 0, math.cos(math.radians(self.angle)) * -1, 0, 1, 0)
        glTranslatef(self.coordinates[0], self.coordinates[1], self.coordinates[2])

    # key bindings
    def move_forward(self):
        self.coordinates[2] += 10 * math.cos(math.radians(self.angle))
        self.coordinates[0] -= 10 * math.sin(math.radians(self.angle))

    def move_back(self):
        self.coordinates[2] -= 10 * math.cos(math.radians(self.angle))
        self.coordinates[0] += 10 * math.sin(math.radians(self.angle))

    def move_left(self, n):
        self.coordinates[0] += n * math.cos(math.radians(self.angle))
        self.coordinates[2] += n * math.sin(math.radians(self.angle))

    def move_right(self, n):
        self.coordinates[0] -= n * math.cos(math.radians(self.angle))
        self.coordinates[2] -= n * math.sin(math.radians(self.angle))

    # rotate camera
    def rotate(self, n):
        self.angle += n

    def doFunkyStuff(self):

        xMoveAcc = self.tangents.vertices[0][0, 0]  # initial x-translation, used to store accumulated x translation
        yMoveAcc = self.tangents.vertices[0][0, 1]  # initial y-translation, used to store accumulated y translation
        zMoveAcc = self.tangents.vertices[0][0, 2]  # initial z-translation, used to store accumulated z translation

        for i in range(0, np.shape(self.tangents.tangents)[0] - 1):  # take two vertices at a time
            # add the difference between next two points to accumulated translation
            xMoveAcc += self.tangents.vertices[i + 1][0, 0] - self.tangents.vertices[i][0, 0]
            yMoveAcc += self.tangents.vertices[i + 1][0, 1] - self.tangents.vertices[i][0, 1]
            zMoveAcc += self.tangents.vertices[i + 1][0, 2] - self.tangents.vertices[i][0, 2]
            # vector for startOrientation
            s = np.mat([0, 0, 1])  # start vector has to be same every time, because glRotate doesnt update points
            # vector for endOrientation
            e = self.tangents.tangents[i]
            os = np.mat([(s[0, 1] * e[0, 2] - e[0, 1] * s[0, 2]), (-(s[0, 0] * e[0, 2] - e[0, 0] * s[0, 2])),
                         (s[0, 0] * e[0, 1] - s[0, 1] * e[0, 0])])  # calculate rotation axis
            # rotation angle in rad
            fi = math.acos(np.matmul(s, np.transpose(e)) / (np.linalg.norm(s) * np.linalg.norm(e)))
            # rotation angle in degrees
            fi = np.degrees(fi)
            self.render_scene()
            glPushMatrix()
            glTranslatef(xMoveAcc, yMoveAcc, zMoveAcc)
            glRotatef(fi, os[0, 0], os[0, 1], os[0, 2])
            self.teddy.render_scene()
            glPopMatrix()
            self.bSpline.render_scene()
            self.tangents.render_scene()
            pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_mode((640, 480), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("RAG-lab1")
    clock = pygame.time.Clock()
    # Feature checker
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glEnable(GL_CULL_FACE)
    #
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, float(800) / 600, .0001, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    mainObj = objItem()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    mainObj.move_left(4)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    mainObj.move_right(4)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    mainObj.move_forward()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    mainObj.move_back()
                elif event.key == pygame.K_1:
                    mainObj.rotate(4)
                    mainObj.move_left(4)
                elif event.key == pygame.K_2:
                    mainObj.rotate(-4)
                    mainObj.move_right(4)
                elif event.key == pygame.K_3:
                    mainObj.doFunkyStuff()
        mainObj.render_scene()
        mainObj.bSpline.render_scene()
        mainObj.tangents.render_scene()
        mainObj.teddy.render_scene()
        pygame.display.flip()
        clock.tick(3)
    pygame.quit()


if __name__ == '__main__':
    main()
