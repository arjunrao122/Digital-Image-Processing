import numpy as np
import cv2


class Operation:

    def __init__(self):
        pass

    def merge(self, image_left, image_right, column):
        """
        Merge image_left and image_right at column (column)
        
        image_left: the input image 1
        image_right: the input image 2
        column: column at which the images should be merged

        returns the merged image at column
        """

        # add your code here

        merged_image = np.zeros((350, 340), np.uint8)

        merged_image[0:350, 0:column] = image_left[0:350, 0:column]
        merged_image[0:350, column:340] = image_right[0:350, column:340]

        # Please do not change the structure
        return merged_image

    def intensity_scaling(self, input_image, column, alpha, beta):
        """
        Scale your image intensity.

        input_image: the input image
        column: image column at which left section ends
        alpha: left half scaling constant
        beta: right half scaling constant

        return: output_image
        """

        # add your code here
        scaled_image = np.zeros((350, 340), np.uint8)
        scaled_image[0:350, 0:column] = input_image[0:350, 0:column]*alpha
        scaled_image[0:350, column:340] = input_image[0:350, column:340]*beta

        # Please do not change the structure
        return scaled_image

    def centralize_pixel(self, input_image, column):
        """
        Centralize your pixels (do not use np.mean)

        input_image: the input image
        column: image column at which left section ends

        return: output_image
        """

        # add your code here

        avg_left = 0
        for row in range(350):
            for col in range(column):
                value = input_image[row, col]
                avg_left = avg_left + value
        avg_left = avg_left / (350 * column)

        avg_right = 0
        for row in range(350):
            for col in range(column, 340):
                value = input_image[row, col]
                avg_right = avg_right + value
        avg_right = avg_right / (350 * (340 - column))

        offset_left = 128 - avg_left
        offset_right = 128 - avg_right

        for row in range(350):
            for col in range(column):
                value = input_image[row, col]
                left = offset_left + value
                if left > 255:
                    left = 255
                if left < 0:
                    left = 0
                input_image[row, col] = int(left)

        for row in range(350):
            for col in range(column, 340):
                value = input_image[row, col]
                right = offset_right + value
                if right > 255:
                    right = 255
                if right < 0:
                    right = 0
                input_image[row, col] = int(right)

        return input_image   # Currently the input image is returned, please replace this with the centralized image
