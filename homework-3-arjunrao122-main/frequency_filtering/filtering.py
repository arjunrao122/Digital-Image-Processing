# For this part of the assignment, You can use inbuilt functions to compute the fourier transform
# You are welcome to use fft that are available in numpy and opencv

import numpy as np
import cv2


class Filtering:

    def __init__(self, image):
        """initializes the variables for frequency filtering on an input image
        takes as input:
        image: the input image
        """
        self.image = image
        self.mask = self.get_mask

    def get_mask(self, shape):
        """Computes a user-defined mask
        takes as input:
        shape: the shape of the mask to be generated
        rtype: a 2d numpy array with size of shape
        """

        mask = self.image.copy()

        mask = mask * 8

        k = 256
        c = 10

        for i in range(shape[0]):
            for j in range(shape[1]):
                if mask[i, j] > 95 and ((k - c > i or i > k + c) and (k - c > j or j > k + c)):
                    mask = cv2.circle(mask, (j, i), 8, 0, -1)

        return mask

    def post_process_image(self, image):
        """Post processing to display DFTs and IDFTs
        takes as input:
        image: the image obtained from the inverse fourier transform
        return an image with full contrast stretch
        -----------------------------------------------------
        You can perform post processing as needed. For example,
        1. You can perfrom log compression
        2. You can perfrom a full contrast stretch (fsimage)
        3. You can take negative (255 - fsimage)
        4. etc.
        """

        image1 = image.copy()

        row, col = image.shape

        a = np.min(image)
        b = np.max(image)

        k = 255 / (b - a)

        for i in range(row):
            for j in range(col):
                image1[i, j] = k * (image1[i, j] - a)

        return image1

    def filter(self):
        """Performs frequency filtering on an input image
        returns a filtered image, magnitude of frequency_filtering, magnitude of filtered frequency_filtering
        ----------------------------------------------------------
        You are allowed to use inbuilt functions to compute fft
        There are packages available in numpy as well as in opencv
        Steps:
        1. Compute the fft of the image
        2. shift the fft to center the low frequencies
        3. get the mask (write your code in functions provided above) the functions can be called by self.filter(shape)
        4. filter the image frequency based on the mask (Convolution theorem)
        5. compute the inverse shift
        6. compute the inverse fourier transform
        7. compute the magnitude
        8. You will need to do post processing on the magnitude and depending on the algorithm (use post_process_image to write this code)
        Note: You do not have to do zero padding as discussed in class, the inbuilt functions takes care of that
        filtered image, magnitude of frequency_filtering, magnitude of filtered frequency_filtering: Make sure all images being returned have grey scale full contrast stretch and dtype=uint8
        """

        image = self.image
        shape = np.shape(image)

        fft = np.fft.fft2(image)  # compute fft

        shift = np.fft.fftshift(fft)   # compute shift
        mag = np.log(np.abs(shift))
        dft = np.uint8(mag)

        filter1 = Filtering(dft)    # mask
        mask = filter1.get_mask(shape)

        filter1 = shift * mask

        inverse_shift = np.fft.ifftshift(filter1)    # compute inverse shift

        filtered_image = np.fft.ifft2(inverse_shift)    # inverse transform

        filtered_image = np.uint8(self.post_process_image(np.absolute(filtered_image)))

        """Note: You do not have to do zero padding as discussed in class, the inbuilt functions takes care of that
        filtered image, magnitude of DFT, magnitude of filtered DFT: Make sure all images being returned have grey scale full contrast stretch and dtype=uint8 
        """

        return [filtered_image, dft * 8, mask]
