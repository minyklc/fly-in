#!/usr/bin/env python3
from Connection import Connection
from typing import Any

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Visualizer():
    def __init__(self):
        self.smooth = list()
        self.drone = list()

    def update(self, frame: int):
        for i in range(len(self.drone)):
            x, y = self.smooth[i][frame]
            self.drone[i].set_data([x], [y])
        return self.drone[0],
    
    @staticmethod
    def duplicate(path):
        new = list()
        for p in path:
            new.extend([p, p])
        return new

    @staticmethod
    def smooth_path(hubs, step=50):
        res = list()
        for i in range(len(hubs) - 1):
            for t in np.linspace(0, 1, step, endpoint=False):
                res.append(hubs[i] + (hubs[i + 1] - hubs[i]) * t)
        return np.array(res)

    def map(self, hub: dict, connec: list[Connection], ax: Any):
        hx = [hub[h].coor[0] for h in hub]
        hy = [hub[h].coor[1] for h in hub]
        ax.set_xlim(min(hx) - 2, max(hx) + 2)
        ax.set_ylim(min(hy) - 2, max(hy) + 2)
        for h in hub:
            x = hub[h].coor[0]
            y = hub[h].coor[1]
            ax.scatter(x, y, c=hub[h].color, s=500, edgecolors='black')
        for c in connec:
            cx = [hub[c.z1].coor[0], hub[c.z2].coor[0]]
            cy = [hub[c.z1].coor[1], hub[c.z2].coor[1]]
            ax.plot(cx, cy, color='black')
        return ax

    def add_path(self, path: list[list[tuple]]):
        for p in path:
            pathpath = self.duplicate(p)
            tmp = np.array(pathpath, dtype=float)
            smooth = self.smooth_path(tmp)
            self.smooth.append(smooth)
            # print(smooth)

    def create_drone(self, nb: int, ax: Any):
        for i in range(nb):
            drone, = ax.plot([], [], 'yo', markersize=10, label='Drone')
            self.drone.append(drone)

    def generate(self, hub: dict, connec: list[Connection], nb_drones: int, paths: list[list]):
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        ax = self.map(hub, connec, ax)

        #gérer les paths
        self.add_path(paths)

        #créer les drones
        self.create_drone(nb_drones, ax)

        # ax.legend()
        ani = FuncAnimation(fig, self.update, frames=len(self.smooth[0]), interval=20)
        self.ani = ani

    def show(self, save: bool):
        if save:
            self.ani.save("flyin.gif", writer="pillow", fps=50)
        plt.show()
