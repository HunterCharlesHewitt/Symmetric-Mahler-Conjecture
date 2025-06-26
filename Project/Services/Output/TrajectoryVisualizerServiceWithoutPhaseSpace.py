import numpy as np
from matplotlib import pyplot as plt
from numpy import tan
from matplotlib.animation import PillowWriter
from matplotlib.patches import Polygon
from moviepy import VideoFileClip
from scipy.spatial import HalfspaceIntersection

FRAMES_PER_SECOND = 30
AXIS_MIN = -5
AXIS_MAX = 5
FILENAME = 'trajectory.gif'
COORD_CHANGE_RATE = 0.01
STARTING_T_POSITION = [np.float64(1.658378724774288), np.float64(0.3378274339933091)]
STARTING_T_ANGLE = 170
STARTING_K_POSITION = (-1.5, 1.5 * tan(np.pi / 3) - 3)


def get_random_point_on_edge(polytope):
    vertices = get_sorted_vertices(polytope)
    n = len(vertices)
    i = np.random.randint(0, n)
    v1 = vertices[i]
    v2 = vertices[(i + 1) % n]
    t = np.random.uniform(0, 1)
    x = (1 - t) * v1[0] + t * v2[0]
    y = (1 - t) * v1[1] + t * v2[1]

    return (x, y), (v1, v2)  # Return the point and the edge it came from


def is_point_on_edge(point, v1, v2, epsilon=5*COORD_CHANGE_RATE):
    x, y = point
    x1, y1 = v1
    x2, y2 = v2

    # Step 1: Check collinearity using the 2D cross product
    cross = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)
    if abs(cross) > epsilon:
        return False

    # Step 2: Check if point lies within bounding box of segment
    if (min(x1, x2) - epsilon <= x <= max(x1, x2) + epsilon and
            min(y1, y2) - epsilon <= y <= max(y1, y2) + epsilon):
        return True

    return False


def is_point_on_any_edge(point, polytope, epsilon=5*COORD_CHANGE_RATE):
    polygon_vertices = get_sorted_vertices(polytope)
    n = len(polygon_vertices)
    for i in range(n):
        v1 = polygon_vertices[i]
        v2 = polygon_vertices[(i + 1) % n]
        if is_point_on_edge(point, v1, v2, epsilon):
            return True
    return False


def is_point_inside_polytope(point, polytope, epsilon=5*COORD_CHANGE_RATE):
    vertices = get_sorted_vertices(polytope)
    polygon = Polygon(vertices, closed=True)
    if polygon.contains_point(point):
        return True
    return is_point_on_any_edge(point, polytope, epsilon)


def get_edge_equations(polytope):
    vertices = get_sorted_vertices(polytope)
    equations = []
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        if np.isclose(x1, x2):
            equations.append({'type': 'vertical', 'x': x1})
        else:
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            equations.append({'type': 'line', 'm': m, 'b': b})
    return equations


def find_edge_and_unit_normal(point, polytope, epsilon=5*COORD_CHANGE_RATE):
    vertices = get_sorted_vertices(polytope)
    n = len(vertices)
    for i in range(n):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % n]

        if is_point_on_edge(point, v1, v2, epsilon):
            dx = v2[0] - v1[0]
            dy = v2[1] - v1[1]

            normal = np.array([-dy, dx])
            norm_length = np.linalg.norm(normal)

            if norm_length == 0:
                raise ValueError("Zero-length edge found")

            unit_normal = normal / norm_length
            return unit_normal

    raise Exception("Given point is not on an edge")


def get_slope_of_vector(vec, epsilon=1e-10):
    x, y = vec
    if abs(x) < epsilon:
        return np.inf if y > 0 else -np.inf
    return y / x


def get_t_slope(point, polytope_k):
    normal_vector = find_edge_and_unit_normal(point, polytope_k)
    return get_slope_of_vector(normal_vector)


def get_k_slope(point, polytope_t):
    normal_vector = find_edge_and_unit_normal(point, polytope_t)
    return -1 * get_slope_of_vector(normal_vector)


def draw_shape(polytope, axs_for_polytope, edge_color='green'):
    sorted_vertices = get_sorted_vertices(polytope)
    shape = Polygon(sorted_vertices, closed=True, edgecolor=edge_color, facecolor='none')
    axs_for_polytope.add_patch(shape)


def get_sorted_vertices(polytope):
    half_spaces = np.array([np.append(vector, -1) for vector in polytope])
    interior_point = np.array([0.0, 0.0])
    hs = HalfspaceIntersection(half_spaces, interior_point)
    vertices = hs.intersections
    sorted_vertices = sorted(vertices, key=lambda v: np.arctan2(v[1] - interior_point[1], v[0] - interior_point[0]))
    return sorted_vertices


def set_axs_min_max(local_axs, axs_min, axs_max):
    for ax in local_axs:
        ax.set_xlim([axs_min, axs_max])
        ax.set_ylim([axs_min, axs_max])


def add_frame_for_axis(writer, axs_pts, xval, yval, xlist, ylist):
    xlist.append(xval)
    ylist.append(yval)
    axs_pts.set_data(xlist, ylist)
    writer.grab_frame()


def get_next_point(slope, start_pos, point, slope_0_dir):
    if slope == np.inf:
        point[1] += COORD_CHANGE_RATE
        return point
    elif slope == -1 * np.inf:
        point[1] -= COORD_CHANGE_RATE
        return point
    elif slope < 0:
        point[0] -= COORD_CHANGE_RATE
    elif slope > 0:
        point[0] += COORD_CHANGE_RATE
    else:
        if slope_0_dir == 1:
            point[0] += COORD_CHANGE_RATE
        elif slope_0_dir == -1:
            point[0] -= COORD_CHANGE_RATE
        else:
            raise ValueError('Invalid zero slope direction')
    point[1] = slope * (point[0] - start_pos[0]) + start_pos[1]
    return point


#TODO this function has way too many arguments, suggests a class is hiding in this function
def draw_bounce(writer, polytope, bounce_start_pos, slope, axs_pts, x_list, y_list, axis_for_polytope, slope_0_dir=0):
    # I know the line below looks strange, but it is needed for a shallow copy
    curr_point = [bounce_start_pos[0], bounce_start_pos[1]]
    shape = Polygon(get_sorted_vertices(polytope), closed=True)
    curr_point = get_next_point(start_pos=bounce_start_pos, point=curr_point, slope=slope, slope_0_dir=slope_0_dir)
    while is_point_inside_polytope(point=curr_point, polytope=polytope, epsilon=0.001):
    # while shape.contains_point(axis_for_polytope.transData.transform((curr_point[0], curr_point[1]))):
        add_frame_for_axis(writer, axs_pts, curr_point[0], curr_point[1], x_list, y_list)
        curr_point = get_next_point(start_pos=bounce_start_pos, point=curr_point, slope=slope, slope_0_dir=slope_0_dir)
    if len(x_list) == 0:
        raise Exception("Your bounce_start_pos is most likely outside of the polygon")
    return [x_list[-1], y_list[-1]]


def visualize_trajectory(T, K, t_start_position=STARTING_T_POSITION, t_start_angle=STARTING_T_ANGLE,
                         k_start_position=STARTING_K_POSITION):
    fig, axs = plt.subplots(2, figsize=(5, 10))
    t_axis = axs[0]
    t_axis.set_aspect('equal')
    t_axis.grid(True)
    k_axis = axs[1]
    k_axis.set_aspect('equal')
    k_axis.grid(True)
    axs_1_pts, = t_axis.plot([], [], 'k-')
    axs_2_pts, = k_axis.plot([], [], 'k-')

    # set_axs_min_max(axs, AXIS_MIN, AXIS_MAX)
    metadata = dict(title='Movie', artist='Hunter')
    writer = PillowWriter(fps=FRAMES_PER_SECOND, metadata=metadata)

    draw_shape(polytope=T, axs_for_polytope=t_axis, edge_color='blue')
    draw_shape(polytope=K, axs_for_polytope=k_axis, edge_color='blue')

    # plt.show() # uncomment to see the initial drawing
    curr_t_bounce_start_pos = t_start_position
    curr_k_bounce_start_pos = k_start_position
    t_slope = np.tan(t_start_angle * np.pi / 180)
    x_list_t, y_list_t, x_list_k, y_list_k = [], [], [], []
    with writer.saving(fig, FILENAME, dpi=100):
        for i in range(0, 4):
            curr_t_bounce_start_pos = draw_bounce(writer=writer, polytope=T, bounce_start_pos=curr_t_bounce_start_pos,
                                                  slope=t_slope, axs_pts=axs_1_pts, x_list=x_list_t, y_list=y_list_t, axis_for_polytope=t_axis)

            k_slope = get_k_slope(point=curr_t_bounce_start_pos, polytope_t=T)

            curr_k_bounce_start_pos = draw_bounce(writer=writer, polytope=K, bounce_start_pos=curr_k_bounce_start_pos,
                                                  slope=k_slope, axs_pts=axs_2_pts, x_list=x_list_k, y_list=y_list_k, axis_for_polytope=k_axis)

            t_slope = get_t_slope(point=curr_k_bounce_start_pos, polytope_k=K)


T = np.array([[-0.88538681, 0.16564993], [0.15918032, 0.91929798], [0.78453111, -0.89113456]])
print(is_point_on_any_edge(polytope=T, point=(1.27465, 0)))
K = np.array([[-0.82753897, 0.64060135], [0.54545526, -0.83767349], [0.99944807, 0.3057224]])
visualize_trajectory(T=T, K=K)
