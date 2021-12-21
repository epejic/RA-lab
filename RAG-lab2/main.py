import math
import time
import random
import particle
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pyglet.gl import glEnable, glBindTexture, glColor3f
from PIL import Image

ociste = particle.Point3D(0, 0, 0)
particles = []
previousTime = 0
maxParticleNumber = 80
angle = 0


def idleFunction():
    global previousTime
    # current time in ms
    currentTime = time.time() * 1000
    timePassed = currentTime - previousTime
    # update every 10 ms
    if timePassed > 10:
        # remove particles that need to die
        particlesLen = len(particles)
        i = 0
        while i < particlesLen:
            if particles[i].destroyTime <= currentTime:
                particles.remove(particles[i])
                particlesLen = particlesLen - 1
            else:
                i = i + 1
        # add random number of new particles
        particlesToCreate = random.randint(0, maxParticleNumber - len(particles))
        # add max number of new particles
        # particlesToCreate = maxParticleNumber - len(particles)
        for i in range(0, particlesToCreate):
            particles.append(particle.Particle(currentTime))

        for i in range(0, len(particles)):
            # rotate particles accordingly
            s = np.mat([0, 0, 1])  # start vector has to be same every time, because glRotate doesnt update points
            # vector for endOrientation
            e = np.mat([particles[i].x, particles[i].y, particles[i].z - 100])
            osRotacije = np.mat([(s[0, 1] * e[0, 2] - e[0, 1] * s[0, 2]), (-(s[0, 0] * e[0, 2] - e[0, 0] * s[0, 2])),
                                 (s[0, 0] * e[0, 1] - s[0, 1] * e[0, 0])])  # calculate rotation axis
            # rotation angle in rad
            fi = math.acos(np.matmul(s, np.transpose(e)) / (np.linalg.norm(s) * np.linalg.norm(e)))
            # rotation angle in degrees
            fi = np.degrees(fi)

            particles[i].angle = fi
            particles[i].rotVectX = osRotacije[0, 0]
            particles[i].rotVectY = osRotacije[0, 1]
            particles[i].rotVectZ = osRotacije[0, 2]

            # make random movement
            particles[i].x = particles[i].x + particles[i].vX * particles[i].speed
            particles[i].y = particles[i].y + particles[i].vY * particles[i].speed
            particles[i].z = particles[i].z + particles[i].vZ * particles[i].speed

            # norm = pow(pow(particles[i].x, 2.0) + pow(particles[i].y, 2.0) + pow(particles[i].z, 2.0), 0.5)
            # particles[i].x /= norm
            # particles[i].y /= norm
            # particles[i].z /= norm

            if particles[i].x > 0.95 or particles[i].x < -0.95:
                particles[i].vX *= -1

            if particles[i].y > 1 or particles[i].y < -1:
                particles[i].vY *= -1

            if particles[i].z > 1 or particles[i].z < -1:
                particles[i].vZ *= -1

            colorCoef = (particles[i].destroyTime - currentTime) / \
                        (particles[i].destroyTime - particles[i].createTime)
            # print(colorCoef)
            # particles get smaller as they die
            particles[i].size = particles[i].initialSize * colorCoef

            # change colour every 10th frame on avg
            if random.randint(0, 5) > 0:
                RedAddOn = particles[i].vX
                GreenAddOn = particles[i].vY
                BlueAddOn = particles[i].vZ

                # particles fade as they die
                particles[i].R = (particles[i].R + RedAddOn) * colorCoef
                particles[i].G = (particles[i].G + GreenAddOn) * colorCoef
                particles[i].B = (particles[i].B + BlueAddOn) * colorCoef

                if particles[i].R < 0.05:
                    particles[i].R = 0.2
                if particles[i].G < 0.05:
                    particles[i].G = 0.2
                if particles[i].B < 0.05:
                    particles[i].B = 0.2

                if False:
                    if particles[i].R < 0:
                        particles[i].R = 0
                    elif particles[i].R > 1:
                        particles[i].R = 1

                    if particles[i].G < 0:
                        particles[i].G = 0
                    elif particles[i].G > 1:
                        particles[i].G = 1

                    if particles[i].B < 0:
                        particles[i].B = 0
                    elif particles[i].B > 1:
                        particles[i].B = 1

        dispFunction()
        previousTime = currentTime


def drawParticle(particleToDraw):
    glColor3f(particleToDraw.R, particleToDraw.G, particleToDraw.B)
    glTranslatef(particleToDraw.x, particleToDraw.y, particleToDraw.z)
    glRotatef(particleToDraw.angle, particleToDraw.rotVectX, particleToDraw.rotVectY, particleToDraw.rotVectZ)
    glBegin(GL_QUADS)

    glTexCoord2d(0.0, 0.0)
    glVertex3f(-particleToDraw.size, -particleToDraw.size, 0.0)
    glTexCoord2d(1.0, 0.0)
    glVertex3f(-particleToDraw.size, particleToDraw.size, 0.0)
    glTexCoord2d(1.0, 1.0)
    glVertex3f(particleToDraw.size, particleToDraw.size, 0.0)
    glTexCoord2d(0.0, 1.0)
    glVertex3f(particleToDraw.size, -particleToDraw.size, 0.0)

    glEnd()
    glRotatef(-particleToDraw.angle, particleToDraw.rotVectX, particleToDraw.rotVectY, particleToDraw.rotVectZ)
    glTranslatef(-particleToDraw.x, -particleToDraw.y, -particleToDraw.z)


def drawParticles():
    for i in range(0, len(particles)):
        particleToDraw = particles[i]
        drawParticle(particleToDraw)


def dispFunction():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glLoadIdentity()
    gluLookAt(0, 0, 0, math.sin(math.radians(angle)), 0, math.cos(math.radians(angle)) * -1, 0, 1, 0)
    glTranslatef(ociste.x, ociste.y, -ociste.z)
    drawParticles()
    glutSwapBuffers()


def loadTexture(filename, wrap):
    if not os.path.exists(filename):
        raise ValueError("Texture file not found: " + filename)
    image = Image.open(filename)
    ix = image.size[0]
    iy = image.size[1]
    img_data = image.tobytes("raw", "RGBX", 0, -1)
    textureL = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureL)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    if wrap is True:
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    else:
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, ix, iy, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return textureL


def keyFunction(key, x, y):
    global angle
    if key == b'w':
        ociste.y = ociste.y - 0.1 + 0 * x + 0 * y
    elif key == b's':
        ociste.y = ociste.y + 0.1
    elif key == b'a':
        ociste.x = ociste.x + 0.1
    elif key == b'd':
        ociste.x = ociste.x - 0.1
    elif key == b'q':
        angle = angle - 4
    elif key == b'e':
        angle = angle + 4
    elif key == b'y':
        ociste.z = ociste.z + 0.1
    elif key == b'x':
        ociste.z = ociste.z - 0.1


def runAway(x, y):
    global particles
    for i in range(0, len(particles)):
        dist = pow(pow(particles[i].x - x, 2) + pow(particles[i].y - y, 2), 0.5)
        # print(dist)
        if dist < 0.5:
            particles[i].speed = 0.05
            particles[i].vX = particles[i].x - x
            particles[i].vY = particles[i].y - y
            particles[i].destroyTime = time.time() * 1000 + random.uniform(2, 3) * 1000


def stop(x, y):
    global particles
    for i in range(0, len(particles)):
        dist = pow(pow(particles[i].x - x, 2) + pow(particles[i].y - y, 2), 0.5)
        # print(dist)
        if dist < 0.5:
            particles[i].speed = 0
            particles[i].vX = particles[i].x - x
            particles[i].vY = particles[i].y - y


def mouseFunction(button, state, x, y):
    if button == 0:
        # mouse coordinates in the middle of the screen are 256, 256
        runAway(x / 256 - 1, -(y / 256 - 1))
    if button == 2:
        stop(x / 256 - 1, -(y / 256 - 1))


glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(512, 512)
glutInitWindowPosition(100, 100)
glutInit(sys.argv)

window = glutCreateWindow("RAG-lab2")
glutDisplayFunc(dispFunction)
glutKeyboardFunc(keyFunction)
glutMouseFunc(mouseFunction)
glutIdleFunc(idleFunction)
texture = loadTexture("cestica.bmp", True)

glBlendFunc(GL_SRC_ALPHA, GL_ONE)
glEnable(GL_BLEND)

glEnable(GL_TEXTURE_2D)
glBindTexture(GL_TEXTURE_2D, texture)
glutMainLoop()
