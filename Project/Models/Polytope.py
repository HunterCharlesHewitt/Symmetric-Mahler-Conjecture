import numpy as np
from scipy.spatial import HalfspaceIntersection


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

    def get_sorted_vertices(self):
        half_spaces = np.array([np.append(vector, -1) for vector in self.normal_vectors])
        interior_point = np.array([0.0, 0.0])
        hs = HalfspaceIntersection(half_spaces, interior_point)
        vertices = hs.intersections
        return sorted(vertices, key=lambda v: np.arctan2(v[1] - interior_point[1], v[0] - interior_point[0]))

    def get_vertices_in_desmos_format(self):
        vertices = self.get_sorted_vertices()
        vertices_str = ""
        for v in vertices:
            vertices_str += "(" + str(v[0]) + "," + str(v[1]) + "), "
        return vertices_str + "(" + str(vertices[0][0]) + "," + str(vertices[0][1]) + ")"
