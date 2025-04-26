import numpy as np


class Polytope:
    def __init__(self, normal_vectors, dim):
        self.normal_vectors = normal_vectors
        self.dim = dim

    def __eq__(self, other):
        if not isinstance(other, Polytope):
            return False
        if self.dim != other.dim:
            return False
        return np.allclose(
            self.normal_vectors,
            other.normal_vectors,
            atol=1e-5,
            rtol=0.0
        )