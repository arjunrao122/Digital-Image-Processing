# For this part of the assignment, please implement your own code for all computations,
# Do not use inbuilt functions like fft from either numpy, opencv or other libraries
import numpy as np
import math as m

class Dft:
    def __init__(self):
        pass

    def forward_transform(self, matrix):
        """Computes the forward Fourier transform of the input matrix
        takes as input:
        matrix: a 2d matrix
        returns a complex matrix representing fourier transform"""

        row, col = matrix.shape

        m1 = np.zeros((row, col), dtype=complex)

        for u in range(row):
            for v in range(col):
                for i in range(row):
                    for j in range(col):
                        n = np.exp(((-2 * m.pi * 1J) / 15) * (u * i + v * j))
                        m1[u, v] = m1[u, v] + matrix[i, j] * n

        return m1

    def inverse_transform(self, matrix):
        """Computes the inverse Fourier transform of the input matrix
        You can implement the inverse transform formula with or without the normalizing factor.
        Both formulas are accepted.
        takes as input:
        matrix: a 2d matrix (DFT) usually complex
        returns a complex matrix representing the inverse fourier transform"""

        row, col = matrix.shape

        m1 = np.zeros((row, col), dtype=complex)

        for u in range(row):
            for v in range(col):
                for i in range(row):
                    for j in range(col):
                        n = np.exp(((2 * m.pi * 1J) / 15) * (u * i + v * j))
                        m1[u, v] = m1[u, v] + matrix[i, j] * n

        return m1

    def magnitude(self, matrix):
        """Computes the magnitude of the input matrix (iDFT)
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing magnitude of the complex matrix"""

        row, col = matrix.shape

        m1 = np.zeros((row, col), dtype=float)

        for i in range(row):
            for j in range(col):
                m1[i, j] = (matrix[i, j].real ** 2 + matrix[i, j].imag ** 2) ** 0.5

        return m1
