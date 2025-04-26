import numpy as np
from scipy import optimize
import cvxpy as cp

# we want to find the minimum length (w.r.t. the K asymetric norm) orbit of a polytope T of no more than n+1 bounces such that 
# the cone of vectors normal to the faces of T which are hit by the orbit contains a line as a subset.

# okay, for a polytope T, we need to find the face sequence of all possible orbits of length n+1 or less.
# this sucks to do, so I will do something else first.

def inner_product(vector1, vector2):
    return sum(a*b for a,b in zip(vector1, vector2))

def K_norm(p, K): # I think this is correct
    return max(inner_product(p,v) for v in K)

def K_length(pi,pi_plus1, K):
    return K_norm(pi_plus1 - pi, K) # it is not trivial why this is correct, but it is. (I proved it on paper)

# This method does not work.

# # V is the list of faces hit by the orbit, and K is the norm.
# def find_min_orbit(V, T, K):
#     if(not check_if_line_in_cone(V)[0]):
#         print("This orbit can be translated into the interior of the polytope.")
#         return None
#     m = V.shape[0]
#     n = V.shape[1]
#     # this is a convex optimization problem, so we can use cvxpy to solve it.
#     # There are (n+1)*n parameters, each coorisponding to a component of a point in the orbit
#     # We define the parameters as x_ij for 1 <= i <= n+1 and 1 <= j <= n, we reffer to x_i as a point in R^n
#     # We want to minimize sum_i=1^n+1 K_length(x_i,x_i+1, K) + K_length(x_n+1, x_1, K)
#     # The constraints are:
#         # for each vector x_i, there is a vector v_j in V such that v_j . x_i = 1
#         # for each vector x_i, and for each vector v_1 . x_i <= 1, ... , v_m . x_i <= 1
    
#     #Define cvxpy-compatible versions of K_norm and K_length
#     def cvx_K_norm(p, K):
#         return cp.max(cp.hstack([p @ k_vec for k_vec in K]))    
#     def cvx_K_length(pi, pi_plus1, K):
#         return cvx_K_norm(pi_plus1 - pi, K)
    
#     # Define variables: n+1 points in R^n
#     X = [cp.Variable(n) for _ in range(n+1)]
    
#     # Define binary variables to track which faces each point lies on
#     is_on_face = [[cp.Variable(boolean=True) for _ in range(m)] for _ in range(n+1)]
    
#     # Define slack variables to allow V[j]·X[i] to be less than 1 when not on face
#     # slack[i][j] will be 0 when point i is on face j, and positive otherwise
#     slack = [[cp.Variable(nonneg=True) for _ in range(m)] for _ in range(n+1)]
    
#     # Define the objective: minimize the sum of K-lengths
#     total_length = 0
#     for i in range(n):
#         total_length += cvx_K_length(X[i], X[i+1], K)
    
#     # Add the length from last point back to first point
#     total_length += cvx_K_length(X[n], X[0], K)
    
#     # Constraints
#     constraints = []
    
#     epsilon = 1e-6  # Small tolerance for numerical stability

#     # For each point in the orbit
#     for i in range(n+1):
#         # For each face
#         for j in range(m):
#             # This part is somewhat wrong. Cursor.AI is not good at this.
    
#             constraints.append(slack[i][j] >= 0)
            
#             # Connect the dot product, binary variable, and slack variable
#             # V[j]·X[i] + slack[i][j] = 1
#             constraints.append(V[j] @ X[i] + slack[i][j] == 1)
            
#             # If is_on_face[i][j] is true, then slack[i][j] must be 0
#             # If is_on_face[i][j] is false, then slack[i][j] can be positive
#             # TODO: stop using big constant M
#             M = 1000
#             # when is_on_face[i][j] is 1, this constraint makes slack 0,
#             # otherwise, it makes slack <= M, which is doing almost nothing
#             constraints.append(slack[i][j] <= M * (1 - is_on_face[i][j]))
        
#         # Each point must lie on at least one face
#         constraints.append(cp.sum(is_on_face[i]) >= 1)
#         for j in range(len(T)):
#             constraints.append(T[j] @ X[i] <= 1)
    
#     # Ensure that each face is used at least once
#     for j in range(m):
#         constraints.append(cp.sum([is_on_face[i][j] for i in range(n+1)]) >= 1)
    


#     # Create and solve the problem
#     prob = cp.Problem(cp.Minimize(total_length), constraints)
    
#     try:
#         result = prob.solve(solver=cp.MOSEK)  # Or another appropriate solver
        
#         # Extract the optimal orbit
#         optimal_orbit = [x.value for x in X]
#         optimal_length = result
        
#         # For verification, print which faces each point lies on
#         for i in range(n+1):
#             faces_on = [j for j in range(m) if is_on_face[i][j].value > 0.5]
#             print(f"Point {i} lies on faces: {faces_on}")
#             for j in range(m):
#                 print(f"  Face {j}: V[j]·X[i] = {np.dot(V[j], X[i].value)}, slack = {slack[i][j].value}")
            
#         return optimal_orbit, optimal_length
#     except Exception as e:
#         print(f"Solver error: {e}")
#         print("The problem may be infeasible or the solver may have encountered numerical issues.")
#         return None
    

# print(find_min_orbit(np.array([[0,2], [0,-2]]), np.array([[2,0], [0,2], [-2, 0], [0, -2]]), np.array([[1,0], [0,1], [-1, 0], [0, -1]])))
