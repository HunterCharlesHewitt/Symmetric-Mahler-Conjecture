class BilliardSystem:
    def __init__(self, K, T):
        self.K = K
        self.T = T
        self.ratio = None
        self.volume_k_metric = None
        self.capacity_k_of_t = None