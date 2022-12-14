from .interpolation import interpolation
import math
import numpy as np

bi = interpolation()


class Geometric:
    def __init__(self):
        pass

    def forward_rotate(self, image, theta):
        """Computes the forward rotated image by an angle theta
                image: input image
                theta: angle to rotate the image by (in radians)
                return the rotated image"""
        x_max, y_max, x_min, y_min = self.compute_min_max(theta, image)
        forward_rotated_image = np.zeros((math.ceil(x_max - x_min), math.ceil(y_max - y_min)), dtype=int)
        rows = forward_rotated_image.shape[0]
        cols = forward_rotated_image.shape[1]
        for i in range(rows):
            for j in range(cols):
                x = int((i * math.cos(theta) - j * math.sin(theta)))
                y = int((i * math.sin(theta) + j * math.cos(theta)))
                if image.shape[0] > i >= 0 and image.shape[1] > j >= 0:
                    x -= x_min
                    y -= y_min
                    forward_rotated_image[int(x)][int(y)] = image[i][j]
        return forward_rotated_image

    def reverse_rotation(self, rotated_image, theta, origin, original_shape):
        """Computes the reverse rotated image by an angle theta
                rotated_image: the rotated image from previous step
                theta: angle to rotate the image by (in radians)
                Origin: origin of the original image with respect to the rotated image
                Original shape: Shape of the orginal image
                return the original image"""
        new_image = np.zeros((original_shape[0], original_shape[1]), dtype=int)
        for i in range(rotated_image.shape[0]):
            for j in range(rotated_image.shape[1]):
                a = i - origin[0]
                b = j - origin[1]
                a_ = int((a * math.cos(theta)) + (b * math.sin(theta)))
                b_ = int((-a * math.sin(theta)) + (b * math.cos(theta)))

                if new_image.shape[0] > a_ >= 0 and new_image.shape[1] > b_ >= 0:
                    new_image[a_][b_] = rotated_image[i][j]
        return new_image

    def rotate(self, image, theta, interpolation_type):
        """Computes the rotated image by an angle theta and perfrom interpolation
                image: the input image
                theta: angle to rotate the image by (in radians)
                interpolation_type: type of interpolation to use (nearest_neighbor, bilinear)
                return the rotated image"""
        x_max, y_max, x_min, y_min = self.compute_min_max(theta, image)
        new_image = np.zeros((math.ceil(x_max - x_min), math.ceil(y_max - y_min)), dtype=int)
        origin = (-x_min, -y_min)
        rows = new_image.shape[0]
        cols = new_image.shape[1]
        for i in range(rows):
            i_ = i - origin[0]
            for j in range(cols):
                j_ = j - origin[1]
                i__ = math.ceil((i_ * math.cos(theta)) + (j_ * math.sin(theta)))
                j__ = math.ceil((j_ * math.cos(theta)) - (i_ * math.sin(theta)))
                if image.shape[0] > round(i__) >= 0 and image.shape[1] > round(j__) >= 0:
                    if interpolation_type == 'nearest_neighbor':
                        new_image[i][j] = image[round(i__)][round(j__)]
                    elif interpolation_type == 'bilinear':
                        i1 = math.floor(i__)
                        j1 = math.floor(j__)
                        i2 = i1 + 1
                        j2 = j1 + 1
                        a = round(i__)
                        b = round(j__)
                        c = image.shape[0]
                        d = image.shape[1]
                        if 0 <= a < image.shape[0] and 0 <= b < image.shape[1] and i1 < \
                                image.shape[0] and i2 < c and j1 < d and j2 < image.shape[1]:
                            new_image[i][j] = bi.bilinear_interpolation([i1, j1], [i1, j2], [i2, j1], [i2, j2],
                                                                        [i__, j__], image)
        return new_image

    def compute_min_max(self, theta, image):
        x_min, x_max, y_min, y_max = 0, 0, 0, 0
        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                x = i * math.cos(theta) - j * math.sin(theta)
                if x <= x_min:
                    x_min = x
                if x > x_max:
                    x_max = x
                y = i * math.sin(theta) + j * math.cos(theta)
                if y <= y_min:
                    y_min = y
                if y > y_max:
                    y_max = y
        return x_max, y_max, x_min, y_min
