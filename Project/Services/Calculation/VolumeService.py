import numpy as np
from scipy.spatial import HalfspaceIntersection
from Project.Models.Polytope import Polytope


def get_volume_k_metric(K, T):
    return get_volume(T) * get_polar_dual_volume(K)


def get_volume(polytope):
    polar_dual = get_polar_dual(polytope)
    return get_polar_dual_volume(polar_dual)


def get_polar_dual_volume(polar_dual):
    return get_half_space(polar_dual).dual_volume


def get_polar_dual(polytope):
    hs = get_half_space(polytope)
    scaled_dual = scale_dual_so_last_val_is_neg_1(hs.dual_equations)
    if polytope.dim == 2:
        angles = get_principal_angles(scaled_dual)
        sorted_indices = np.argsort(angles)
        scaled_dual = scaled_dual[sorted_indices]
    return Polytope(normal_vectors=scaled_dual, dim=polytope.dim)


def get_half_space(polytope):
    halfspace_vectors = np.hstack((polytope.normal_vectors, np.ones((polytope.normal_vectors.shape[0], 1)) * -1))
    return HalfspaceIntersection(halfspace_vectors, np.zeros(polytope.dim))


def get_principal_angles(scaled_dual):
    angles = np.arctan2(scaled_dual[:, 1], scaled_dual[:, 0])
    return np.where(angles < 0, angles + 2 * np.pi, angles)


def scale_dual_so_last_val_is_neg_1(dual):
    return np.array([[-row[i] / row[-1] for i in range(len(row) - 1)] for row in dual])
