import numpy as np

from Project.Services.Calculation.VolumeService import get_polar_dual
from Project.Services.Calculation.LengthService import K_length, max_K_vector
from Project.Models.PhaseSpace import *
from Project.Models.Capacity import Capacity
from Project.Models.Polytope import Polytope
from Project.Services.Output.TrajectoryVisualizerService import TrajectoryVisualizerService
from Project.Services.Calculation.GurobiSolver import gurobi_solver_simple

def get_trajectory_capacity(T, K):
    # T is the table K is the norm
    K_dual = get_polar_dual(K)

    dim = T.dim
    # These can be thought of as nodes.
    phase_spaces = generate_phase_spaces(T, K_dual)

    initial_phase_space_maps: list[PhaseSpaceMap] = generate_initial_phase_space_maps(phase_spaces)
    fix_T = False
    graded_phase_space_maps = [initial_phase_space_maps]
    for i in range((dim+1)*2):
        graded_phase_space_maps.append(expandend_phase_space_maps(graded_phase_space_maps[-1], T, K_dual, fix_T))
        fix_T = not fix_T
    
    phase_space_maps = []
    #TODO there is probably a simpler way to do the nested fors below, I will change later
    for maps_list in graded_phase_space_maps[1:]:
        for phase_space_map in maps_list:
            phase_space_maps.append(phase_space_map)

    min_length = float('inf')
    min_cone = None
    x = None
    for phase_space_map in phase_space_maps:
        if phase_space_map.is_endomorphism():
            solution = find_fixed_points(phase_space_map)
            if solution["any_solution"]:
                length = float('inf')
                if solution["is_unique"]:
                    x = solution["particular"]
                    # fix_T starts out as true, so we only want the even indexes in phase_space_map_list
                    t_phase_space_map_list = phase_space_map.phase_space_map_list[::2]
                    length = calculate_trajectory(T, K_dual, x, t_phase_space_map_list, visualize_trajectory=True)
                else:
                    A, b = get_lp_matrix(T, K_dual, phase_space_map, solution)
                    c, offset = get_lp_objective(K, phase_space_map, solution)
                    length, status, x = gurobi_solver_simple(A, b, c)
                    length += offset
                if length < min_length and length > 1e-6:
                    min_length = length
                    min_cone = phase_space_map.input_phase_space.k_vect_perp
    # TODO: I don't know if we should return all of this. x isn't really a trajectory, just a starting point.
    return Capacity(length=min_length, orbit=None, cones=min_cone, trajectory=x)

def in_polytope(x, T: Polytope):
    tolerance = 1e-7
    for vect in T.normal_vectors:
        # The check below fails because vdot gets an array with 'dtype=object'.
        # It's an array whose elements are other arrays, not numbers.
        # vdot can't do math on that, even if the shape seems right.
        if dot(x, np.matrix(vect).T) > 1+tolerance:
            return False
    return True

def find_fixed_points(phase_space_map: PhaseSpaceMap):
    # finds the fixed point in T.
    # x mapsto matrix @ x+shift
    # we want this in local coordinates
    # thus (matrix-I) @ x= -shift
    # or more simply, Ax = b
    phase_space_map.set_map_in_phase_space_coordinates()
    # dim is the dimention of the T-coordinates in the phase space. This is one less than the dimention of the polytope T.
    dim = phase_space_map.input_phase_space.phase_space_dim//2
    A_T = phase_space_map.phase_space_T_matrix-np.eye(dim)
    A_K = phase_space_map.phase_space_K_matrix-np.eye(dim)
    A = np.block([[A_T, np.zeros((dim, dim))], [np.zeros((dim, dim)), A_K]])
    b_T = -phase_space_map.phase_space_T_shift
    b_K = -phase_space_map.phase_space_K_shift
    b = np.concatenate([b_T, b_K], axis=0)
    
    # Flatten b for lstsq (expects shape (n,))
    tolerance = 1e-6
    b_flat = np.asarray(b).flatten()
    x_particular = np.matrix(np.linalg.lstsq(A, b_flat, rcond=None)[0]).T
    residual = np.linalg.norm(A @ x_particular - b)
    rv = {
        "particular": None,
        "any_solution": False,
        "is_unique": True,
        "t_nullspace": None,
        "k_nullspace": None
    }
    if residual > tolerance:
        return rv
    rv["particular"] = x_particular
    rv["any_solution"] = True
    rv["t_nullspace"] = np.matrix(null_space(A_T))
    rv["k_nullspace"] = np.matrix(null_space(A_K))
    null_dim_t = rv["t_nullspace"].shape[1]
    null_dim_k = rv["k_nullspace"].shape[1]
    if null_dim_t == 0 and null_dim_k == 0:
        # We don't need to think about the null spaces
        return rv
    rv["is_unique"] = False
    return rv

def calculate_trajectory(T, K_dual, x, t_phase_space_maps: list[PhaseSpaceMap], visualize_trajectory=False):
    length = 0
    prev_t, prev_k = t_phase_space_maps[0].input_phase_space.from_phase_space_coordinates(x)
    k_list = []
    t_list = []
    cur_t = prev_t
    cur_k = prev_k
    for phase_space_map in t_phase_space_maps:
        val = phase_space_map.map_x(x)
        cur_t, cur_k = phase_space_map.output_phase_space.from_phase_space_coordinates(val)
        if visualize_trajectory:
            k_list.append([cur_k.item((0, 0)), cur_k.item((1, 0))])
            t_list.append([cur_t.item((0, 0)), cur_t.item((1, 0))])
        if not in_polytope(cur_t, T) or dot(cur_t, phase_space_map.output_phase_space.t_vect_perp) < 1-1e-6:
            return float('inf')
        if not in_polytope(cur_k, K_dual) or dot(cur_k, phase_space_map.output_phase_space.k_vect_perp) < 1-1e-6:
            return float('inf')
        length += float(K_length(prev_t, cur_t, get_polar_dual(K_dual)))
        prev_t = cur_t
    if visualize_trajectory:
        vs = TrajectoryVisualizerService(T=T, K=K_dual, t_list=t_list, k_list=k_list)
        vs.visualize_trajectory()
    # if length < 1e-5:
    #     return float('inf')
    return length

def generate_phase_spaces(T, K_dual):
    # We are assuming that the particle is at T's facet and after bouncing traveling in the direction of K's facet.
    rv = []
    for t_vect_perp in T.normal_vectors:
        for k_vect_perp in K_dual.normal_vectors:
            # our assumption means that t_vect_perp and k_vect_perp disagree on direction
            if dot(t_vect_perp, k_vect_perp) < -1e-9:
                rv.append(PhaseSpace(t_vect_perp=np.matrix(t_vect_perp).T, k_vect_perp=np.matrix(k_vect_perp).T))
    return rv

def generate_initial_phase_space_maps(phace_spaces):
    rv = []
    for phase_space in phace_spaces:
        rv.append(PhaseSpaceMap(
            input_phase_space=phase_space,
            output_phase_space=phase_space,
            T_matrix=np.eye(phase_space.vect_dim),
            K_matrix=np.eye(phase_space.vect_dim),
            T_shift=np.zeros((phase_space.vect_dim, 1)),
            K_shift=np.zeros((phase_space.vect_dim, 1))
        ))
    return rv


def expandend_phase_space_maps(starting_maps, T, K_dual, fix_T):
    rv = []
    if(fix_T):
        for affine_map in starting_maps:
            # we will do the map map_id_x_phi_T AFTER affine_map
            for K_vect in map(lambda x: np.array([x]).T, K_dual.normal_vectors):
                cur_t_perp = affine_map.output_phase_space.t_vect_perp
                if dot(K_vect, cur_t_perp) < -1e-9: # making sure cur_t_perp is not in same direction as K_vect
                    rv.append(affine_map.left_compose(affine_map.output_phase_space.map_id_x_phi_T(new_K_normal_vect=K_vect)))
    else:
        for affine_map in starting_maps:
            # we will do the map map_id_x_phi_T AFTER affine_map
            for T_vect in map(lambda x: np.array([x]).T, T.normal_vectors):
                cur_k_perp = affine_map.output_phase_space.k_vect_perp
                if dot(T_vect, cur_k_perp) > 1e-9: # making sure cur_k_perp is not in same direction as T_vect
                    rv.append(affine_map.left_compose(affine_map.output_phase_space.map_phi_K_x_id(new_T_normal_vect=T_vect)))
    return rv

def get_lp_matrix(T, K_dual, phase_space_map: PhaseSpaceMap, solution):
    # we have a linear program where we optimize an affine linear function of free_space_dim variables.
    # Let x be the vector of free variables. This means we are optimizing a function subject to the constraint
    # Ax <= b
    # This means A has free_space_dim columns and one row for each constraint.
    # The constraints are generated by ensuring that x stays in the polytope for each linear map.
    A = None
    b = None
    change_T = False
    change_K = True
    for ps_map in phase_space_map.phase_space_map_list:
        if A is None or b is None:
            A, b = add_constraints_for_map(T, K_dual, ps_map, solution, True, True)
        else:
            constraints_A, constraints_b = add_constraints_for_map(T, K_dual, ps_map, solution, change_T, change_K)
            change_T = not change_T
            change_K = not change_K
            A = np.concatenate([A, constraints_A], axis=0)
            b = np.concatenate([b, constraints_b], axis=0)
    return A, b

def get_lp_objective(K, phase_space_map: PhaseSpaceMap, solution):
    # We want to minimize the K-length of the trajectory.
    # So every other map in ps_map list fixes K. We care about the maps where T changes
    # Since the first map is identity, there are an odd number of phase space maps, and we only want ones with odd index.
    particular_solution: np.matrix = solution["particular"]
    ps_dim = particular_solution.shape[0]
    free_space_t: np.matrix = solution["t_nullspace"]
    free_space_k: np.matrix = solution["k_nullspace"]
    free_space_dim_t = free_space_t.shape[1]
    free_space_dim_k = free_space_k.shape[1]
    # from free space coordinates to phase space coordinates to euclidian coordinates
    # This should be a map with free_space_dim_t columns and dim rows.
    # where dim is the dimention of euclidian space T is embedded into.

    # Multiplying by zero-dimentional matricies should be fine in theory.
    to_euclidian_matrix = phase_space_map.input_phase_space.t_basis @ free_space_t
    to_euclidian_shift = phase_space_map.input_phase_space.t_basis @ particular_solution[:ps_dim//2] + phase_space_map.input_phase_space.t_offset
    prev_t_matrix = to_euclidian_matrix
    prev_t_shift = to_euclidian_shift
    c = np.zeros((free_space_dim_t+free_space_dim_k, 1))
    offset = 0
    for ps_map in phase_space_map.phase_space_map_list[1::2]:
        k_vect_perp = ps_map.output_phase_space.k_vect_perp
        cur_t_matrix = ps_map.T_matrix @ to_euclidian_matrix
        cur_t_shift = ps_map.T_matrix @ to_euclidian_shift + ps_map.T_shift
        # x maps to cur_t_matrix x + cur_t_shift
        # Last time x mapped to prev_t_matrix x + prev_t_shift,
        # The difference cur_t_matrix x + cur_t_shift - (prev_t_matrix x + prev_t_shift) is the thing we want to measure the K-length of.
        k_vect = np.matrix(max_K_vector(np.asarray(k_vect_perp).flatten(), K)).T
        cur_c, cur_offset = dot_product_value(k_vect, cur_t_matrix-prev_t_matrix, cur_t_shift-prev_t_shift)
        cur_c = np.concatenate([cur_c, np.zeros((free_space_dim_k, 1))], axis=0)
        c += cur_c
        offset += cur_offset[0,0]
        prev_t_matrix = cur_t_matrix
        prev_t_shift = cur_t_shift
    return c, offset

def add_constraints_for_map(T, K_dual, ps_map: PhaseSpaceMap, solution, change_T, change_K):
    # should be a column vector
    particular_solution: np.matrix = solution["particular"]
    ps_dim = particular_solution.shape[0]
    free_space_t: np.matrix = solution["t_nullspace"]
    free_space_k: np.matrix = solution["k_nullspace"]
    free_space_dim_t = free_space_t.shape[1]
    free_space_dim_k = free_space_k.shape[1]
    A = None
    b = None
    # The thing we need to check is that Ax+b remains in T. 
    # so for each vector in T (except for ps_map.output_phase_space.t_vect_perp) we need to check that dot(ps_map(x), vector) <= 1
    # It's not quite that simple because ps_map(x) is not in regular coordinates, nor is it in phase space coordinates. 
    # Only when multiplied by solution["t_nullspace"] and then ps_map.input_phase_space.t_basis does it become regular coordinates.
    # This means we first map x to regular coordinates, then we apply ps_map.
    # if the first map is x |--> Mx+q
    # and the second map is y |--> Ny+r
    # we have x |--> N(Mx+q)+r
    # Thus the matrix is N @ M and the shift is N @ q + r

    # We do a similar thing for K.

    # It is worth noting, that we do NOT assume that free_space_dim_t and free_space_dim_k are nonzero, 
    # when the dimentions are zero, we are adding that 0 <= some number.
    if change_T:
        M = ps_map.input_phase_space.t_basis @ free_space_t
        N = ps_map.T_matrix
        q = ps_map.input_phase_space.t_basis @ particular_solution[:ps_dim//2] + ps_map.input_phase_space.t_offset
        r = ps_map.T_shift
        for t_vect in map(lambda x: np.array([x]).T, T.normal_vectors):
            if not matrix_equals(t_vect, ps_map.output_phase_space.t_vect_perp):
                cur_A, cur_b = dot_product_constraint(t_vect, N @ M, N @ q + r)
                cur_A = np.concatenate([cur_A, np.zeros((1, free_space_dim_k))], axis=1)
                if A is None or b is None:
                    A = cur_A
                    b = cur_b
                else:
                    A = np.concatenate([A, cur_A], axis=0)
                    b = np.concatenate([b, cur_b], axis=0)
    if change_K:
        M = ps_map.input_phase_space.k_basis @ free_space_k
        N = ps_map.K_matrix
        q = ps_map.input_phase_space.k_basis @ particular_solution[ps_dim//2:] + ps_map.input_phase_space.k_offset
        r = ps_map.K_shift
        for k_vect in map(lambda x: np.array([x]).T, K_dual.normal_vectors):
            if not matrix_equals(k_vect, ps_map.output_phase_space.k_vect_perp):
                cur_A, cur_b = dot_product_constraint(k_vect, N @ M, N @ q + r)
                cur_A = np.concatenate([np.zeros((1, free_space_dim_t)), cur_A], axis=1)
                if A is None or b is None:
                    A = cur_A
                    b = cur_b
                else:
                    A = np.concatenate([A, cur_A], axis=0)
                    b = np.concatenate([b, cur_b], axis=0)
    return A, b

def dot_product_value(v, matrix, shift):
    # Should return dot(v, matrix @ x + shift)
    # in the form of two vectors, c and d such that dot(v, matrix @ x + shift) = c @ x + d
    # Let P be the matrix.
    # and let w be the shift
    # [[sum_i P_1i x_i + w_1],         [[v_1]     
    # ...                         .    ...
    # [sum_i P_ni x_i + w_n]]          [v_n]]
    # This means c_i = sum_j P_ji v_j
    # and d = sum_j w_j v_j
    c = np.zeros((matrix.shape[1], 1))
    d = np.zeros((1, 1))
    for i in range(matrix.shape[1]):
        num = 0
        for j in range(v.shape[0]):
            num += matrix[j, i] * v[j]
        c[i, 0] = num
    d[0, 0] = dot(shift, v)
    return c, d

def dot_product_constraint(v, matrix, shift):
    # Adds the constraints that dot(v1, matrix @ x + shift) <= 1, int the form of a matrix A and a vector b
    # The matrix should have x.shape[0] columns and one row.
    # Let P be the matrix.
    # and let w be the shift
    # We have dot(v1, Px+w) <= 1
    # [[sum_i P_1i x_i + w_1],         [[v_1]     
    # ...                         .    ...       <=   1
    # [sum_i P_ni x_i + w_n]]          [v_n]]
    # So for each i the constraint is sum_j P_ji v_j
    # and the vector b is 1-sum_j w_j v_j
    A_transposed, one_minus_b = dot_product_value(v, matrix, shift)
    return A_transposed.T, np.ones((1,1))-one_minus_b
    
# T_vectors = np.array([[0.,1.], [1.,0.], [0.,-1.], [-1.,0.]])
# K_vectors = np.array([[1.,0.], [0.,1.], [-1.,0.], [0.,-1.]])

# T = Polytope(normal_vectors=T_vectors, dim=2)
# K = Polytope(normal_vectors=K_vectors, dim=2)
# K_dual = get_polar_dual(K)

# b4 = PhaseSpace(t_vect_perp=np.matrix([0.,1.]).T, k_vect_perp=np.matrix([-1.,-1.]).T)
# d4 = PhaseSpace(t_vect_perp=np.matrix([0.,-1.]).T, k_vect_perp=np.matrix([-1.,-1.]).T)
# d2 = PhaseSpace(t_vect_perp=np.matrix([0.,-1.]).T, k_vect_perp=np.matrix([1.,1.]).T)
# b2 = PhaseSpace(t_vect_perp=np.matrix([0.,1.]).T, k_vect_perp=np.matrix([1.,1.]).T)

# map_1 = b4.map_phi_K_x_id(np.matrix([0.,-1.]).T)
# map_2 = d4.map_id_x_phi_T(np.matrix([1.,1.]).T)
# map_3 = d2.map_phi_K_x_id(np.matrix([0.,1.]).T)
# map_4 = b2.map_id_x_phi_T(np.matrix([-1.,-1.]).T)

# composed_map_1 = map_1.left_compose(after_map=map_2)
# composed_map_2 = composed_map_1.left_compose(after_map=map_3)
# composed_map_3 = composed_map_2.left_compose(after_map=map_4)

# b4 = PhaseSpace(t_vect_perp=np.matrix([0.,1.]).T, k_vect_perp=np.matrix([-1.,-1.]).T)
# a4 = PhaseSpace(t_vect_perp=np.matrix([-1.,0.]).T, k_vect_perp=np.matrix([-1.,-1.]).T)
# a3 = PhaseSpace(t_vect_perp=np.matrix([-1.,0.]).T, k_vect_perp=np.matrix([1.,-1.]).T)
# d3 = PhaseSpace(t_vect_perp=np.matrix([0.,-1.]).T, k_vect_perp=np.matrix([1.,-1.]).T)
# d2 = PhaseSpace(t_vect_perp=np.matrix([0.,-1.]).T, k_vect_perp=np.matrix([1.,1.]).T)
# c2 = PhaseSpace(t_vect_perp=np.matrix([1.,0.]).T, k_vect_perp=np.matrix([1.,1.]).T)
# c1 = PhaseSpace(t_vect_perp=np.matrix([1.,0.]).T, k_vect_perp=np.matrix([-1.,1.]).T)
# b1 = PhaseSpace(t_vect_perp=np.matrix([0.,1.]).T, k_vect_perp=np.matrix([-1.,1.]).T)

# map_1 = b4.map_phi_K_x_id(np.matrix([-1.,0.]).T)
# map_2 = a4.map_id_x_phi_T(np.matrix([1.,-1.]).T)
# map_3 = a3.map_phi_K_x_id(np.matrix([0.,-1.]).T)
# map_4 = d3.map_id_x_phi_T(np.matrix([1.,1.]).T)
# map_5 = d2.map_phi_K_x_id(np.matrix([1., 0.]).T)
# map_6 = c2.map_id_x_phi_T(np.matrix([-1.,1.]).T)
# map_7 = c1.map_phi_K_x_id(np.matrix([0.,1.]).T)
# map_8 = b1.map_id_x_phi_T(np.matrix([-1.,-1.]).T)

# composed_map_1 = map_1.left_compose(after_map=map_2)
# composed_map_2 = composed_map_1.left_compose(after_map=map_3)
# composed_map_3 = composed_map_2.left_compose(after_map=map_4)
# composed_map_4 = composed_map_3.left_compose(after_map=map_5)
# composed_map_5 = composed_map_4.left_compose(after_map=map_6)
# composed_map_6 = composed_map_5.left_compose(after_map=map_7)
# composed_map_7 = composed_map_6.left_compose(after_map=map_8)
