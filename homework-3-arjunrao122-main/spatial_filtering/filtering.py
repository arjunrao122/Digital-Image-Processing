import math as m
import numpy as np


class Filtering:

    def __init__(self, image):
        self.image = image

    def get_gaussian_filter(self):
        """Initialzes/Computes and returns a 5X5 Gaussian filter"""

        gaussian_filter = np.zeros((5, 5))

        sigma = 1

        mid_x = mid_y = int(5 / 2)

        for i in range(5):
            for j in range(5):
                gaussian_filter[i, j] = (1 / (2 * m.pi * sigma ** 2)) * np.exp(
                    -((i - mid_x) ** 2 + (j - mid_y) ** 2) / (2 * sigma ** 2))

        return gaussian_filter

    def get_laplacian_filter(self):
        """Initialzes and returns a 3X3 Laplacian filter"""

        return np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])

    def filter(self, filter_name):
        """Perform filtering on the image using the specified filter, and returns a filtered image
            takes as input:
            filter_name: a string, specifying the type of filter to use ["gaussian", laplacian"]
            return type: a 2d numpy array
                """

        row, col = self.image.shape

        image_pad = np.zeros((row + 2, col + 2))
        for i in range(row):
            for j in range(col):
                image_pad[i + 1, j + 1] = self.image[i, j]

        if filter_name == "gaussian":
            filter = self.get_gaussian_filter()
        else:
            filter = self.get_laplacian_filter()

        kernel_copy = np.zeros((filter.shape[0], filter.shape[1]))
        for i in range(filter.shape[0]):
            for j in range(filter.shape[1]):
                kernel_copy[i, j] = filter[filter.shape[0] - i - 1, filter.shape[1] - j - 1]

        image_height = image_pad.shape[0]
        image_width = image_pad.shape[1]
        kernel_height = kernel_copy.shape[0]
        kernel_width = kernel_copy.shape[1]

        height = kernel_height // 2
        width = kernel_width // 2

        converted_image = np.zeros(image_pad.shape)

        for i in range(height, image_height - height):
            for j in range(width, image_width - width):
                sum1 = 0

                for u in range(kernel_height):
                    for v in range(kernel_width):
                        sum1 = sum1 + kernel_copy[u, v] * image_pad[i - height + u, j - width + v]
                converted_image[i, j] = sum1

        return converted_image

