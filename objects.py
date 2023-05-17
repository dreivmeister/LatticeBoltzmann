import numpy as np
import matplotlib.pyplot as plt
class Object:
    def __init__(self) -> None:
        self.object = None
        self.boundary = None
    
    def getObject(self):
        return self.object
    
    def getBoundary(self):
        return self.boundary
    
    def setBoundary(self, boundary):
        self.boundary = boundary




class Cylinder(Object):
    def __init__(self, X, Y, radius, Px, Py) -> None:
        self.cylinder = ((X - Px)**2 + (Y - Py)**2 < (radius)**2)
        self.boundary = None

    def getObject(self):
        return self.cylinder


class Cube(Object):
    def __init__(self, Ny, Nx, BLx, BLy, TRx, TRy) -> None:
        self.cube = np.full((Ny, Nx), False)
        for y in range(Ny):
            for x in range(Nx):
                if (x > BLx) and (x < TRx) and (y > BLy) and (y < TRy):
                    self.cube[y,x] = True
        self.boundary = None
    
    def getObject(self):
        return self.cube
    
    
class Triangle(Object):
    def __init__(self, Ny, Nx, P1x, P1y, P2x, P2y, P3x, P3y) -> None:
        self.P1 = (P1x, P1y)
        self.P2 = (P2x, P2y)
        self.P3 = (P3x, P3y)
        self.triangle = np.full((Ny, Nx), False)
        for y in range(Ny):
            for x in range(Nx):
                if self.pointInTriangle((x,y)):
                    self.triangle[y,x] = True
        self.boundary = None
    
    def getObject(self):
        return self.triangle
    
    def sign(self, P1, P2, P3):
        return (P1[0]-P3[0])*(P2[1]-P3[1])-(P2[0]-P3[0])*(P1[1]-P3[1])
    
    def pointInTriangle(self, P):
        
        d1 = self.sign(P, self.P1, self.P2)
        d2 = self.sign(P, self.P2, self.P3)
        d3 = self.sign(P, self.P3, self.P1)

        has_neg = (d1<0) or (d2<0) or (d3<0)
        has_pos = (d1>0) or (d2>0) or (d3>0)

        return not (has_neg and has_pos)


class Polygon(Object):
    def __init__(self, Ny, Nx, vertices_x=[], vertices_y=[]) -> None:
        #list of the polygon-vertices
        self.vertices_x = vertices_x
        self.vertices_y = vertices_y

        self.vertices_x.append(self.vertices_x[0])
        self.vertices_y.append(self.vertices_y[0])
        

        self.num_points = len(self.vertices_x)
        self.polygon = np.full((Ny, Nx), False)

        for y in range(Ny):
            for x in range(Nx):
                if self.is_point_inside(x,y):   
                    self.polygon[y,x] = True

        self.boundary = None
        self.fitness = 0

    def getObject(self):
        return self.polygon

    def is_point_inside(self, Px, Py):
        n = self.num_points
        inside = False

        p1x,p1y = self.vertices_x[0], self.vertices_y[0]
        for i in range(n+1):
            p2x,p2y = self.vertices_x[i%n], self.vertices_y[i%n]
            if Py > min(p1y,p2y):
                if Py <= max(p1y,p2y):
                    if Px <= max(p1x,p2x):
                        if p1y != p2y:
                            xints = (Py-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or Px <= xints:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside

    def plot_polygon(self):
        plt.plot(self.vertices_x, self.vertices_y)
        plt.show()


class Custom_Shape(Object):
    def __init__(self, shape) -> None:
        self.shape = shape
        self.boundary = None
    
    def getObject(self):
        return self.shape