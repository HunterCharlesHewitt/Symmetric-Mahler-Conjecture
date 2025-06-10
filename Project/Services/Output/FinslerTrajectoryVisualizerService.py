from math import tan

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
from matplotlib.patches import Polygon
from moviepy import VideoFileClip

def func(x):
    return np.sin(x) * 3


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


if __name__ == '__main__':
    # Size Parameters
    FRAMES_PER_SECOND = 30
    AXIS_MIN = -5
    AXIS_MAX = 5
    STARTING_T_POSITION = [0, -3]
    STARTING_T_ANGLE = 150
    STARTING_K_POSITION = (-1.5, 1.5 * tan(np.pi / 3) - 3)

    # K_NORMAL_SLOPES = [inf,sqrt(3)/3, -sqrt(3)/3]

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
        point = [STARTING_T_POSITION[0], STARTING_T_POSITION[1]]
        while T_shape.contains_point(axs[0].transData.transform((point[0], point[1]))):
            add_frame_for_axis(axs_1_pts, point[0], point[1], xlist_T, ylist_T)
            if STARTING_T_ANGLE > 90:
                point[0] -= 3 / 70  #TODO add or subtract based on angle
            elif STARTING_T_ANGLE < 90:
                point[0] += 3 / 70
            else:
                point[1] += 3 / 70
                continue
            m = np.tan(STARTING_T_ANGLE * np.pi / 180)
            point[1] = m * (point[0]) + STARTING_T_POSITION[1]
        #change starting_T_position_here

        xlist_K = []
        ylist_K = []
        for xval in np.linspace(np.cos(np.pi / 3) * 3 - 3, np.cos(np.pi / 3) * 3, 100):
            add_frame_for_axis(axs_2_pts, xval, np.sin(np.pi / 3) * 3 - 3, xlist_K, ylist_K)

        # slope is now sqrt(3)/3
        STARTING_T_POSITION = [-3, tan(30 * np.pi / 180) * 3 - 3]
        point = [STARTING_T_POSITION[0], STARTING_T_POSITION[1]]
        while T_shape.contains_point(axs[0].transData.transform((point[0], point[1]))):
            add_frame_for_axis(axs_1_pts, point[0], point[1], xlist_T, ylist_T)
            m = np.sqrt(3) / 3
            point[0] += 3 / 70
            point[1] = m * (point[0]) + (2*np.sqrt(3)-3)
        STARTING_T_POSITION = [xlist_T[-1], ylist_T[-1]]

        xlist_K_new = []
        ylist_K_new = []
        axs_2_pts_new, = axs[1].plot([], [], 'r-')  # 'r-' means red line
        for xval in np.linspace(np.cos(np.pi / 3) * 3, np.cos(np.pi / 3) * 3 - 3, 100):
            add_frame_for_axis(axs_2_pts_new, xval, np.sin(np.pi / 3) * 3 - 3, xlist_K_new, ylist_K_new)

        point = [STARTING_T_POSITION[0], STARTING_T_POSITION[1]]
        while T_shape.contains_point(axs[0].transData.transform((point[0], point[1]))):
            add_frame_for_axis(axs_1_pts, point[0], point[1], xlist_T, ylist_T)
            m = -1 * np.sqrt(3) / 3
            point[0] -= 3 / 70
            point[1] = m * (point[0] - STARTING_T_POSITION[0]) + STARTING_T_POSITION[1]
        STARTING_T_POSITION = [xlist_T[-1], ylist_T[-1]]

        for yval in np.linspace(np.sin(np.pi / 3) * 3 - 3, -3, 75):
            add_frame_for_axis(axs_2_pts_new, np.cos(np.pi / 3) * 3 - 3, yval, xlist_K_new, ylist_K_new)

        for yval in np.linspace(STARTING_T_POSITION[1], -3, 75):
            add_frame_for_axis(axs_1_pts, STARTING_T_POSITION[0], yval, xlist_T, ylist_T)

        axs_2_pts_new_new, = axs[1].plot([], [], 'k-')
        xlist_K_new_new = []
        ylist_K_new_new = []
        for yval in np.linspace(-3, np.sin(np.pi / 3) * 3 - 3, 100):
            add_frame_for_axis(axs_2_pts_new_new, np.cos(np.pi / 3) * 3 - 3, yval, xlist_K_new_new, ylist_K_new_new)

        for i in range(0, 100):
            writer.grab_frame()

        clip = VideoFileClip("trajectory.gif")
        clip.write_videofile("trajectory.mp4")