#from input_parser import parser
from LBM_copy import LBM
from objects import Polygon
from BezierCurves import Bezier_Curve
from scipy.spatial import Delaunay, delaunay_plot_2d
import numpy as np
import matplotlib.pyplot as plt

if __name__== "__main__":
	control_points_x = [100,150,180,50,100]
	control_points_y = [50,70,40,90,50]
	px, py = Bezier_Curve(control_points_x, control_points_y, num_curve_points=10, plot=False)
	Poly = Polygon(100, 400, px, py)
	#Poly.plot_polygon()

	points = np.array(list(zip(Poly.vertices_x,Poly.vertices_y)))

	tri = Delaunay(points)
	lotris = points[tri.simplices]
	print(len(lotris))

	_ = delaunay_plot_2d(tri)
	#plt.plot(Poly.vertices_x, Poly.vertices_y, alpha=0.5)
	plt.show()


	# for triangle in lotris:
	# 	print(triangle)
	# 	plt.plot([triangle[0,0],triangle[1,0]], [triangle[0,1],triangle[1,1]], 'ro-')
	# 	plt.plot([triangle[0,0], triangle[2,0]], [triangle[0,1],triangle[2,1]], 'ro-')
	# 	plt.plot([triangle[1,0],triangle[2,0]], [triangle[1,1],triangle[2,1]], 'ro-')
	# plt.show()


	
	# Sim = LBM(objects=[Poly], plotRealTime=False, Nt=100)
	# Sim.run()


#Next Steps:
#Interactive plot

#IDEAS:
#-remove all lines which are outside the polygon
#