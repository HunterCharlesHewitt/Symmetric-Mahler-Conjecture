import math

from Services.VolumeService import get_volume_k_metric
from Services.CapacityService import get_capacity


def set_billiard_system_ratio(billiard_system):
    K = billiard_system.K
    T = billiard_system.T
    vol = get_volume_k_metric(K=K, T=T)
    capacity = get_capacity(T=T, K=K, volume_k_metric=vol)
    billiard_system.ratio = math.pow(capacity.length, T.dim) / vol
