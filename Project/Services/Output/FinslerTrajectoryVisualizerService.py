import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
from matplotlib.patches import Polygon


def func(x):
    return np.sin(x) * 3

def draw_T():
    square = plt.Rectangle((-3, -3), 6, 6, fc='white', ec="red")
    axs[0].add_patch(square)

def draw_K():
    pts = np.array([[3, 3], [2, 5], [5, np.sqrt(5 ** 2 - 2 ** 2)]])
    p = Polygon(pts)
    axs[1].add_patch(p)


def add_frame_for_axis(axs_pts, xval, yval):
    xlist.append(xval)
    ylist.append(yval)
    axs_pts.set_data(xlist, ylist)
    writer.grab_frame()


if __name__ == '__main__':
    fig, axs = plt.subplots(2, figsize=(5, 10))

    axs_1_pts, = axs[0].plot([], [], 'k-')
    axs_2_pts, = axs[1].plot([], [], 'k-')

    for ax in axs:
        ax.set_xlim([-5, 5])
        ax.set_ylim([-5, 5])

    metadata = dict(title='Movie', artist='Hunter')
    writer = PillowWriter(fps=30, metadata=metadata)

    draw_T()
    draw_K()


    with writer.saving(fig, 'sinWave.gif', 100):
        xlist = []
        ylist = []
        for xval in np.linspace(-5, 5, 70):
            add_frame_for_axis(axs_1_pts, xval, func(xval))
        xlist = []
        ylist = []
        for xval in np.linspace(-5, 5, 70):
            add_frame_for_axis(axs_2_pts, xval, -1 * func(xval))
