import numpy as np
import cv2 as cv2


class CellCounting:
    def __init__(self):
        pass

    def blob_coloring(self, image):
        """Implement the blob coloring algorithm
        takes a input:
        image: binary image
        return: a list/dict of regions"""

        image1 = np.zeros((image.shape[0], image.shape[1]), np.uint8)

        regions = dict()

        r = 1

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):

                if image[i, j] == 255 and image[i, j - 1] == 0 and image[i - 1, j] == 0:
                    image1[i, j] = r

                    r += 1

                if image[i, j] == 255 and image[i, j - 1] == 0 and image[i - 1, j] == 255:
                    image1[i, j] = image1[i-1, j]

                if image[i, j] == 255 and image[i, j - 1] == 255 and image[i - 1, j] == 0:
                    image1[i, j] = image1[i, j-1]

                if image[i, j] == 255 and image[i, j - 1] == 255 and image[i - 1, j] == 255:
                    image1[i, j] = image1[i - 1, j]
                    if image1[i, j - 1] != image1[i - 1, j]:
                        image1[i, j - 1] = image1[i - 1, j]

        for i in range(0, image1.shape[0]):
            for j in range(0, image1.shape[1]):
                if image1[i, j] in regions.keys():
                    regions[image1[i, j]].append([i, j])
                else:
                    regions[image1[i, j]] = [[i, j]]

        return regions

    def compute_statistics(self, region):
        """Compute cell statistics area and location
        takes as input
        region: a list/dict of pixels in a region
        returns: region statistics"""

        for key, value in list(region.items()):
            if len(value) < 15:
                region.pop(key)

        stats = dict()
        for key, value in list(region.items()):
            x_center = 0
            y_center = 0

            for i in range(len(value)):
                x_center = x_center + value[i][0]
                y_center = y_center + value[i][1]

            area = len(value)
            x_center = x_center / len(value)
            y_center = y_center / len(value)
            center = (int(x_center), int(y_center))
            stats[key] = []
            stats[key].append(center)
            stats[key].append(area)

        k = 1

        for key, value in stats.items():
            print("Region:", k, "Centroid:", value[0], "Area: ", value[1])
            k += 1

        return stats

    def mark_image_regions(self, image, stats):
        """Creates a new image with computed stats
        Make a copy of the image on which you can write text.
        takes as input
        image: a list/dict of pixels in a region
        stats: stats regarding location and area
        returns: image marked with center and area"""

        comp_image = image.copy()

        k = 1

        for key, value in list(stats.items()):
            center = value[0]
            area = value[1]
            cv2.putText(comp_image, '.' + str(k) + ',' + str(area), (center[1], center[0]), cv2.FONT_HERSHEY_DUPLEX, 0.3, 70)
            k += 1

        return comp_image
