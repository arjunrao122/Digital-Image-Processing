import numpy as np


class Filtering:

    def __init__(self, image, filter_name, filter_size, var=None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler
        global_var: noise variance to be used in the Local noise reduction filter
        S_max: Maximum allowed size of the window that is used in adaptive median filter
        """

        self.image = image

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        if filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        self.filter_size = filter_size
        self.global_var = var
        self.S_max = 15

    def get_arithmetic_mean(self, roi):
        """Computes the arithmetic mean of the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the arithmetic mean value of the roi"""

        row, col = roi.shape

        sum1 = 0

        total = row * col

        for i in range(row):
            for j in range(col):
                sum1 = sum1 + roi[i, j]

        arithmetic_mean = sum1 / total

        return float(arithmetic_mean)

    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""

        row, col = roi.shape

        prod_1 = 1

        total = row * col

        for i in range(row):
            for j in range(col):
                prod_1 = prod_1 * roi[i, j]

        geometric_mean = prod_1 ** (1 / total)

        return float(geometric_mean)

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""

        row, col = roi.shape

        array = np.zeros((row * col))

        count = 0

        for i in range(row):
            for j in range(col):
                array[count] = roi[i, j]
                count = count + 1

        length = len(array)

        mean = sum(array) / length

        deviations = [(x - mean) ** 2 for x in array]

        lv = sum(deviations) / length

        g = roi[int(roi.shape[0] / 2), int(roi.shape[0] / 2)]

        if self.global_var is None:
            self.global_var = 100

        local_noise = g - (self.global_var / lv) * (g - mean)

        return local_noise

    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi"""

        row, col = roi.shape

        array = np.zeros((row * col))

        count = 0

        for i in range(row):
            for j in range(col):
                array[count] = roi[i, j]
                count += 1

        array = sorted(array)

        mid = len(array) // 2

        median = (array[mid] + array[~mid]) / 2

        return median

    def get_adaptive_median(self, roi, x, y):
        """Use this function to implment the adaptive median.
        It is left up to the student to define the input to this function and call it as needed. Feel free to create
        additional functions as needed.
        """

        row, col = roi.shape

        z_max = 0

        z_min = 255

        for i in range(row):
            for j in range(col):
                if roi[i, j] > z_max:
                    z_max = roi[i, j]

                if roi[i, j] < z_min:
                    z_min = roi[i, j]

        z_med = self.get_median(roi)

        S_max = self.S_max

        size = self.filter_size

        a1 = z_med - z_min

        a2 = z_med - z_max

        b1 = self.image[x, y] - z_min

        b2 = self.image[x, y] - z_max

        while size <= S_max:
            if a1 > 0 and a2 < 0:
                break
            else:
                size = size + 2

        if size > S_max:
            return z_med
        else:
            if b1 > 0 and b2 < 0:
                return self.image[x, y]
            else:
                return z_med

    def filtering(self):
        """performs filtering on an image containing gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernal and apply a mathematical
        operation for all the elements with in the kernel. For example, mean, median and etc.

        Steps:
        1. add the necesssary zero padding to the noisy image, that way we have sufficient values to perform the operati
        ons on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        2. Iterate through the image and every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        4. Save the results at (i,j) in the ouput image.
        5. return the output image

        Note: You can create extra functions as needed. For example if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """

        row, col = self.image.shape

        padded_image = np.zeros((row + (self.filter_size - 1), col + (self.filter_size - 1)))

        for i in range(row):
            for j in range(col):
                padded_image[i + (self.filter_size - 2), j + (self.filter_size - 2)] = self.image[i, j]

        filtered_image = np.zeros((self.image.shape[0], self.image.shape[1]))

        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                if self.filter == self.get_adaptive_median:
                    filtered_image[i, j] = self.filter(padded_image[i:i + self.filter_size, j:j + self.filter_size], i, j)
                else:
                    filtered_image[i, j] = self.filter(padded_image[i:i + self.filter_size, j:j + self.filter_size])

        return filtered_image
