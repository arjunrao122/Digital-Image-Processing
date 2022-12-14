class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        """Computes the histogram of the input image
        takes as input:
        image: a grey scale image
        returns a histogram as a list"""

        hist = [0]*256

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                number = image[i, j]
                hist[number] += 1

        return hist

    def find_otsu_threshold(self, hist):
        """analyses a histogram it to find the otsu's threshold assuming that the input hstogram is bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value (otsu's threshold)"""

        sum1 = total = 0

        for i in range(256):
            sum1 = sum1 + i*hist[i]
            total = total + hist[i]

        sum_b = w_b = variance_max = threshold = 0

        for i in range(256):

            w_b = w_b + hist[i]

            if w_b == 0:
                continue

            w_f = total - w_b

            if w_f == 0:
                break

            sum_b = sum_b + (i * hist[i])
            m_b = sum_b/w_b
            m_f = (sum1 - sum_b) / w_f

            variance_between = w_b * w_f * (m_b - m_f) * (m_b - m_f)

            if variance_between > variance_max:
                variance_max = variance_between
                threshold = i

        return threshold

    def binarize(self, image):
        """Comptues the binary image of the the input image based on histogram analysis and thresholding
        take as input
        image: an grey scale image
        returns: a binary image"""

        binary_image = image.copy()

        histogram = self.compute_histogram(binary_image)

        threshold = self.find_otsu_threshold(histogram)

        for i in range(binary_image.shape[0]):
            for j in range(binary_image.shape[1]):
                if binary_image[i, j] >= threshold:
                    binary_image[i, j] = 0
                else:
                    binary_image[i, j] = 255

        return binary_image
