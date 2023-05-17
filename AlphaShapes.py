
from BezierCurves import Bezier_Curve
from objects import Polygon
import numpy as np
from Constr_DT import alpha_shape
import matplotlib.pyplot as plt



if __name__== "__main__":
    control_points_x = [100,150,180,39,50,100]
    control_points_y = [50,70,40,42,90,50]
    px, py = Bezier_Curve(control_points_x, control_points_y, num_curve_points=10, plot=False)
    Poly = Polygon(100, 400, px, py)
    

    points = np.array(list(zip(Poly.vertices_x,Poly.vertices_y)))

    # Constructing the input point data
    # np.random.seed(0)
    # x = 3.0 * np.random.rand(2000)
    # y = 2.0 * np.random.rand(2000) - 1.0
    # inside = (x ** 2 + y ** 2 > 1.0) & ((x - 3) ** 2 + y ** 2 > 1.0)
    # points = np.vstack([x[inside], y[inside]]).T
    # print(points)

    #Computing the alpha shape
    edges = alpha_shape(points, alpha=100.0, only_outer=False)
    # Plotting the output
    plt.figure()
    plt.axis('equal')
    plt.plot(points[:, 0], points[:, 1], '.')
    for i, j in edges:
        print(i,j)
        plt.plot(points[[i, j], 0], points[[i, j], 1])
    plt.show()