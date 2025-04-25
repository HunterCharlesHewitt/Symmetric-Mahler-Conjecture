import unittest

import numpy as np

from Models.BilliardSystem import BilliardSystem
from Models.Polytope import Polytope


class BilliardSystemTest(unittest.TestCase):
    def test_BilliardSystem_constructor_sets_values(self):
        # Setup
        dim = 2
        k_normal_vectors = np.array([[-0.39275834, -0.21369186], [0.97887142, -0.7326133], [-0.2209859, 0.91339311]])
        t_normal_vectors = np.array([[-0.70880303, 0.64350865], [0.31667143, -0.20694839], [-0.41566717, -0.62539306]])
        K = Polytope(normal_vectors=k_normal_vectors, dim=dim)
        T = Polytope(normal_vectors=t_normal_vectors, dim=dim)

        # Execute
        bs = BilliardSystem(K, T)

        # Assert
        self.assertEqual(bs.K, K)
        self.assertEqual(bs.T, T)
        self.assertEqual(bs.K.normal_vectors.tolist(), k_normal_vectors.tolist())
        self.assertEqual(bs.T.normal_vectors.tolist(), t_normal_vectors.tolist())
        self.assertEqual(bs.K.dim, K.dim)
        self.assertEqual(bs.T.dim, T.dim)


if __name__ == '__main__':
    unittest.main()
