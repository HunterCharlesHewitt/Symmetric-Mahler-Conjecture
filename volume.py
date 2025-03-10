import typing
from math import gamma, pi
import numpy as np
from matplotlib.patches import Circle
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
import matplotlib.pyplot as plt

# not used
def inner_product(vector1, vector2):
    return sum(a*b for a,b in zip(vector1, vector2))

def find_polar_duel(dim, normal_vectors):
    halfspace_vectors = np.hstack((normal_vectors, np.ones((normal_vectors.shape[0], 1)) * -1))
    hs = HalfspaceIntersection(halfspace_vectors, np.zeros(dim))
    duel = hs.dual_equations
    # for each array in deul its last value should be -1, so we need to scale every entry in each row by -1/duel[-1]
    scaled_duel = np.array([[-row[i] / row[-1] for i in range(len(row)-1)] for row in duel])
    return scaled_duel

def find_polar_duel_volume(dim, normal_vectors):
    halfspace_vectors = np.hstack((normal_vectors, np.ones((normal_vectors.shape[0], 1)) * -1))
    hs = HalfspaceIntersection(halfspace_vectors, np.zeros(dim))
    return hs.dual_volume

def find_volume(dim, normal_vectors):
    polar_duel = find_polar_duel(dim,normal_vectors)
    return find_polar_duel_volume(dim,polar_duel)

# n = 2
# vectors = np.array([[2,0], [0,2], [-2,0], [0,-2]])


# print(find_polar_duel(n,find_polar_duel(n,vectors)))
# print(find_volume(n,vectors))
# print(find_polar_duel_volume(n,vectors))
