import numpy as np
from volume import volume_k_metric
from orbit import K_norm


def does_billiard_conjecture_hold(K, T, dim):
    Q = get_unit_cube(dim)[0]
    vol_k_t = get_volume(dim=dim, K=K, T=T)
    vol_q_q = get_volume(dim=dim, K=Q, T=Q)
    return (capacity(K=K, T=T, dim=dim) ** 2 / vol_k_t) <= (capacity(K=Q, T=Q, dim=dim) ** (2 * dim) / vol_q_q)


def capacity(K, T, dim):
    """
    Computes C_K(T) defined as:

        C_K(T) = min_{m >= 1} min_{P in P_m(T)} ell_K(P)

    where ell_K(P) is the K-norm length of the closed polygon P.

    Parameters:
      - T: The convex body (geometric object) in the vector space V.
      - K: The dual unit ball which defines the norm ||.||_K.

    Returns:
        - min_length is the minimum length achieved.
    """

    best_length = float('inf')

    # Iterate over different numbers of vertices.
    for m in range(1, dim + 2):
        # Get all candidate tuples of points that do not fit into a shrunken copy of K.
        candidate_polygons = get_untranslatable_points(T=T, m=m)

        # Iterate over each candidate polygon P, where P is a tuple/list of m points.
        for P in candidate_polygons:
            # Initialize length of the closed polygon P.
            total_length = 0
            # Compute the length by summing norms of differences.
            # We use modulo arithmetic to close the polygon: q_{m+1} is q_1.
            for i in range(m):
                next_i = (i + 1) % m
                diff_vector = P[next_i] - P[i]
                total_length += K_norm(diff_vector, K)

            # Update best length and polygon if we found a shorter one.
            if total_length < best_length:
                best_length = total_length
                best_polygon = P
                print(best_length, best_polygon)

    return best_length


def get_volume(K, T, dim):
    return volume_k_metric(dim=dim, K=K, T=T)


#TODO just make into table
def get_unit_cube(dim):
    """
    Constructs the half-space (H-representation) of a unit cube in R^dim using normal vectors.

    The unit cube is defined as:
        { x in R^dim : 0 <= x_i <= 1 for i = 1,...,dim }

    It is represented as:
        { x in R^dim : A x <= b }
    where A is a (2*dim x dim) matrix and b is a (2*dim) vector.

    Returns:
        A (np.ndarray): The matrix of normal vectors, with shape (2*dim, dim).
        b (np.ndarray): The offset vector, with shape (2*dim,).
    """
    A = np.zeros((2 * dim, dim))
    b = np.zeros(2 * dim)

    # For each dimension i, create two inequalities:
    for i in range(dim):
        # Inequality: -x_i <= 0  (which represents x_i >= 0)
        A[i, i] = -1
        b[i] = 0

        # Inequality: x_i <= 1
        A[dim + i, i] = 1
        b[dim + i] = 1
    return A, b


#TODO implement
def get_untranslatable_points(T, m):
    return []
