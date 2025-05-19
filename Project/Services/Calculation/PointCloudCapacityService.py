from random import choice

import numpy as np

from Project.Services.Calculation import CapacityService
from Project.Services.Calculation.LengthService import K_length
from Project.Models.Capacity import Capacity

def approximate_capacity(T, K, num_points, samples_per_facet):
    dim = T.dim
    orbits, facet_list = CapacityService.get_all_untranslatable_orbits(T)

    # Create a mapping from facet to index
    facet_to_index = {}
    for i, facet in enumerate(T.normal_vectors):
        # Use tuple representation of the facet vector for dictionary key
        facet_to_index[tuple(facet)] = i

    # should create random numbers over [-1,1], not [0,1)
    point_cloud = np.random.rand(num_points, dim) * 2 - 1
    sorted_point_cloud = sort_point_cloud_by_facet(point_cloud, T.normal_vectors)

    shortest_trajectory = None
    shortest_length = float('inf')
    for i, orbit in enumerate(orbits):
        for _ in range(samples_per_facet):
            trajectory = []
            for facet in orbit:
                # Convert numpy array to tuple before using as dictionary key
                # Handle both single vectors and lists of vectors
                if isinstance(facet, np.ndarray):
                    facet_tuple = tuple(facet)
                else:
                    # If facet is a list of vectors, use the first one
                    facet_tuple = tuple(facet[0])
                point_list = sorted_point_cloud[facet_to_index[facet_tuple]]
                if len(point_list) != 0:
                    trajectory.append(choice(point_list))  
            capacity = calculate_K_length(trajectory, K)
            if capacity < shortest_length:
                shortest_length = capacity
                shortest_trajectory = trajectory
    return Capacity(length=shortest_length, orbit=None, cones=None, trajectory=shortest_trajectory)
    

def calculate_K_length(trajectory, K):
    length = 0
    for i, point in enumerate(trajectory):
        past_point = trajectory[(i - 1) % len(trajectory)]
        length += K_length(past_point, point, K)
    return length

def sort_point_cloud_by_facet(point_cloud, facets):
    rv = {}
    for i, facet in enumerate(facets):
        rv[i] = []
    for point in point_cloud:
        facet_index = find_facet_for_point(point, facets)
        # scalar multiply point by 1/(np.dot(point, facet))
        point = point * (1 / np.dot(point, facets[facet_index]))
        rv[facet_index].append(point)
    return rv


def find_facet_for_point(point, facets):
    # should return the max value of np.dot(point, facet)
    max_dot = -float('inf')
    max_facet_index = None
    for i, facet in enumerate(facets):
        dot = np.dot(point, facet)
        if dot > max_dot:
            max_dot = dot
            max_facet_index = i
    return max_facet_index
