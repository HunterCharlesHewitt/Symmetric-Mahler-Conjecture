import numpy as np
from scipy.linalg import null_space

class PhaseSpace:
    def __init__(self, t_vect_perp, k_vect_perp):
        self.vect_dim = t_vect_perp.shape[0]
        self.phase_space_dim = 2*(self.vect_dim-1)
        self.t_vect_perp = t_vect_perp
        self.k_vect_perp = k_vect_perp
        self.t_basis = null_space(t_vect_perp.reshape(1, -1))  # shape (vect_dim, vect_dim-1)
        self.k_basis = null_space(k_vect_perp.reshape(1, -1))  # shape (vect_dim, vect_dim-1)

    def to_phase_space_coordinates(self, t_vect, k_vect):
        return np.concatenate([self.t_basis.T @ t_vect, self.k_basis.T @ k_vect])

    def from_phase_space_coordinates(self, x):
        return self.t_basis @ x[:self.phase_space_dim/2], self.k_basis @ x[self.phase_space_dim/2:]
    
    def map_id_x_phi_T(self, new_K_normal_vect):
        # <new_K_normal_vect, x - lambda self.t_vect_perp> = 1
        # x mapsto -lambda(x) self.t_vect_perp + x
        # where lambda(x) = <new_K_normal_vect,x>/s - 1/s
        # This means K_shift = self.t_vect_perp/s
        # and K_matrix = I - A
        # where A = [[self.t_vect_perp_1/s new_K_normal_vect^T]
        #            [...]
        #            [self.t_vect_perp_self.vect_dim/s new_K_normal_vect^T]]
        # where s = <new_K_normal_vect,self.t_vect_perp>
        s = np.dot(new_K_normal_vect, self.t_vect_perp)
        if(s == 0):
            raise ValueError("new_K_normal_vect and self.t_vect_perp are perpendicular")
        K_shift = self.t_vect_perp/s
        A = np.outer(self.t_vect_perp, new_K_normal_vect)/s
        K_matrix = np.eye(self.vect_dim) - A
        output_phase_space = PhaseSpace(t_vect_perp=self.t_vect_perp,k_vect_perp=new_K_normal_vect)
        return PhaseSpaceMap(
            input_phase_space=self,
            output_phase_space=output_phase_space,
            T_matrix=np.eye(self.vect_dim),
            K_matrix=K_matrix,
            T_shift=np.zeros((self.vect_dim, 1)),
            K_shift=K_shift
        )
    
    def map_phi_K_x_id(self, new_T_normal_vect):
        # <new_T_normal_vect, x + lambda self.k_vect_perp> = 1
        # x mapsto lambda(x) self.k_vect_perp + x
        # where lambda(x) = -<new_T_normal_vect,x>/s + 1/s
        # This means T_shift = self.k_vect_perp/s
        # and T_matrix = I - A
        # where A = [[self.k_vect_perp_1/s new_T_normal_vect^T]
        #            [...]
        #            [self.k_vect_perp_self.vect_dim/s new_T_normal_vect^T]]
        # where s = <new_T_normal_vect,self.k_vect_perp>
        s = np.dot(new_T_normal_vect, self.k_vect_perp)
        if(s == 0):
            raise ValueError("new_T_normal_vect and self.k_vect_perp are perpendicular")
        T_shift = self.k_vect_perp/s
        A = np.outer(self.k_vect_perp, new_T_normal_vect)/s
        T_matrix = np.eye(self.vect_dim) - A
        output_phase_space = PhaseSpace(t_vect_perp=new_T_normal_vect,k_vect_perp=self.k_vect_perp)
        return PhaseSpaceMap(
            input_phase_space=self,
            output_phase_space=output_phase_space,
            T_matrix=T_matrix,
            K_matrix=np.eye(self.vect_dim),
            T_shift=T_shift,
            K_shift=np.zeros((self.vect_dim, 1))
        )


class PhaseSpaceMap:
    def __init__(self, input_phase_space, output_phase_space, T_matrix, K_matrix, T_shift, K_shift):
        self.input_phase_space = input_phase_space
        self.output_phase_space = output_phase_space
        self.vect_dim = input_phase_space.vect_dim
        self.phase_space_dim = input_phase_space.phase_space_dim
        if(output_phase_space.vect_dim != self.vect_dim or output_phase_space.phase_space_dim != self.phase_space_dim):
            raise ValueError("Phase space dimensions do not match")
        self.T_matrix = T_matrix # shape (vect_dim, vect_dim)
        self.K_matrix = K_matrix # shape (vect_dim, vect_dim)
        self.T_shift = T_shift # shape (vect_dim, 1)
        self.K_shift = K_shift # shape (vect_dim, 1)
        self.is_length_function_set = False
    
    def set_length_function_of_T(self, length_dot, length_shift):
        # should be an affine linear function of input_phase_space
        self.is_length_function_set = True
        self.length_dot = length_dot
        self.length_shift = length_shift

    def map_x(self, x):
        t_vect, k_vect = self.input_phase_space.from_phase_space_coordinates(x)
        t_vect_mapped = self.T_matrix @ t_vect + self.T_shift
        k_vect_mapped = self.K_matrix @ k_vect + self.K_shift
        return self.output_phase_space.to_phase_space_coordinates(t_vect_mapped, k_vect_mapped)
    
    def left_compose(self, after_map):
        # matrix multiplication so it is right to left, thus left is after
        composed_map = PhaseSpaceMap(
            input_phase_space=self.input_phase_space,
            output_phase_space=after_map.output_phase_space,
            T_matrix = after_map.T_matrix @ self.T_matrix,
            K_matrix = after_map.K_matrix @ self.K_matrix,
            T_shift = after_map.T_shift + after_map.T_matrix @ self.T_shift,
            K_shift = after_map.K_shift + after_map.K_matrix @ self.K_shift
        )
        if self.is_length_function_set and after_map.is_length_function_set:
            # Length functions are added together, so the length should be 
            # self's length_function(self.input_phase_space) + after_map's length_function(after_map.input_phase_space)
            # but we don't have access to after_map.input_phase_space
            # If after_maps's length_function(y) = cy+d
            # and y = self.T_matrix @ x + self.T_shift
            # then after_map's length function(x) = (self.T_matrix^T @ c) @ x + (c @ self.T_shift + d)
            # Thus we add (self.T_matrix^T @ c) to self.length_dot
            # and we add c @ self.T_shift + d to self.length_shift
            composed_map.length_dot = self.length_dot + self.T_matrix.T @ after_map.length_dot
            composed_map.length_shift = self.length_shift + after_map.length_dot @ self.T_shift + after_map.length_shift
        return composed_map            
    
    def right_compose(self, before_map):
        composed_map = PhaseSpaceMap(
            input_phase_space=before_map.input_phase_space,
            output_phase_space=self.output_phase_space,
            T_matrix = self.T_matrix @ before_map.T_matrix,
            K_matrix = self.K_matrix @ before_map.K_matrix,
            T_shift = self.T_shift + self.T_matrix @ before_map.T_shift,
            K_shift = self.K_shift + self.K_matrix @ before_map.K_shift
        )
        if self.is_length_function_set and before_map.is_length_function_set:
            composed_map.length_dot = before_map.length_dot + before_map.T_matrix.T @ self.length_dot
            composed_map.length_shift = before_map.length_shift + self.length_dot @ before_map.T_shift + self.length_shift
        return composed_map
