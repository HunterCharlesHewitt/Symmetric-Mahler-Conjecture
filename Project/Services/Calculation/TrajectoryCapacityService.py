import numpy as np

from Project.Services.Calculation.VolumeService import get_polar_dual
from Project.Services.Calculation.LengthService import K_length
from Project.Models.PhaseSpace import PhaseSpace, PhaseSpaceMap, dot
from Project.Models.Capacity import Capacity
from Project.Models.Polytope import Polytope
from Project.Services.Output.TrajectoryVisualizerService import TrajectoryVisualizerService

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
    for phase_space_map in phase_space_maps:
        if phase_space_map.is_endomorphism():
            x = find_fixed_point(phase_space_map)
            if x is not None:
                # fix_T starts out as true, so we only want the even indexes in phase_space_map_list
                t_phase_space_map_list = phase_space_map.phase_space_map_list[::2]
                length = calculate_trajectory(T, K, x, t_phase_space_map_list, visualize_trajectory=True)
                if length < min_length:
                    min_length = length
                    min_cone = phase_space_map.input_phase_space.k_vect_perp
    return Capacity(length=min_length, orbit=None, cones=min_cone, trajectory=None)

def in_polytope(x, T: Polytope):
    tolerance = 1e-7
    for vect in T.normal_vectors:
        # The check below fails because vdot gets an array with 'dtype=object'.
        # It's an array whose elements are other arrays, not numbers.
        # vdot can't do math on that, even if the shape seems right.
        if dot(x, np.matrix(vect).T) > 1+tolerance:
            return False
    return True

def find_fixed_point(phase_space_map: PhaseSpaceMap):
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
    x_particular = np.linalg.lstsq(A, b_flat, rcond=None)[0]
    residual = np.linalg.norm(A @ x_particular - b_flat)
    if residual > tolerance:
        return None
    
    # only returning a particular solution even if there are many.
    # We should change this in the future, because it might cause an error, and be blatanly wrong.

    return np.matrix(x_particular).T

def calculate_trajectory(T, K, x, t_phase_space_maps: list[PhaseSpaceMap], visualize_trajectory=False):
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
        if not in_polytope(cur_k, K) or dot(cur_k, phase_space_map.output_phase_space.k_vect_perp) < 1-1e-6:
            return float('inf')
        length += float(K_length(prev_t, cur_t, K))
        prev_t = cur_t
    if length < 1e-5:
        return float('inf')
    if visualize_trajectory:
        # TODO I think the problem is that i'm drawing K when I should be doing the unit ball of K? Or something?
        vs = TrajectoryVisualizerService(T=T, K=K, t_list=t_list, k_list=k_list)
        vs.visualize_trajectory()
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
