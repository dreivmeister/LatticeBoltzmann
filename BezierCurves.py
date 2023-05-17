import math
import matplotlib.pyplot as plt


def Bezier(curve_param, num_contr_p, cpx, cpy):
    curve_point = [0,0]
    n = num_contr_p-1

    for i in range(num_contr_p):
        B_i = 1
        for j in range(1, i+1):
            B_i *= (n-j+1)/j

        B_i *= math.pow(curve_param,i)*pow(1-curve_param, n-i)
        curve_point[0] += cpx[i] * B_i
        curve_point[1] += cpy[i] * B_i
    
    return curve_point


def Bezier_Curve(control_points_x, control_points_y, num_curve_points=10, plot=True):
    pointsx = []
    pointsy = []
    num_control_points = len(control_points_x)
    for i in range(num_curve_points):
        t = i / num_curve_points
        p = Bezier(t, num_control_points, control_points_x, control_points_y)
        pointsx.append(p[0])
        pointsy.append(p[1])

    if plot:
        plt.plot(control_points_x, control_points_y, 'o', color='black')
        plt.plot(pointsx, pointsy, 'o', color='red', alpha=0.1)
        plt.show()
        
    return pointsx, pointsy
