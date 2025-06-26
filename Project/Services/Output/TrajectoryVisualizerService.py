from scipy.spatial import HalfspaceIntersection
import numpy as np
from matplotlib.patches import Polygon
from matplotlib import pyplot as plt


def get_polytope_sorted_vertices(polytope):
    half_spaces = np.array([np.append(vector, -1) for vector in polytope.normal_vectors])
    interior_point = np.array([0.0, 0.0])
    hs = HalfspaceIntersection(half_spaces, interior_point)
    vertices = hs.intersections
    sorted_vertices = sorted(vertices, key=lambda v: np.arctan2(v[1] - interior_point[1], v[0] - interior_point[0]))
    print_str = ""
    for v in sorted_vertices:
        print_str += "(" + str(v[0]) + "," + str(v[1]) + "),"
    print_str += "(" + str(sorted_vertices[0][0]) + "," + str(sorted_vertices[0][1]) + ")"
    print(print_str)
    return sorted_vertices


def draw_polytope(polytope, axs_for_polytope, edge_color='green'):
    sorted_vertices = get_polytope_sorted_vertices(polytope)
    shape = Polygon(sorted_vertices, closed=True, edgecolor=edge_color, facecolor='none')
    axs_for_polytope.add_patch(shape)
    x_vals = [x[0] for x in sorted_vertices]
    y_vals = [y[1] for y in sorted_vertices]
    fig_min = min(min(x_vals), min(y_vals)) - 1
    fig_max = max(max(x_vals), max(y_vals)) + 1
    axs_for_polytope.set_xlim(fig_min, fig_max)
    axs_for_polytope.set_ylim(fig_min, fig_max)
    axs_for_polytope.scatter(*zip(*sorted_vertices), color='green')


def visualize_trajectory(T, K, t_list, k_list):
    if T.dim != 2:
        raise ValueError('Figure is expected to be a 2-dimensional for visualization')
    fig, axs = plt.subplots(2, figsize=(5, 10))
    t_axis = axs[0]
    k_axis = axs[1]
    t_axis.set_aspect('equal')
    k_axis.set_aspect('equal')
    t_axis.set_title("T")
    k_axis.set_title("K")
    t_axis.grid(True)
    k_axis.grid(True)

    print("T")
    draw_polytope(polytope=T, axs_for_polytope=t_axis, edge_color='blue')
    print("K")
    draw_polytope(polytope=K, axs_for_polytope=k_axis, edge_color='blue')

    plt.show()
