class interpolation:

    def linear_interpolation(self, x1, x2, x, pt1, pt21, image):
        """Computes the linear interpolation value at some iD location x between two 1D points (Pt1 and Pt2).

        There are no arguments defined in the function definition on purpose. It is left upto the student to define any requierd arguments.
        Please change the signature of the function and add the arguments based on your implementation.

        The function ideally takes two 1D points Pt1 and Pt2, and their intensitites I(Pt1), I(Pt2).
        return the interpolated intensity value (I(x)) at location x """

        # Write your code for linear interpolation here
        return ((x2 - x) / (x2 - x1) * image[pt1[0]][pt1[1]]) + ((x - x1) / (x2 - x1)) * image[pt21[0]][pt21[1]]

    def bilinear_interpolation(self, pt1, pt12, pt21, pt2, original, image):
        """Computes the bilinear interpolation value at some 2D location x between four 2D points (Pt1, Pt2, Pt3, and Pt4).

        There are no arguments defined in the function definition on purpose. It is left upto the student to define any requierd arguments.
        Please change the signature of the function and add the arguments based on your implementation.

        The function ideally takes four 2D points Pt1, Pt2, Pt3, and Pt4, and their intensitites I(Pt1), I(Pt2), I(Pt3), and I(Pt4).
        return the interpolated intensity value (I(x)) at location x """

        # Write your code for bilinear interpolation here
        # Recall that bilinear interpolation performs linear interpolation three times
        # Please reuse or call linear interpolation method three times by passing the appropriate parameters to compute this task

        i1 = self.linear_interpolation(pt1[0], pt21[0], original[0], pt1, pt21, image)
        i2 = self.linear_interpolation(pt12[0], pt2[0], original[0], pt12, pt2, image)
        return ((((pt12[1] - original[1]) / (pt12[1] - pt21[1])) * i1) + (
                (original[1] - pt21[1]) / (pt12[1] - pt1[1]) * i2))
