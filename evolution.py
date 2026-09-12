import random
import math
import numpy as np

from Project.Services.Output.VisualizerService import *
from Project.Services.Calculation import RatioService
from Project.Models.BilliardSystem import BilliardSystem
from Project.Models.Polytope import Polytope
from Project.Services.Calculation.CapacityService import is_line_in_cone
from Project.Services.Calculation.VolumeService import get_polar_dual
from Project.Services.Example_Generation.RandomBilliardSystemService import get_random_billiard_system
from Project.Services.Output.FileWriterService import FileWriterService

def calculate_ratio(T, K, filewriter):
    bs = BilliardSystem(T=T, K=K)
    RatioService.set_billiard_system_ratio(bs)
    filewriter.write_billiard_system_to_file(bs)
    return bs.ratio

def generate_random_species(dim, T_sides, K_sides, normalized):
    species = []
    T_ready = False
    while not T_ready:
        for _ in range(T_sides):
            to_append = [random.random()*2-1 for _ in range(dim)]
            if normalized:
                to_append = to_append / np.linalg.norm(to_append)
            species.append(to_append)
        T_ready = is_line_in_cone(np.array(species))
        if not T_ready:
            species = []
    K_ready = False
    while not K_ready:
        for _ in range(K_sides):
            to_append = [random.random()*2-1 for _ in range(dim)]
            if normalized:
                to_append = to_append / np.linalg.norm(to_append)
            species.append(to_append)
        K_ready = is_line_in_cone(np.array(species[T_sides:]))
        if not K_ready:
            species = species[:T_sides]
    return np.array(species)

def mutate(species, mutation_rate, T_sides, K_sides, normailized):
    new_species = []
    T_ready = False
    while not T_ready:
        for i in range(T_sides):
            to_add = []
            for j in range(species.shape[1]):
                to_add.append(species[i][j] + random.gauss(0, mutation_rate))
            if normailized:
                to_add = to_add / np.linalg.norm(to_add)
            new_species.append(to_add)
        T_ready = is_line_in_cone(np.array(new_species[:T_sides]))
        if not T_ready:
            new_species = []
    K_ready = False
    while not K_ready:
        for i in range(T_sides, T_sides+K_sides):
            to_add = []
            for j in range(species.shape[1]):
                to_add.append(species[i][j] + random.gauss(0, mutation_rate))
            if normailized:
                to_add = to_add / np.linalg.norm(to_add)
            new_species.append(to_add)
        K_ready = is_line_in_cone(np.array(new_species[T_sides:]))
        if not K_ready:
            new_species = new_species[:T_sides]
    return np.array(new_species)

def evolution_simulator(dim, T_sides, K_sides, species_count, generations, survival_rate=0.1, mutation_rate=0.1, normailized=False, diminishing_mutation_rate=0):
    species = []
    stop_num = 1.2
    best_alive = None
    filewriter = FileWriterService()
    starting_mutation_rate = mutation_rate
    for _ in range(species_count):
        species.append(generate_random_species(dim, T_sides, K_sides, normailized))
    for i in range(generations):
        print(f"Generation {i+1}")
        scores = []
        for s in species:
            # visualize_polytope(s[:T_sides], points = [], second_polytope = s[T_sides:])
            T = get_polar_dual(get_polar_dual(Polytope(normal_vectors=s[:T_sides], dim=dim)))
            K = get_polar_dual(get_polar_dual(Polytope(normal_vectors=s[T_sides:], dim=dim)))
            num = calculate_ratio(T, K, filewriter)
            print(num)
            scores.append(num)
        # evolving state: 
        # 1. sort species by score
        species_and_scores = list(zip(species, scores))
        species_and_scores.sort(key=lambda x: x[1])
        # 2. take the top 10%
        top_species = species_and_scores[-int(len(species_and_scores)*survival_rate):]   
        # Each of the top species has 10 offspring
        species = []
        for survivor in top_species:
            for _ in range(math.floor(1/survival_rate)):
                species.append(mutate(survivor[0], mutation_rate, T_sides, K_sides, normailized))
        # finding the best alive and updating the stop number
        best_alive = top_species[-1][0]
        print(top_species[-1])
        if i % 10 == 0:
            visualize_polytope(best_alive[:T_sides], points = [], second_polytope = best_alive[T_sides:])
        stop_num = top_species[0][1]
        mutation_rate = starting_mutation_rate/(1+i*diminishing_mutation_rate)
    return best_alive, stop_num

evolution_simulator(dim=2, T_sides=5, K_sides=5, species_count=20, generations=11, survival_rate=0.2, mutation_rate=0.05, normailized=False, diminishing_mutation_rate=0.12)
