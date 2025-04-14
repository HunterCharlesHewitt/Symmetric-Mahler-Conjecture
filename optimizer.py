import math
import random

import numpy as np
import cvxpy as cp

from volume import *
from orbit import *

# def find_k_cones(dim, K):
#     K = np.array(K)
#     # K is a list of vectors. The cone is the polar dual to this list of vectors.
#     dual = find_polar_dual(dim, K)
#     # now we need to normalize the vectors in the dual, which we will do with numpy.
#     normalized_dual = np.array([row / np.linalg.norm(row) for row in dual])
#     return normalized_dual

def optimize_k_length(convexEs, cones, T, K, verbose=False):
    # convexEs = (E1..Em) is a list of convex sets which lie on the boundary of T and have codimention at least 1.
    # cones = (C1..Cm) is a list of vectors in K. 
    # T is the table and K defines the asymetric norm.

    # we want to minimize the length (wrt the norm defined by K) of an orbit containing
    # points x1..xm for each xi in Ei such that x{i+1}-xi lies in Ci.

    # a point v is said to be in the cone Ci if <v, Ci> >= <v, u> for all u in K.

    # For each Ei, E{i+1}, we need to find points xi, x{i+1} that minimize <x{i+1}-xi, Ci> 
    # such that x{i+1}-xi is in Ci.

    n = len(K[0])  # dimension of the space
    m = len(convexEs)  # number of points in the orbit
    
    # Create variables for each point in the orbit
    xs = [cp.Variable(n) for _ in range(m)]

    constraints = []
    
    # Objective: minimize the sum of K-lengths between consecutive points
    objective = 0
    for i in range(m):
        past_i = (i - 1) % m
        diff = xs[i] - xs[past_i]
        # For each vector k in K, we need diff·k ≤ t where t is the length
        t = cp.Variable()  # This represents the K-norm of the difference
        objective += t
        # Add constraints that ensure t bounds the K-norm
        for k in K:
            if verbose:
                print(f"This constraint is x{i} - x{(i-1)%m} @ {k} <= length")
            constraints.append(diff @ k <= t)
    
    # 1. Each point must lie in its corresponding convex set
    for i, (x, E) in enumerate(zip(xs, convexEs)):
        for v in T:
            if any(np.array_equal(v, e) for e in E):
                if verbose:
                    print(f"This constraint is x{i} @ {v} == 1")
                constraints.append(x @ v == 1)
            else:
                if verbose:
                    print(f"This constraint is x{i} @ {v} <= 1")
                constraints.append(x @ v <= 1)
    
    # 2. Each difference vector must lie in its corresponding cone
    for i in range(m):
        past_i = (i - 1) % m
        diff = xs[i] - xs[past_i]
        c = cones[i]
        # For each vector k in K, the projection onto c must be maximal
        for k in K:
            if verbose:
                print(f"This constraint is x{i} - x{(i-1)%m} @ {c} >= x{i} - x{(i-1)%m} @ {k}")
            constraints.append(diff @ c >= diff @ k)
    
    # Solve the optimization problem
    prob = cp.Problem(cp.Minimize(objective), constraints)
    result = prob.solve()

    if verbose:
        print(prob.status)
        print(result)

    if prob.status == 'optimal':
        # Extract the optimal points
        optimal_points = [x.value for x in xs]
        # Calculate the total length
        total_length = sum(K_length(optimal_points[i], optimal_points[(i+1)%m], K) 
                         for i in range(m))
        return total_length, optimal_points
    else:
        return float('inf'), None

def get_all_cones(K, m):
    # so a cone should be an array of m vectors.
    all_cones = []
    if(m==1):
        return [np.array([k]) for k in K]
    tail_cones = get_all_cones(K, m-1)
    for vector in K:
        for cone in tail_cones:
            to_add = np.array([vector])
            to_add = np.concatenate((to_add, cone))
            all_cones.append(to_add)
    return all_cones

def optimize_over_cones(convexEs, T, K, lazyness=0):
    k_len = len(K)
    m = len(convexEs)

    min_val = float('inf')
    min_cones = None

    print("started getting cones")
    all_cones = get_all_cones(K, m)
    print("finished getting cones")

    for cones in all_cones:
        if random.random() > lazyness:
            val, _ = optimize_k_length(convexEs, cones, T, K, verbose=False)
            if val < min_val:
                min_val = val
                min_cones = cones

    return min_val, min_cones


# # square example
# dim = 2
# # T is the square
# T = np.array([[1,0], [0,1], [-1,0], [0,-1]])
# # K is the polar duel of T 
# K = np.array([[1,1], [1,-1], [-1,1], [-1,-1]])
# # here m = 2. # in this case 2d array with only one item.
# Es = [np.array([[0,1]]), np.array([[0,-1]])]
# cones = [np.array([1,1]), np.array([-1,-1])]

# # Viterbo counter example
# dim=2
# sides = 5
# T_vertecies = np.array([[math.cos(2*math.pi*i/sides), math.sin(2*math.pi*i/sides)] for i in range(sides)])
# # Hiam and Ostrover could have been more clear about this, but it seems like the normal vectors that define K lie on the unit sphere (standard norm)
# # This is odd since the dual of the the vectrors defining T lie on the unit sphere. I belive this because they inner producted these unit vectors
# # with vectors in the boundary of the polytope T.
# K = np.array([[math.sin(2*math.pi*i/sides), -math.cos(2*math.pi*i/sides)] for i in range((-sides)//2, sides//2)])
# # K = find_polar_dual(dim, np.array([[math.sin(2*math.pi*i/sides), -math.cos(2*math.pi*i/sides)] for i in range((-sides)//2, sides//2)]))
# T = find_polar_dual(2, T_vertecies)
# # case 1
# # Es = [np.array([T[1]]), np.array([T[4]]), np.array([T[3]])]
# # cones = np.array([K[0], K[3], K[2]])
# # cones = np.array([K[1], K[4], K[3]])
# # case 2
# Es = [np.array([T[0]]), np.array([T[2]]), np.array([T[4]])]
# # cones = np.array([K[0], K[2], K[4]])
# # cones = np.array([K[1], K[3], K[4]])

# vol = volume_k_metric(dim, K, T)
# val, cones = optimize_over_cones(Es, T, K, lazyness=0)
# # val, xs = optimize_k_length(Es, cones, T, K, verbose=True)

# val, xs = optimize_k_length(Es, cones, T, K, verbose=True)

# print(vol)
# print(val)
# print(cones)

# print(xs)

# for k in K:
#     print("_____________________")
#     print(k)
#     print(inner_product(np.array([xs[2][i]-xs[1][i] for i in [0,1]]), k))

# print(sum([K_length(xs[(i-1)%3], xs[i], K) for i in range(3)]))

# ys = [np.array([-0.22252093, 0.97492791]), np.array([-0.22252093, -0.97492791]), np.array([-0.22252093, -0.97492791])]
# print(sum([K_length(ys[i], ys[(i-1)%3], K) for i in range(3)]))
# print(2*math.cos(math.pi/10)*(1+math.cos(math.pi/5)))

# print(math.pow(4,2)/8)
# print(math.pow(val,2)/vol)
