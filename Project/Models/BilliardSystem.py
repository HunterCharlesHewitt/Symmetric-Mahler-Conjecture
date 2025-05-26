from Project.Services.Calculation.VolumeService import get_polar_dual

class BilliardSystem:
    def __init__(self, K, T):
        self.K = K
        self.T = T
        self.ratio = None
        self.volume_k_metric = None
        self.capacity_k_of_t = None
        self.trajectory = None
    
    def get_dual_billiard_system(self):
        return BilliardSystem(T = get_polar_dual(self.K), K = get_polar_dual(self.T))