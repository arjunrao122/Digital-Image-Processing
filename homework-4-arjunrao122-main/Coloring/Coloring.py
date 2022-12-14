import math

import numpy as np


class Coloring:

    def intensity_slicing(self, image, n_slices):
        '''
       Convert greyscale image to color image using color slicing technique.
       takes as input:
       image: the grayscale input image
       n_slices: number of slices
        
       Steps:
 
        1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
        2. Randomly assign a color to each interval
        3. Create and output color image
        4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
 
       returns colored image
       '''

        row, col = image.shape

        size = int(256 / (n_slices + 1))

        count = 0

        colors = np.zeros((256, 3))

        for i in range(n_slices + 1):
            if i == n_slices:
                size = 256 - count

            colors[count:count + size, 0] = np.random.randint(256)

            colors[count:count + size, 1] = np.random.randint(256)

            colors[count:count + size, 2] = np.random.randint(256)

            count = count + size

        color_image = np.zeros((row, col, 3))

        for i in range(row):
            for j in range(col):
                color_image[i, j, 0] = colors[image[i, j], 0]

                color_image[i, j, 1] = colors[image[i, j], 1]

                color_image[i, j, 2] = colors[image[i, j], 2]

        return color_image

    def color_transformation(self, image, n_slices, theta):
        '''
        Convert greyscale image to color image using color transformation technique.
        takes as input:
        image:  grayscale input image
        colors: color array containing RGB values
        theta: (phase_red, phase,_green, phase_blue) a tuple with phase values for (r, g, b) 
        Steps:
  
         1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
         2. create red values for each slice using 255*sin(slice + theta[0])
            similarly create green and blue using 255*sin(slice + theta[1]), 255*sin(slice + theta[2])
         3. Create and output color image
         4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
  
        returns colored image
        '''

        row, col = image.shape

        size = int(256 / (n_slices + 1))

        count = 0

        colors = np.zeros((256, 3))

        for i in range(n_slices + 1):
            if i == n_slices:
                size = 256 - count

            center = count + (((count + size) - count) / 2)

            print(center)

            colors[count:count + size, 0] = 255 * math.sin(center + theta[0])

            colors[count:count + size, 1] = 255 * math.sin(center + theta[1])

            colors[count:count + size, 2] = 255 * math.sin(center + theta[2])

            count = count + size

        color_image = np.zeros((row, col, 3))

        for i in range(row):
            for j in range(col):
                color_image[i, j, 0] = colors[image[i, j], 0]

                color_image[i, j, 1] = colors[image[i, j], 1]

                color_image[i, j, 2] = colors[image[i, j], 2]

        return color_image
