import math

import numpy as np

from Models.Polytope import Polytope


def get_K_T_from_hiam_ostrover_counterexample():
    k_vectors = np.array(
        [[math.sin(2 * math.pi * i / 5), -math.cos(2 * math.pi * i / 5)] for i in range((-5) // 2, 5 // 2)])
    t_vectors = np.array(
        [[1.00000000e+00, 7.26542528e-01], [-3.81966011e-01, 1.17557050e+00], [-1.23606798e+00, 1.16735757e-16],
         [-3.81966011e-01, -1.17557050e+00], [1.00000000e+00, -7.26542528e-01]])
    K = Polytope(normal_vectors=k_vectors, dim=2)
    T = Polytope(normal_vectors=t_vectors, dim=2)
    return K, T


def get_vol_from_hiam_ostrover_counterexample():
    return 5.653178


def get_capacity_from_hiam_ostrover_counterexample():
    return 3.4409548

def get_ratio_from_hiam_ostrover_counterexample():
    return 2.0944271
