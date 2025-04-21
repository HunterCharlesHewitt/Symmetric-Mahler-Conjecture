import math
import random


from optimizer import *
from visualizer import *

def calculate_ratio(dim, T, K, stop_num=None):
    if stop_num is None:
        stop_num = math.factorial(dim)
    # reducing the number of facets
    T = find_polar_dual(dim, find_polar_dual(dim, T))
    K = find_polar_dual(dim, find_polar_dual(dim, K))
    vol = volume_k_metric(dim, K, T)
    if vol == 0:
        print("THIS IS A BIG PROBLEM")
        print(T)
        print(K)
    return math.pow(c_K_T_(T, K, stop_num), dim)/volume_k_metric(dim, K, T)

def generate_random_species(dim, T_sides, K_sides):
    species = []
    T_ready = False
    while not T_ready:
        for _ in range(T_sides):
            species.append([random.random()*2-1 for _ in range(dim)])
        T_ready = check_if_line_in_cone(np.array(species))
        if not T_ready:
            species = []
    K_ready = False
    while not K_ready:
        for _ in range(K_sides):
            species.append([random.random()*2-1 for _ in range(dim)])
        K_ready = check_if_line_in_cone(np.array(species[T_sides:]))
        if not K_ready:
            species = species[:T_sides]
    return np.array(species)

def mutate(species, mutation_rate, T_sides, K_sides):
    new_species = []
    T_ready = False
    while not T_ready:
        for i in range(T_sides):
            to_add = []
            for j in range(species.shape[1]):
                to_add.append(species[i][j] + random.gauss(0, mutation_rate))
            new_species.append(to_add)
        T_ready = check_if_line_in_cone(np.array(new_species[:T_sides]))
        if not T_ready:
            new_species = []
    K_ready = False
    while not K_ready:
        for i in range(T_sides, T_sides+K_sides):
            to_add = []
            for j in range(species.shape[1]):
                to_add.append(species[i][j] + random.gauss(0, mutation_rate))
            new_species.append(to_add)
        K_ready = check_if_line_in_cone(np.array(new_species[T_sides:]))
        if not K_ready:
            new_species = new_species[:T_sides]
    return np.array(new_species)

def evolution_simulator(dim, T_sides, K_sides, species_count, generations, survival_rate=0.1, mutation_rate=0.1):
    species = []
    stop_num = 1.2
    best_alive = None
    for _ in range(species_count):
        species.append(generate_random_species(dim, T_sides, K_sides))
    for _ in range(generations):
        scores = []
        for s in species:
            # visualize_polytope(s[:T_sides], points = [], second_polytope = s[T_sides:])
            num = calculate_ratio(dim, s[:T_sides], s[T_sides:], stop_num)
            print(num)
            scores.append(num)
        # evolving state: 
        # 1. sort species by score
        species_and_scores = list(zip(species, scores))
        species_and_scores.sort(key=lambda x: x[1])
        # 2. take the top 10%
        top_species = species_and_scores[-int(len(species_and_scores)*survival_rate):]   
        print(top_species)
        # Each of the top species has 10 offspring
        species = []
        for survivor in top_species:
            for _ in range(math.floor(1/survival_rate)):
                species.append(mutate(survivor[0], mutation_rate, T_sides, K_sides))
        # finding the best alive and updating the stop number
        best_alive = top_species[-1][0]
        visualize_polytope(best_alive[:T_sides], points = [], second_polytope = best_alive[T_sides:])
        stop_num = (top_species[-1][1]+top_species[0][1])/2
    return best_alive, stop_num
