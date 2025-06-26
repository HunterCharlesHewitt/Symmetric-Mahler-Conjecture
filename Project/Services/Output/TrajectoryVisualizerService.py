import uuid

from matplotlib.animation import PillowWriter
import numpy as np
from matplotlib.patches import Polygon
from matplotlib import pyplot as plt

NUM_POINTS_PLOTTED_PER_LINE = 30


def draw_polytope(polytope, axs_for_polytope, edge_color='green'):
    sorted_vertices = polytope.get_sorted_vertices()
    shape = Polygon(sorted_vertices, closed=True, edgecolor=edge_color, facecolor='none')
    axs_for_polytope.add_patch(shape)
    x_vals = [x[0] for x in sorted_vertices]
    y_vals = [y[1] for y in sorted_vertices]
    fig_min = min(min(x_vals), min(y_vals)) - 1
    fig_max = max(max(x_vals), max(y_vals)) + 1
    axs_for_polytope.set_xlim(fig_min, fig_max)
    axs_for_polytope.set_ylim(fig_min, fig_max)
    axs_for_polytope.scatter(*zip(*sorted_vertices), color='green')


def get_slope_and_direction(start, end, epsilon=1e-10):
    if abs(end[0] - start[0]) < epsilon:
        direction = "+" if (end[1] - start[1]) > 0 else "-"
        slope = np.inf
    else:
        direction = "+" if (end[0] - start[0]) > 0 else "-"
        slope = (end[1] - start[1]) / (end[0] - start[0])
    return slope, direction


class TrajectoryVisualizerService:
    def __init__(self, T, K, t_list, k_list):
        if T.dim != 2:
            raise ValueError('Figure is expected to be a 2-dimensional for visualization')
        self.T = T
        self.K = K
        self.t_list = t_list
        self.k_list = k_list
        self.plotted_t_values = [[], []]
        self.plotted_k_values = [[], []]

        self.fig, self.axs = plt.subplots(2, figsize=(5, 10))
        self.t_axis = self.axs[0]
        self.k_axis = self.axs[1]
        self.t_plot_points, = self.t_axis.plot([], [], 'k-')
        self.k_plot_points, = self.k_axis.plot([], [], 'k-')

        self.t_axis.set_aspect('equal')
        self.k_axis.set_aspect('equal')
        self.t_axis.set_title("T")
        self.k_axis.set_title("K")
        self.t_axis.grid(True)
        self.k_axis.grid(True)

        self.filename = "Project/Services/Output/Trajectory_Visualization_Outputs/Trajectory_Visualization_" + str(uuid.uuid4().hex) + ".gif"

        metadata = dict(title='Trajectory Visualizer')
        self.writer = PillowWriter(fps= 30, metadata=metadata)

    def visualize_trajectory(self):
        draw_polytope(polytope=self.T, axs_for_polytope=self.t_axis, edge_color='blue')
        draw_polytope(polytope=self.K, axs_for_polytope=self.k_axis, edge_color='blue')
        # plt.show()
        with self.writer.saving(self.fig, self.filename, dpi=100):
            for i in range(len(self.t_list) - 1):
                self.draw_bounce(self.t_list[i], self.t_list[i + 1], self.t_plot_points, self.plotted_t_values)
                self.draw_bounce(self.k_list[i], self.k_list[i + 1], self.k_plot_points, self.plotted_k_values)

    def draw_bounce(self, start, end, plot_points, plotted_values):
        if start[0] == end[0] and start[1] == end[1]:
            raise ValueError("Starting and ending points in a bounce should not be equal")
        slope, direction = get_slope_and_direction(start=start, end=end)
        curr_x_val = start[0]
        curr_y_val = start[1]
        y_val_change_rate = abs(start[1] - end[1]) / NUM_POINTS_PLOTTED_PER_LINE
        x_val_change_rate = abs(start[0] - end[0]) / NUM_POINTS_PLOTTED_PER_LINE
        if slope == np.inf:
            if direction == "+":
                while curr_y_val < end[1]:
                    self.add_frame_for_axis(plot_points, curr_x_val, curr_y_val, plotted_values)
                    curr_y_val += y_val_change_rate
            else:
                while curr_y_val > end[1]:
                    self.add_frame_for_axis(plot_points, curr_x_val, curr_y_val, plotted_values)
                    curr_y_val -= y_val_change_rate
        else:
            if direction == "+":
                while curr_x_val < end[0]:
                    self.add_frame_for_axis(plot_points, curr_x_val, curr_y_val, plotted_values)
                    curr_x_val += x_val_change_rate
                    curr_y_val = slope * (curr_x_val - start[0]) + start[1]
            else:
                while curr_x_val > end[0]:
                    self.add_frame_for_axis(plot_points, curr_x_val, curr_y_val, plotted_values)
                    curr_x_val -= x_val_change_rate
                    curr_y_val = slope * (curr_x_val - start[0]) + start[1]

    def add_frame_for_axis(self, axs_pts, x_val, y_val, plotted_values):
        plotted_values[0].append(x_val)
        plotted_values[1].append(y_val)
        axs_pts.set_data(plotted_values[0], plotted_values[1])
        self.writer.grab_frame()
