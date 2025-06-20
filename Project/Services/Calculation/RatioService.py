import math

from Project.Services.Calculation import VolumeService, CapacityService, PointCloudCapacityService, TrajectoryCapacityService

def set_billiard_system_ratio(billiard_system, stop_num=0, point_cloud_approximation=False, billiards_way = False, num_points=100, samples_per_facet=300):
    K = billiard_system.K
    T = billiard_system.T
    vol = VolumeService.get_volume_k_metric(K=K, T=T)
    # new_stop_num^dim/vol = old_stop_num
    # new_stop_num = (old_stop_num * vol)^(1/dim)
    new_stop_num = math.pow(stop_num * vol, 1/T.dim)
    if point_cloud_approximation:
        capacity = PointCloudCapacityService.approximate_capacity(T=T, K=K, num_points=num_points, samples_per_facet=samples_per_facet)
    elif billiards_way:
        capacity = TrajectoryCapacityService.get_trajectory_capacity(T=T, K=K)
    else:
        capacity = CapacityService.get_capacity(T=T, K=K, volume_k_metric=vol, stop_num=new_stop_num)


    billiard_system.volume_k_metric = vol
    billiard_system.capacity_k_of_t = capacity
    billiard_system.ratio = math.pow(capacity.length, T.dim) / vol
    billiard_system.trajectory = capacity.trajectory
