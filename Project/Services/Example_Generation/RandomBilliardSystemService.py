import random
import numpy as np
from Project.Models.BilliardSystem import BilliardSystem
from Project.Models.Polytope import Polytope
from Project.Services.Calculation.CapacityService import is_line_in_cone
from Project.Services.Calculation.VolumeService import get_polar_dual


def get_random_billiard_system(t_sides, k_sides, dim, normalized=False):
    T = Polytope(normal_vectors=None, dim=dim)
    K = Polytope(normal_vectors=None, dim=dim)
    while T.normal_vectors is None or not is_line_in_cone(T.normal_vectors):
        T.normal_vectors = np.array([[random.random() * 2 - 1 for _ in range(dim)] for _ in range(t_sides)])
        if normalized:
            T.normal_vectors = T.normal_vectors / np.linalg.norm(T.normal_vectors, axis=1, keepdims=True)
    while K.normal_vectors is None or not is_line_in_cone(K.normal_vectors):
        K.normal_vectors = np.array([[random.random() * 2 - 1 for _ in range(dim)] for _ in range(k_sides)])
        if normalized:
            K.normal_vectors = K.normal_vectors / np.linalg.norm(K.normal_vectors, axis=1, keepdims=True)
    # Taking the dual or the dual of the dual to ensure there are no redundant facets
    # If normalized is true, we want the vertecies of T and the dual of K to be on the unit sphere, like in the Hiam-Ostrov counterexample
    T = get_polar_dual(T)
    K = get_polar_dual(K)
    return BilliardSystem(T=T, K=K)
