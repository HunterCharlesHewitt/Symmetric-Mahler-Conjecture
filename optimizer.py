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

