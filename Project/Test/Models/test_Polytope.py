import unittest

import numpy as np

from Project.Models.Polytope import Polytope


class TestPolytope(unittest.TestCase):
    def test_polytope_constructor_sets_values(self):
        # Setup
        normal_vectors = np.array([[-0.39275834, -0.21369186], [0.97887142, -0.7326133], [-0.2209859, 0.91339311]])
        dim = 2

        # Assert
        polytope = Polytope(normal_vectors=normal_vectors, dim=dim)

        # Execute
        self.assertEqual(polytope.dim, dim)
        self.assertEqual(polytope.normal_vectors.tolist(), normal_vectors.tolist())


if __name__ == '__main__':
    unittest.main()
