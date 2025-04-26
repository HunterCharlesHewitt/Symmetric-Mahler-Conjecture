import math
import random
from itertools import combinations, permutations, product
import numpy as np
import cvxpy as cp

from volume import *
from orbit import *


#### FINDING THE BEST ORBIT:
def optimize_k_length(orbit, cones, T, K, verbose=False):
    # orbit = (E1..Em) is a list of convex sets which lie on the boundary of T and have codimention at least 1.
    # cones = (C1..Cm) is a list of vectors in K. 
    # T is the table and K defines the asymetric norm.

    # we want to minimize the length (wrt the norm defined by K) of an orbit containing
    # points x1..xm for each xi in Ei such that x{i+1}-xi lies in Ci.

    # a point v is said to be in the cone Ci if <v, Ci> >= <v, u> for all u in K.

    # For each Ei, E{i+1}, we need to find points xi, x{i+1} that minimize <x{i+1}-xi, Ci> 
    # such that x{i+1}-xi is in Ci.

    n = len(K[0])  # dimension of the space
    m = len(orbit)  # number of points in the orbit
    
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
    for i, (x, E) in enumerate(zip(xs, orbit)):
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
#####

#### FINDING THE BEST CONES
def maximize_one_segment(T, K, facet_1, facet_2, cone):
    n = len(K[0])  # dimension of the space
    
    # the point on facet_1
    x1 = cp.Variable(n)
    # the point on facet_2
    x2 = cp.Variable(n)

    # Objective: maximize the length of the segment from x1 to x2
    diff = x2 - x1
    objective = cp.Variable()
    constraints = []

    # we want to minimize objective, but objective has three restrictions
    # 0. The definition: Objective = diff @ cone
    constraints.append(diff @ cone == objective)

    # 1. x1 must lie on facet_1 and x2 must lie on facet_2
    for v in T:
        if any(np.array_equal(v, e) for e in facet_1):
            constraints.append(x1 @ v == 1)
        else:
            constraints.append(x1 @ v <= 1)
        if any(np.array_equal(v, e) for e in facet_2):
            constraints.append(x2 @ v == 1)
        else:
            constraints.append(x2 @ v <= 1)
    
    #2. diff must lie in cone 
    for k in K:
        constraints.append(diff @ cone >= diff @ k)
    
    prob = cp.Problem(cp.Maximize(objective), constraints)
    prob.solve()

    if prob.status == 'optimal':
        return objective.value
    else:
        return 0

def facets_equal(facet_1, facet_2):
    if len(facet_1) != len(facet_2):
        return False
    for i, u in enumerate(facet_1):
        if not np.array_equal(u, facet_2[i]):
            return False
    return True

def find_cones_for_facet_pair(facet_list, T, K):
    # returns a 2d array of lists of cones
    # the ith row and jth column is the list of cones that are between the ith and jth facet.
    rv = []
    for i in range(len(facet_list)):
        to_add = []
        for j in range(len(facet_list)):
            if i != j:
                cones = []
                for cone in K:
                    max_length = 1
                    try:
                        max_length = maximize_one_segment(T, K, facet_list[i], facet_list[j], cone)
                    except:
                        continue
                    epsilon = 1e-6
                    if max_length >= epsilon:
                        cones.append(cone)
                to_add.append(cones)
            else:
                to_add.append([])
        rv.append(to_add)
    return rv

def optimize_over_cones(orbit, T, K, facet_list, cones_for_facet_pair, lazyness=0):
    min_val = float('inf')
    min_cones = None

    possible_cones = []
    for i, cur_facet in enumerate(orbit):
        past_facet = orbit[(i-1)%len(orbit)]
        # find facet in facet_list
        cur_index = None
        past_index = None
        for j, facet_in_list in enumerate(facet_list):
            if facets_equal(cur_facet, facet_in_list):
                cur_index = j
            if facets_equal(past_facet, facet_in_list):
                past_index = j
        if cur_index is None or past_index is None:
            raise Exception("Facet not found in facet_list")    
        possible_cones.append(cones_for_facet_pair[past_index][cur_index])
    
    all_cones = list(product(*possible_cones))

    if not all_cones:
        raise Exception("Unimplemented. all_cones is empty. This might be due to repeating edges")

    for cones in all_cones:
        if random.random() > lazyness:
            val, _ = optimize_k_length(orbit, cones, T, K, verbose=False)
            if val < min_val:
                min_val = val
                min_cones = cones

    return min_val, min_cones
#####

#### FINDING ALL THE FACETS
def check_if_line_in_cone(V, epsilon=1e-6):
    # first compute the cone and dual cone generated by V
    # then return true if the interior of the dual cone is empty.
    V = np.array(V)
    k, n = V.shape

    y = cp.Variable(n)
    constraints = [V @ y >= epsilon]

    prob = cp.Problem(cp.Minimize(cp.norm(y)), constraints)
    prob.solve()

    return prob.status != cp.OPTIMAL

def check_valid_facet(facet, T, verbose=False):
    # return true iff there is some x in R^dim such that <x,v>=1 for all v in facet 
    # and <x,u> <= 1 for all u in T.
    dim = len(T[0])
    x = cp.Variable(dim)
    constraints = []
    for v in T:
        if any(np.array_equal(u, v) for u in facet):  # Check array equality for each element in facet
            constraints.append(x @ v == 1)
        else:
            constraints.append(x @ v <= 1)
    prob = cp.Problem(cp.Minimize(cp.norm(x)), constraints) # It does not matter what we minimize
    prob.solve()
    if verbose:
        print(prob.status)
        print(prob.status == cp.OPTIMAL)
    return prob.status == cp.OPTIMAL

def get_all_facets(T):
    # returns all facets of any number of dimetions of T.
    rv = []
    power_set_T = []
    for r in range(1, len(T)+1):
        power_set_T.extend(list(combinations(T, r)))
    for s in power_set_T:
        try:
            if check_valid_facet(s, T):
                rv.append(s)
        except:
            # it would bad if an error caused the program to overcredit a species.
            print("Error")
            print(T)
            rv.append(s)
    return rv

def orbit_supports(orbit, support_orbit):
    # We say an orbit D supports an orbit C if for every facet S in C there is a facet S' in D such that S \subseteq S'
    # each orbit is a list of np arrays of vectors of the same dimension.
    for S in orbit:
        facet_supported = False
        for S_prime in support_orbit:
            # Check if facet_in_orbit is a subset of facet_in_support_orbit
            if all(any(np.array_equal(vec1, vec2) for vec2 in S_prime) for vec1 in S):
                facet_supported = True
                break
        if not facet_supported:
            return False
    return True

def get_all_untranslatable_orbit(T):
    # returns all lists of 
    all_facets = get_all_facets(T)
    all_orbit = list(combinations(all_facets, len(T[0])+1))
    rv = []
    facets_included = []
    for orbit in all_orbit:
        # We only want to include orbits that are do not suport any other orbit in rv.
        # This is because adding an orbit that is supported by another will waste computation time.
        if any(orbit_supports(other_orbit, orbit) for other_orbit in rv):
            continue
        vects_in_orbit = []
        for facet in orbit:
            for v in facet:
                if not any(np.array_equal(v, u) for u in vects_in_orbit):
                    vects_in_orbit.append(v)
        if check_if_line_in_cone(vects_in_orbit): # if vects_in_orbit is a line but a subset of it is aswell, then it is ineficient to include it.
            # also append all permutations of orbit that fix the last element
            last_element = orbit[-1]
            for perm in permutations(orbit[:-1]):
                rv.append(perm + (last_element,)) # This is what generated the incorrect orbit.
            # check if we can add to facets_included
            for facet in orbit: # adding new facet to facets_included
                if all(not facets_equal(facet, included_facet) for included_facet in facets_included):
                    facets_included.append(facet)
    return rv, facets_included

def cube_capacilty_ratio(dim):
    if dim < 2 or dim > 8:
        raise Exception("Not implemented")
    # maybe this is right:
    # volumes = [16/2,32/3, 64/6, 128/15, 256/45, 1024/315, 512/315] # See OEIS A049606
    # return math.pow(4, dim)/volumes[dim-2]
    return math.factorial(dim)
#####

#### c_K(T)        
def c_K_T_(T, K, stop_num=None, return_lots = False):
    dim = len(T[0])
    vol = volume_k_metric(dim, K, T)
    if stop_num is None: # Should be the most efficient.
        # big brain trick to be lazy
        stop_num = cube_capacilty_ratio(dim)
        
    orbits, facet_list = get_all_untranslatable_orbit(T)
    cones_for_facet_pair = find_cones_for_facet_pair(facet_list, T, K)
    print(len(orbits))
    min_len = float('inf')
    min_orbit = None
    min_cones = None
    lazinesses_levels = [0.99, 0.95, 0.9, 0.8, 0]
    for laziness in lazinesses_levels:
        for i, orbit in enumerate(orbits):
            # print(f"Started orbit {i}, laziness {laziness}")
            # print(len(orbit))
            # for thing in orbit:
            #     print(len(thing))
            # print(orbit)
            val, cone = optimize_over_cones(orbit, T, K, facet_list, cones_for_facet_pair, laziness)
            if min_len > val:
                min_len = val
                min_orbit = orbit
                min_cones = cone
                if (math.pow(min_len, dim)/vol < stop_num):
                    if return_lots:
                        return min_len, min_orbit, min_cones
                    return min_len
    if return_lots:
        return min_len, min_orbit, min_cones
    return min_len
#####
