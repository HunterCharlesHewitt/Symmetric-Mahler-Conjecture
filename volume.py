import typing
from math import gamma, pi
import numpy as np
from matplotlib.patches import Circle
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
import matplotlib.pyplot as plt

def find_polar_dual(dim, normal_vectors):
    halfspace_vectors = np.hstack((normal_vectors, np.ones((normal_vectors.shape[0], 1)) * -1))
    hs = HalfspaceIntersection(halfspace_vectors, np.zeros(dim))
    dual = hs.dual_equations
    # for each array in deul its last value should be -1, so we need to scale every entry in each row by -1/dual[-1]
    scaled_dual = np.array([[-row[i] / row[-1] for i in range(len(row)-1)] for row in dual])
    return scaled_dual

def find_polar_dual_volume(dim, normal_vectors):
    halfspace_vectors = np.hstack((normal_vectors, np.ones((normal_vectors.shape[0], 1)) * -1))
    hs = HalfspaceIntersection(halfspace_vectors, np.zeros(dim))
    return hs.dual_volume

def find_volume(dim, normal_vectors):
    polar_dual = find_polar_dual(dim,normal_vectors)
    return find_polar_dual_volume(dim,polar_dual)

def volume_k_metric(dim, K, T):
    return find_volume(dim, T)*find_polar_dual_volume(dim,K)



# print(find_polar_duel(n,find_polar_duel(n,vectors)))
# print(find_volume(n,vectors))
# print(find_polar_duel_volume(n,vectors))
