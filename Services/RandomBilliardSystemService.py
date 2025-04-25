import random
import numpy as np
from Models.BilliardSystem import BilliardSystem
from Models.Polytope import Polytope
from Services.CapacityService import is_line_in_cone


def get_random_billiard_system(t_sides, k_sides, dim):
    T = Polytope(normal_vectors=None, dim=dim)
    K = Polytope(normal_vectors=None, dim=dim)
    while T.normal_vectors is None or not is_line_in_cone(T.normal_vectors):
        T.normal_vectors = np.array([[random.random() * 2 - 1 for _ in range(dim)] for _ in range(t_sides)])
    while K.normal_vectors is None or not is_line_in_cone(K.normal_vectors):
        K.normal_vectors = np.array([[random.random() * 2 - 1 for _ in range(dim)] for _ in range(k_sides)])
    return BilliardSystem(T=T, K=K)
