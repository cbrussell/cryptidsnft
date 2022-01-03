import numpy as np
from PIL import Image

# Define start and end colours and image height and width
def get_gradient(): 
    R = np.random.randint(0, 256)
    G = np.random.randint(0, 256)
    B = np.random.randint(0, 256)

    R1 = np.random.randint(0, 256)
    G1 = np.random.randint(0, 256)
    B1 = np.random.randint(0, 256)


    colourA=[R, G, B]
    colourB=[R1, G1, B1]
    h, w = 1100, 1100

    # Make output image
    gradient = np.zeros((h,w,3), np.uint8)

    # Fill R, G and B channels with linear gradient between two end colours
    gradient[:,:,0] = np.linspace(colourA[0], colourB[0], w, dtype=np.uint8)
    gradient[:,:,1] = np.linspace(colourA[1], colourB[1], w, dtype=np.uint8)
    gradient[:,:,2] = np.linspace(colourA[2], colourB[2], w, dtype=np.uint8)

    return gradient