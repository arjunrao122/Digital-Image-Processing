import numpy as np


class Rle:
    def __init__(self):
        pass

    def encode_image(self, binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        rle_code = []

        for i in range(binary_image.shape[0]):

            first = binary_image[i, 0]

            rle_code.append(str(binary_image[i, 0]))

            code = 0

            for j in range(binary_image.shape[1]):

                if binary_image[i, j] == first:
                    code += 1
                else:
                    rle_code.append(code)
                    code = 1
                    first = binary_image[i, j]

            rle_code.append(code)

        return rle_code  # replace zeros with rle_code

    def decode_image(self, rle_code, height, width):
        """
        Get original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """

        decode = []

        for i in range(len(rle_code)):

            if rle_code[i] == '255':
                a = 1

            elif rle_code[i] == '0':
                a = 0

            else:

                if a == 1:
                    for j in range(rle_code[i]):
                        decode.append(255)

                    a = 0

                else:

                    for j in range(rle_code[i]):
                        decode.append(0)

                    a = 1

        image1 = np.zeros((height, width), np.uint8)

        k = 0

        for i in range(height):
            for j in range(width):
                image1[i, j] = decode[k]
                k += 1
                if k == len(decode):
                    break

        return image1  # replace zeros with image reconstructed from rle_Code










