import math

import numpy as np

from Project.Services.Calculation import RatioService
from Project.Models.BilliardSystem import BilliardSystem
from Project.Models.Polytope import Polytope
from Project.Services.Example_Generation.RandomBilliardSystemService import get_random_billiard_system
from Project.Services.Output.FileWriterService import FileWriterService
from Project.Services.Calculation.VolumeService import get_polar_dual
from Project.Services.Output.VisualizerService import visualize_polytope
import sys

def run_on(bs, visualize=False):
    print("T:")
    print(bs.T.normal_vectors)
    print("K:")
    print(bs.K.normal_vectors)
    RatioService.set_billiard_system_ratio(bs)
    print("EHZ CAPACITY VOLUME RATIO:")
    print(bs.ratio)
    if visualize:
        visualize_polytope(polytope = bs.T.normal_vectors, points=[], second_polytope=bs.K.normal_vectors)

if __name__ == '__main__':
    times = 10
    max_num = 0
    filewriter = FileWriterService()
    # for i in range(times):
    #     sys.stdout.write(f"\rTry #:{i} ---- Current_Max: {max_num}")
    #     sys.stdout.flush()

    #     bs = get_random_billiard_system(t_sides=5, k_sides=5, dim=2)
    #     run_on(bs)
    #     # RatioService.set_billiard_system_ratio(bs, billiards_way=True)
    #     # print("RATIO BILLIARDS WAY:")
    #     # print(bs.ratio)
    #     # filewriter.write_billiard_system_to_file(bs)
    #     if bs.ratio > max_num:
    #         max_num = bs.ratio

    # # SQUARE
    # dim=2
    # T_normals = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    # K_normals = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    # # # K = find_polar_dual(dim, np.array([[math.sin(2*math.pi*i/sides), -math.cos(2*math.pi*i/sides)] for i in range((-sides)//2, sides//2)]))
    # T = Polytope(T_normals, dim=dim)
    # K = Polytope(K_normals, dim=dim)

    # # CUBE
    # dim=3
    # T_normals = np.array([[0,0,1],[0,0,-1],[0,1,0],[0,-1,0],[-1,0,0],[1,0,0]])
    # K_normals = np.array([[0,0,1],[0,0,-1],[0,1,0],[0,-1,0],[-1,0,0],[1,0,0]])
    # # # K = find_polar_dual(dim, np.array([[math.sin(2*math.pi*i/sides), -math.cos(2*math.pi*i/sides)] for i in range((-sides)//2, sides//2)]))
    # T = Polytope(T_normals, dim=dim)
    # K = Polytope(K_normals, dim=dim)

    # HAIM OSTROVER COUNTEREXAMPLE TO VITERBO'S CONJECTURE
    dim=2
    sides = 5
    T_vertecies = np.array([[math.cos(2*math.pi*i/sides), math.sin(2*math.pi*i/sides)] for i in range(sides)])
    K_normals = np.array([[math.sin(2*math.pi*i/sides), -math.cos(2*math.pi*i/sides)] for i in range((-sides)//2, sides//2)])
    T = get_polar_dual(Polytope(T_vertecies, dim=dim))
    K = Polytope(K_normals, dim=dim)

    # # Random polytope
    # dim=2
    # T_normals = np.array([[0,1],[0,-1],[0.87,0.2],[-1.3,-1],[-2,-0.3],[-2.3,2.3]])
    # K_normals = np.array([[1,0],[-0.5,-1],[-0.5,2]])
    # # # K = find_polar_dual(dim, np.array([[math.sin(2*math.pi*i/sides), -math.cos(2*math.pi*i/sides)] for i in range((-sides)//2, sides//2)]))
    # T = Polytope(T_normals, dim=dim)
    # K = Polytope(K_normals, dim=dim)
    # T = get_polar_dual(get_polar_dual(T))
    # K = get_polar_dual(get_polar_dual(K))


    bs = BilliardSystem(T=T, K=K)

    run_on(bs, visualize=True)


