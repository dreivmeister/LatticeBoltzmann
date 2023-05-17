import numpy as np
from LBM_copy import LBM
from objects import Cube, Triangle, Cylinder

def split_tuple(tuple_str):
    return tuple_str[1:-1].split(',')
    


def parser(filename):
    inp_file = open(filename, 'r')
    inp_file_lines = inp_file.readlines()

    LBMSimulation = LBM()
    objects = []
    for inp_statement in inp_file_lines:
        inp_statement_split = inp_statement.split()

        for i, ele in enumerate(inp_statement_split):
            #remove comments
            if '#' in ele:
                inp_statement_split = inp_statement_split[:i]

        if inp_statement_split == []:
            continue
        #select keyword of current row
        print(inp_statement_split)
        keyword = inp_statement_split[0]

        #go over all possible keywords
        if keyword == 'SIZE':
            LBMSimulation.Nx = int(inp_statement_split[1])
            LBMSimulation.Ny = int(inp_statement_split[2])
        elif keyword == 'TIME':
            LBMSimulation.Nt = int(inp_statement_split[1])
        elif keyword == 'PLOTNTH':
            LBMSimulation.plotEveryNth = int(inp_statement_split[1])
        elif keyword == 'RHO0':
            LBMSimulation.rho0 = int(inp_statement_split[1])
        elif keyword == 'TAU':
            LBMSimulation.tau = float(inp_statement_split[1])
        elif keyword == 'FLOWDIR':
            LBMSimulation.flowDirection = int(inp_statement_split[1])
        elif keyword == 'PLOTTYPE':
            LBMSimulation.plotType = inp_statement_split[1]
        elif keyword == 'PLOTREALTIME':
            if inp_statement_split[1] == 'True':
                LBMSimulation.plotRealTime = True
            elif inp_statement_split[1] == 'False':
                LBMSimulation.plotRealTime = False
        elif keyword == 'FILENAME':
            LBMSimulation.fileName = inp_statement_split[1]
        elif keyword == 'CYLINDER':
            spl_tuple = split_tuple(inp_statement_split[2])
            X, Y = np.meshgrid(range(LBMSimulation.Nx), range(LBMSimulation.Ny))
            cyl = Cylinder(X, Y, int(inp_statement_split[1]), int(spl_tuple[0]), int(spl_tuple[1]))
            objects.append(cyl)
        elif keyword == 'TRIANGLE':
            spl_tuple1 = split_tuple(inp_statement_split[1])
            spl_tuple2 = split_tuple(inp_statement_split[2])
            spl_tuple3 = split_tuple(inp_statement_split[3])
            tri = Triangle(LBMSimulation.Ny, LBMSimulation.Nx, int(spl_tuple1[0]), int(spl_tuple1[1]), int(spl_tuple2[0]), int(spl_tuple2[1]), int(spl_tuple3[0]), int(spl_tuple3[1]))
            objects.append(tri)
        elif keyword == 'CUBE':
            spl_tuple1 = split_tuple(inp_statement_split[1])
            spl_tuple2 = split_tuple(inp_statement_split[2])
            cub = Cube(LBMSimulation.Ny, LBMSimulation.Nx, int(spl_tuple1[0]), int(spl_tuple1[1]), int(spl_tuple2[0]), int(spl_tuple2[1]))
            objects.append(cub)
        else:
            print(f'Not a valid keyword: {keyword}')

    LBMSimulation.objects = objects

    return LBMSimulation