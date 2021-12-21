from OpenGL.GL import *
import numpy as np


class ObjLoader(object):

    def __init__(self, filename, code):
        self.vertices = []
        self.faces = []
        self.tangents = []
        # used to differentiate object, curve and its tangents
        self.code = code
        ##
        if code == 0:  # argument is .obj path
            try:
                f = open(filename)
                for line in f:
                    if line[:2] == "v ":
                        index1 = line.find(" ") + 1
                        index2 = line.find(" ", index1 + 1)
                        index3 = line.find(" ", index2 + 1)

                        vertex = (float(line[index1:index2]), float(line[index2:index3]), float(line[index3:-1]))
                        vertex = (round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2))
                        self.vertices.append(vertex)

                    elif line[0] == "f":
                        string = line.replace("//", "/")
                        ##
                        i = string.find(" ") + 1
                        face = []
                        for item in range(string.count(" ")):
                            if string.find(" ", i) == -1:
                                face.append(string[i:-1])
                                break
                            face.append(string[i:string.find(" ", i)])
                            i = string.find(" ", i) + 1
                        ##
                        self.faces.append(tuple(face))

                f.close()
            except IOError:
                print(".obj file not found!")
        elif code == 1:  # argument is vertex list
            self.vertices = filename  # in this case fileName is bSpline vertices
        elif code == 2:  # argument is tuple [tangents, vertices]
            self.tangents = filename[0]
            self.vertices = filename[1]

    def render_scene(self):
        if self.code == 0:  # render .obj file
            if len(self.faces) > 0:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                glBegin(GL_TRIANGLES)
                for face in self.faces:
                    for f in face:
                        vertexDraw = self.vertices[int(f) - 1]
                        if int(f) % 3 == 1:
                            glColor4f(0.282, 0.239, 0.545, 0.35)
                        elif int(f) % 3 == 2:
                            glColor4f(0.729, 0.333, 0.827, 0.35)
                        else:
                            glColor4f(0.545, 0.000, 0.545, 0.35)
                        glVertex3fv(vertexDraw)
                glEnd()
                ##
        elif self.code == 1:  # render bSpline using its vertices
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glBegin(GL_LINES)
            for i in range(0, np.shape(self.vertices)[0] - 1):  # take two vertices at a time
                glVertex3f(self.vertices[i][0, 0], self.vertices[i][0, 1], self.vertices[i][0, 2])
                glVertex3f(self.vertices[i + 1][0, 0], self.vertices[i + 1][0, 1], self.vertices[i + 1][0, 2])
                # print(vertex)
            glEnd()
        elif self.code == 2:  # render tangents on bSpline
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glBegin(GL_LINES)
            tangentScalingCoeff = 0.5
            for i in range(0, np.shape(self.vertices)[0]):  # add tangent vector to each vertex
                glVertex3f(self.vertices[i][0, 0], self.vertices[i][0, 1], self.vertices[i][0, 2])
                glVertex3f(self.vertices[i][0, 0] + tangentScalingCoeff * (self.tangents[i][0, 0]),
                           self.vertices[i][0, 1] + tangentScalingCoeff * (self.tangents[i][0, 1]),
                           self.vertices[i][0, 2] + tangentScalingCoeff * (self.tangents[i][0, 2]))
            glEnd()
