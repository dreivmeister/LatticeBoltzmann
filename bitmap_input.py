from PIL import Image
import numpy as np
from objects import Custom_Shape
import matplotlib.pyplot as plt
from LBM_copy import LBM

def fill4_iterative(img, x, y, alteFarbe, neueFarbe):
    stack = []
    stack.append((x, y))
    while len(stack) > 0:
        x, y = stack.pop()
        if x < 0 or x >= img.shape[0] or y < 0 or y >= img.shape[1]:
            continue
        if img[x, y] == alteFarbe:
            img[x, y] = neueFarbe
            stack.append((x, y + 1))
            stack.append((x, y - 1))
            stack.append((x + 1, y))
            stack.append((x - 1, y))
    return img

def input_custom_shape(file_name, Ny=100, Nx=400):
    img = np.array(Image.open(file_name))
    img = img[:,:,0]

    #only 255 and 0
    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            if img[x,y] != 255 and img[x,y] != 0:
                img[x,y] = 0
    img = fill4_iterative(img, 0, 0, 255, 0)
    img_bool = img.astype(dtype=bool)
    return Custom_Shape(img_bool)



# plt.imshow(img_, interpolation='nearest')
# plt.show()

# unique, counts = np.unique(img_, return_counts=True)
# print(np.asarray((unique, counts)).T)


CS = input_custom_shape('fluegel.bmp')

Sim = LBM(objects=[CS])

Sim.run()