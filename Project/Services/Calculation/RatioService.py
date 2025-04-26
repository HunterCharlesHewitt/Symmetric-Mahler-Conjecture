import math

from Project.Services.Calculation import VolumeService, CapacityService


def set_billiard_system_ratio(billiard_system):
    K = billiard_system.K
    T = billiard_system.T
    vol = VolumeService.get_volume_k_metric(K=K, T=T)
    capacity = CapacityService.get_capacity(T=T, K=K, volume_k_metric=vol)
    billiard_system.volume_k_metric = vol
    billiard_system.capacity_k_of_t = capacity
    billiard_system.ratio = math.pow(capacity.length, T.dim) / vol
