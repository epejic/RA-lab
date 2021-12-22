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
maxParticleNumber = 30
angle = 0
limitSpeed = True

towardsMassCenter = True
matchSpeeds = True
avoidOtherBirds = True

towardsMassCenterCoef = 10
matchSpeedsCoef = 0.055
avoidOtherBirdsCoef = 2
initialParticleVCoef = 0.95

speedLimit = 0.006
avoidRadius = 1
centerOfMassRadius = 2


def idleFunction():
    global previousTime
    global avoidRadius
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

        avgVelocityX = 0
        avgVelocityY = 0
        for i in range(0, len(particles)):
            avgVelocityX += particles[i].vX
            avgVelocityY += particles[i].vY

        avgVelocityX /= len(particles)
        avgVelocityY /= len(particles)

        for i in range(0, len(particles)):
            speedVectorX = 0
            speedVectorY = 0
            if towardsMassCenter:
                if random.randint(0, 100) > 90:

                    massCenterX = 0
                    massCenterY = 0
                    massCounter = 0
                    for j in range(0, len(particles)):
                        dist = math.sqrt(
                            pow(particles[i].x - particles[j].x, 2) + pow(particles[i].y - particles[j].y, 2))
                        if dist < centerOfMassRadius:
                            massCenterX += particles[j].x
                            massCenterY += particles[j].y
                            massCounter += 1
                    if massCounter == 0:
                        massCounter = 1
                    massCenterX /= massCounter
                    massCenterY /= massCounter

                    # Calculate speed vector
                    speedVectorX = massCenterX - particles[i].x
                    speedVectorY = massCenterY - particles[i].y
                    # Normalise speed vector
                    speedVectorLen = math.sqrt(pow(speedVectorX, 2) + pow(speedVectorY, 2))
                    if speedVectorLen < 1E-3:
                        speedVectorLen = 1
                    speedVectorX /= speedVectorLen
                    speedVectorY /= speedVectorLen

            if not matchSpeeds:
                avgVelocityX = avgVelocityY = 0
            # make movement
            if avoidOtherBirds:
                avgXLoc = 0
                avgYLoc = 0
                locCounter = 0
                for j in range(0, len(particles)):
                    # exclude self from proximity calculations
                    if j == i:
                        continue
                    dist = math.sqrt(pow(particles[i].x - particles[j].x, 2) + pow(particles[i].y - particles[j].y, 2))
                    if dist < avoidRadius:
                        avgXLoc += particles[j].x
                        avgYLoc += particles[j].y
                        locCounter += 1
                if locCounter == 0:
                    locCounter = 1
                # normalise vector
                avgXLoc /= locCounter
                avgYLoc /= locCounter

                # calculate vector to go away from other birds
                avgXLoc = particles[i].x - avgXLoc
                avgYLoc = particles[i].y - avgYLoc
            else:
                avgXLoc = 0
                avgYLoc = 0

            particles[i].vX = particles[
                                  i].vX * initialParticleVCoef + speedVectorX * towardsMassCenterCoef + avgVelocityX * matchSpeedsCoef + avgXLoc * avoidOtherBirdsCoef
            particles[i].vY = particles[
                                  i].vY * initialParticleVCoef + speedVectorY * towardsMassCenterCoef + avgVelocityY * matchSpeedsCoef + avgYLoc * avoidOtherBirdsCoef

            vX = particles[i].vX * particles[i].speed
            vY = particles[i].vY * particles[i].speed

            if limitSpeed:
                norm = math.sqrt(pow(vX, 2) + pow(vY, 2))
                vX = vX / norm * speedLimit
                vY = vY / norm * speedLimit

            particles[i].x = particles[i].x + vX
            particles[i].y = particles[i].y + vY

            if particles[i].x > 0.95 or particles[i].x < -0.95:
                particles[i].vX *= -1

            if particles[i].y > 1 or particles[i].y < -1:
                particles[i].vY *= -1

            if particles[i].z > 1 or particles[i].z < -1:
                particles[i].vZ *= -1

        dispFunction()
        previousTime = currentTime


def drawParticle(particleToDraw):
    glColor3f(particleToDraw.R, particleToDraw.G, particleToDraw.B)
    glTranslatef(particleToDraw.x, particleToDraw.y, particleToDraw.z)
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


glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutInitWindowPosition(100, 100)
glutInit(sys.argv)

window = glutCreateWindow("RAG-lab3")
glutDisplayFunc(dispFunction)
glutIdleFunc(idleFunction)
texture = loadTexture("cestica.bmp", True)

glBlendFunc(GL_SRC_ALPHA, GL_ONE)
glEnable(GL_BLEND)

glEnable(GL_TEXTURE_2D)
glBindTexture(GL_TEXTURE_2D, texture)
glutMainLoop()
