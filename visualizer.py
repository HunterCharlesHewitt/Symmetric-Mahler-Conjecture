from scipy.spatial import HalfspaceIntersection
import matplotlib.pyplot as plt
import numpy as np

def visualize_polytope(polytope, points = [], second_polytope = None):
    dim = len(polytope[0])
    if dim != 2:
        raise Exception("Can not visualize non two dimentional polytopes.")
    halfspaces = np.array([np.append(vector, -1) for vector in polytope])

    print(halfspaces)

    # Interior point (must satisfy all constraints)
    interior_point = np.array([0.0, 0.0])

    hs = HalfspaceIntersection(halfspaces, interior_point)
    vertices = hs.intersections

    # Use the interior point to sort angles
    def angle_from_interior(v):
        return np.arctan2(v[1] - interior_point[1], v[0] - interior_point[0])

    sorted_vertices = sorted(vertices, key=angle_from_interior)

    plt.fill(*zip(*sorted_vertices), alpha=0.5, edgecolor='green')
    plt.scatter(*zip(*sorted_vertices), color='green')
    if points:
        plt.scatter(*zip(*points), color='red')
    plt.gca().set_aspect('equal')
    plt.title("Convex Polygon (Sorted via Interior Point)")
    plt.grid(True)

    if second_polytope is not None:
        halfspaces2 = np.array([np.append(vector, -1) for vector in second_polytope])

        hs2 = HalfspaceIntersection(halfspaces2, interior_point)
        vertices2 = sorted(hs2.intersections, key=angle_from_interior)

        plt.fill(*zip(*vertices2), alpha=0.5, edgecolor='orange')
        plt.scatter(*zip(*vertices2), color='orange')
    plt.show()
    