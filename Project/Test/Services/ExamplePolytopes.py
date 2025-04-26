import math

import numpy as np

from Project.Models.BilliardSystem import BilliardSystem
from Project.Models.Capacity import Capacity
from Project.Models.Polytope import Polytope


def get_billiard_system_from_hiam_ostrover_counterexample():
    k_vectors = np.array(
        [[math.sin(2 * math.pi * i / 5), -math.cos(2 * math.pi * i / 5)] for i in range((-5) // 2, 5 // 2)])
    t_vectors = np.array(
        [[1.00000000e+00, 7.26542528e-01], [-3.81966011e-01, 1.17557050e+00], [-1.23606798e+00, 1.16735757e-16],
         [-3.81966011e-01, -1.17557050e+00], [1.00000000e+00, -7.26542528e-01]])
    K = Polytope(normal_vectors=k_vectors, dim=2)
    T = Polytope(normal_vectors=t_vectors, dim=2)
    bs = BilliardSystem(K=K, T=T)
    bs.volume_k_metric = 5.653178
    bs.capacity_k_of_t = Capacity(length=3.4409548, orbit=None, cones=None)
    bs.ratio = 2.0944271
    return bs
