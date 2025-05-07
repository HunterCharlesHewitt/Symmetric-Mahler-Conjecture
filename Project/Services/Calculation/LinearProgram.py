from abc import ABC, abstractmethod

import numpy as np

class LinearProgram(ABC):
    def __init__(self):
        # We want to mimimize c^T x subject to Ax <= b
        self.A = []
        self.b = []
        self.c = []

    @abstractmethod
    def solve(self):
        pass

    def combine(self, other):
        # creates the diagonal matrix
        # [self.A, 0]
        # [0, other.A]
        # and the vector
        # [self.b, other.b]
        
        # Convert to numpy arrays if they're not already
        A1 = np.array(self.A)
        A2 = np.array(other.A)
        
        # Get dimensions
        m1, n1 = A1.shape if len(A1) > 0 else (0, 0)
        m2, n2 = A2.shape if len(A2) > 0 else (0, 0)
        
        # Create the block diagonal matrix
        combined_A = np.zeros((m1 + m2, n1 + n2))
        if m1 > 0 and n1 > 0:
            combined_A[:m1, :n1] = A1
        if m2 > 0 and n2 > 0:
            combined_A[m1:, n1:] = A2
            
        self.A = combined_A
        self.b = np.concatenate((self.b, other.b))
        self.c = np.concatenate((self.c, other.c))




