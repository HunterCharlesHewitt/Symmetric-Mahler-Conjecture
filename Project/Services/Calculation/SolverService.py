from abc import ABC, abstractmethod
import cvxpy as cp


# This is an abstract class that we can implement with something other than cvxpy if we wish
class SolverService(ABC):

    @abstractmethod
    def solve(self):
        pass

    @abstractmethod
    def add_constraints(self):
        pass
