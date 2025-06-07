import numpy as np

from Project.Services.Calculation.VolumeService import get_polar_dual
from Project.Models.PhaseSpace import PhaseSpace, PhaseSpaceMap

def get_trajectory_capacity(T, K):
    # T is the table K is the norm
    K_dual = get_polar_dual(K)

    dim = T.dim
    # These can be thought of as nodes.
    phace_spaces = generate_phase_spaces(T, K_dual)
    phase_space_maps = generate_initial_phase_space_maps(phace_spaces)

    fix_T = False
    for _ in range(dim*2):
        phase_space_maps = expatend_phase_space_maps(phase_space_maps, T, K_dual, fix_T)
        fix_T = not fix_T

def generate_phase_spaces(T, K_dual):
    rv = []
    for t_vect_perp in T.normal_vectors:
        for k_vect_perp in K_dual.normal_vectors:
            if np.dot(t_vect_perp, k_vect_perp) <= 0:
                rv.append(PhaseSpace(t_vect_perp=t_vect_perp, k_vect_perp=k_vect_perp))
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


def expatend_phase_space_maps(starting_maps, T, K_dual, fix_T):
    rv = []
    if(fix_T):
        for affine_map in starting_maps:
            # we will do the map map_id_x_phi_T AFTER affine_map
            for K_vect in K_dual.normal_vectors:
                if not np.array_equal(K_vect, affine_map.output_phase_space.k_vect_perp):
                    rv.append(affine_map.left_compose(affine_map.map_id_x_phi_T(new_K_normal_vect=K_vect)))
    else:
        for affine_map in starting_maps:
            # we will do the map map_id_x_phi_T AFTER affine_map
            for T_vect in T.normal_vectors:
                if not np.array_equal(T_vect, affine_map.output_phase_space.t_vect_perp):
                    rv.append(affine_map.left_compose(affine_map.map_phi_K_x_id(new_T_normal_vect=T_vect)))
    return rv

