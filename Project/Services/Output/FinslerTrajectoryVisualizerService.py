from math import tan

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
from matplotlib.patches import Polygon
from moviepy import VideoFileClip


def draw_T():
    square = plt.Rectangle((-3, -3), 6, 6, facecolor='white', edgecolor="red")
    axs[0].add_patch(square)
    return square


def draw_K():
    side_length = 3
    p1 = np.array([-3, -3])
    p2 = np.array([side_length, -3])
    height = np.sqrt(np.square(6) - np.square(3))
    p3 = np.array([0, height - 3])
    pts = np.array([p1, p2, p3])
    triangle = Polygon(pts, closed=True, edgecolor='blue', facecolor='white')
    axs[1].add_patch(triangle)
    return triangle


def add_frame_for_axis(axs_pts, xval, yval, xlist, ylist):
    xlist.append(xval)
    ylist.append(yval)
    axs_pts.set_data(xlist, ylist)
    writer.grab_frame()


def set_axs_min_max(local_axs, axs_min, axs_max):
    for ax in local_axs:
        ax.set_xlim([axs_min, axs_max])
        ax.set_ylim([axs_min, axs_max])


def get_slope():
    pass


def draw_T_bounce(new_bounce_starting_position, slope, axs_pts, xList, yList):
    curr_point = [new_bounce_starting_position[0], new_bounce_starting_position[1]]
    while T_shape.contains_point(axs[0].transData.transform((curr_point[0], curr_point[1]))):
        add_frame_for_axis(axs_pts, curr_point[0], curr_point[1], xlist_T, ylist_T)
        if slope == np.inf:
            curr_point[1] += COORD_CHANGE_RATE
            continue
        elif slope == -1 * np.inf:
            curr_point[1] -= COORD_CHANGE_RATE
            continue
        elif slope < 0:
            curr_point[0] -= COORD_CHANGE_RATE
        elif slope > 0 and slope != -1 * np.inf:
            curr_point[0] += COORD_CHANGE_RATE
        else:
            #TODO This is incorrect
            curr_point[1] += COORD_CHANGE_RATE
            continue
        curr_point[1] = slope * (curr_point[0] - new_bounce_starting_position[0]) + new_bounce_starting_position[1]
    return [xList[-1], yList[-1]]


if __name__ == '__main__':
    # Size Parameters
    FRAMES_PER_SECOND = 30
    AXIS_MIN = -5
    AXIS_MAX = 5
    COORD_CHANGE_RATE = 3 / 70
    STARTING_T_POSITION = [0, -3]
    STARTING_T_ANGLE = 150
    STARTING_K_POSITION = (-1.5, 1.5 * tan(np.pi / 3) - 3)

    # K_NORMAL_SLOPES = [inf,sqrt(3)/3, -sqrt(3)/3]
    # T_NORMAL_SLOPES = [0,-0, inf, -inf]

    # FIGURE SETUP
    fig, axs = plt.subplots(2, figsize=(5, 10))
    axs_1_pts, = axs[0].plot([], [], 'k-')
    axs_2_pts, = axs[1].plot([], [], 'k-')
    set_axs_min_max(axs, AXIS_MIN, AXIS_MAX)
    metadata = dict(title='Movie', artist='Hunter')
    writer = PillowWriter(fps=FRAMES_PER_SECOND, metadata=metadata)

    T_shape = draw_T()
    K_shape = draw_K()

    with writer.saving(fig, 'trajectory.gif', 100):
        xlist_T = []
        ylist_T = []
        slope = np.tan(STARTING_T_ANGLE * np.pi / 180)
        curr_t_bounce_starting_position = draw_T_bounce(STARTING_T_POSITION, slope=slope, axs_pts=axs_1_pts, xList=xlist_T, yList=ylist_T)

        # curr_k_bounce_starting_position = draw_T_bounce(STARTING_K_POSITION, slope)

        xlist_K = []
        ylist_K = []
        for xval in np.linspace(np.cos(np.pi / 3) * 3 - 3, np.cos(np.pi / 3) * 3, 100):
            add_frame_for_axis(axs_2_pts, xval, np.sin(np.pi / 3) * 3 - 3, xlist_K, ylist_K)

        curr_t_bounce_starting_position = draw_T_bounce(curr_t_bounce_starting_position, np.sqrt(3) / 3, axs_pts=axs_1_pts, xList=xlist_T, yList=ylist_T)

        xlist_K_new = []
        ylist_K_new = []
        axs_2_pts_new, = axs[1].plot([], [], 'r-')  # 'r-' means red line
        for xval in np.linspace(np.cos(np.pi / 3) * 3, np.cos(np.pi / 3) * 3 - 3, 100):
            add_frame_for_axis(axs_2_pts_new, xval, np.sin(np.pi / 3) * 3 - 3, xlist_K_new, ylist_K_new)

        curr_t_bounce_starting_position = draw_T_bounce(curr_t_bounce_starting_position, -1 * np.sqrt(3) / 3, axs_pts=axs_1_pts, xList=xlist_T, yList=ylist_T)

        for yval in np.linspace(np.sin(np.pi / 3) * 3 - 3, -3, 75):
            add_frame_for_axis(axs_2_pts_new, np.cos(np.pi / 3) * 3 - 3, yval, xlist_K_new, ylist_K_new)

        curr_t_bounce_starting_position = draw_T_bounce(curr_t_bounce_starting_position, -1 * np.inf, axs_pts=axs_1_pts, xList=xlist_T, yList=ylist_T)

        axs_2_pts_new_new, = axs[1].plot([], [], color='#00FF00')
        xlist_K_new_new = []
        ylist_K_new_new = []
        for yval in np.linspace(-3, np.sin(np.pi / 3) * 3 - 3, 100):
            add_frame_for_axis(axs_2_pts_new_new, np.cos(np.pi / 3) * 3 - 3, yval, xlist_K_new_new, ylist_K_new_new)

        for i in range(0, 100):
            writer.grab_frame()

        clip = VideoFileClip("trajectory.gif")
        clip.write_videofile("trajectory.mp4")
