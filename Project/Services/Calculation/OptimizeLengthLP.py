import numpy as np

from Project.Services.Calculation.LinearProgram import LinearProgram
from Project.Models.Polytope import Polytope

def calculate_b_length(dim, T, K):
    return 2*(dim+1) + len(T.normal_vectors)*(dim+1) + (len(K.normal_vectors)-1)*(dim+1)

def calculate_c_length(dim):
    return (dim+1)**2

class OptimizeLengthLP(LinearProgram):

    def add_constraints_on_ts(self, cones):
        # x_i - x_{i-1} @ cone_i <= t_i 
        # this means -t_i + (x_i - x_{i-1})@ cone_i <= 0
        # -t_i + sum_{j=1}^n (x_i_j - x_{i-1}_j)*cone_i_j <= 0
        for i in range(self.n+1):
            self.A[i][self.n * (self.n+1) + i] = -1
            past = (i-1) % (self.n+1)
            for j in range(self.n):
                self.A[i][i*(self.n) + j] = cones[i][j]
                self.A[i][past*(self.n) + j] = -cones[i][j]

    def add_equalality_constraints_on_xs(self, orbit):
        # x_i @ facet_i >= 1
        # -x_i @ facet_i <= -1
        # sum_{j=1}^n -x_i_j * facet_i_j <= -1
        for i in range(self.n+1):
            self.b[self.n + 1 + i] = -1
            for j in range(self.n):
                self.A[self.n + 1 + i][i*(self.n) + j] = -orbit[i][0][j]
    
    def add_inequality_constraints_on_xs(self, T):
        # x_i @ Tfacet <= 1
        # sum_{j=1}^n x_i_j * Tfacet_j <= 1
        for index, facet in enumerate(T.normal_vectors):
            for i in range(self.n+1):
                self.b[2*(self.n + 1) + index*(self.n+1) + i] = 1
                for j in range(self.n):
                    self.A[2*(self.n + 1) + index*(self.n+1) + i, i*(self.n) + j] = facet[j]

    def add_inequality_constraints_on_differences(self, cones, K):
        # x_i - x_{i-1} @ Kfacet <= x_i - x_{i-1} @ cone_i
        # x_i - x_{i-1} @ Kfacet - cone_i <= 0
        # sum_{j=1}^n (x_i_j - x_{i-1}_j) * (Kfacet_j - cone_i_j) <= 0
        for i in range(self.n+1):
            adj = 0
            for index, facet in enumerate(K.normal_vectors):
                if np.equal(facet, cones[i]).all():
                    adj = 1
                    continue
                past = (i-1) % (self.n+1)
                for j in range(self.n):
                    self.A[2*(self.n + 1) + self.m*(self.n + 1) + (index-adj)*(self.n + 1) + i, i*(self.n) + j] = facet[j] - cones[i][j]
                    self.A[2*(self.n + 1) + self.m*(self.n + 1) + (index-adj)*(self.n + 1) + i, past*(self.n) + j] = -facet[j] + cones[i][j]

    def __init__(self, orbit, cones, T:Polytope, K:Polytope):
        # Each time we run optimize_k_length, it is in the exact same format.
        # when the dimention is n.
        # There is a list of n+1 facets from T which we assume is to have m normal vectors, and a list of n+1 cones from K, which we assume is to have k normal vectors.
        # Here are the variables: Total of (n+1)^2 variables.
        #   We have n+1 n-dimentional vectors x_1..x_{n+1}, each lying on a certain facet.
        #   We have n+1 scalars t_1..t_{n+1}, coorisponding to the lengths of the n+1 edges of the orbit.
        # Here are the constraints: Total of 2(n+1) + m(n+1) + k(n+1) constraints.
        #   (1) n+1 constraints on the ts: x_i - x_{i-1} @ cone_i <= t_i
        #   (2) (n+1) equality constraints on the xs: x_i @ edge_i >= 1
        #   (3) m(n+1) constraints on the xs: x_i @ Tfacet_j <= 1
        #   (4) k(n+1) constraints on the differences: x_i - x_{i-1} @ Kfacet_j <= x_i - x_{i-1} @ cone_i

        self.n = T.dim
        self.m = len(T.normal_vectors)
        self.k = len(K.normal_vectors)
        self.problem_solved = False

        # The number of rows is the number of constraints, which is 2(n+1) + (m-1)(n+1) + k(n+1)
        self.A = np.zeros((2*(self.n+1) + self.m*(self.n+1) + (self.k-1)*(self.n+1), (self.n+1)**2))
        self.b = np.zeros((2*(self.n+1) + self.m*(self.n+1) + (self.k-1)*(self.n+1)))

        # We want to mimimize the sum of the t_i's
        self.c = np.zeros((self.n+1)**2)
        for i in range(self.n+1):
            self.c[self.n * (self.n+1) + i] = 1

        self.add_constraints_on_ts(cones)
        self.add_equalality_constraints_on_xs(orbit)
        self.add_inequality_constraints_on_xs(T)
        self.add_inequality_constraints_on_differences(cones, K)
        

        

        

