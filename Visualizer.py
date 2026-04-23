#!/usr/bin/env python3
from Connection import Connection
from typing import Any

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.animation import FuncAnimation


class Visualizer():
    def __init__(self) -> None:
        self.smooth: list[Any] = list()
        self.drone: list[Any] = list()
        self.turn = 0
        self.legend_turn: Any = None

    def update_turn(self) -> None:
        if self.legend_turn is not None:
            self.legend_turn[0].set_label(f'Turn: {self.turn}')
            self.ax.legend(
                            handles=self.legend_turn,
                            loc='upper left',
                            framealpha=0.8
                        )

    def update(self, frame: int) -> tuple[Any]:
        turn = frame // 50
        if turn != self.turn:
            self.turn = turn
            self.update_turn()

        for i in range(len(self.drone)):
            x, y = self.smooth[i][frame]
            self.drone[i].set_data([x], [y])
        return self.drone[0],

    @staticmethod
    def duplicate(path: list[tuple[int, int]]) -> list[tuple[int, int]]:
        new = list()
        for p in path:
            new.extend([p, p])
        return new

    @staticmethod
    def smooth_path(hubs: Any, step: int = 25) -> Any:
        res = list()
        for i in range(len(hubs) - 1):
            for t in np.linspace(0, 1, step, endpoint=False):
                res.append(hubs[i] + (hubs[i + 1] - hubs[i]) * t)
        return np.array(res)

    def map(self, hub: dict[str, Any], connec: list[Connection],
            ax: Any) -> Any:
        hx = [hub[h].coor[0] for h in hub]
        hy = [hub[h].coor[1] for h in hub]
        self.min = min(hx)
        self.max = max(hx)
        ax.set_xlim(self.min - 2, self.max + 2)
        ax.set_ylim(min(hy) - 2, max(hy) + 2)
        for h in hub:
            x = hub[h].coor[0]
            y = hub[h].coor[1]
            try:
                ax.scatter(x, y, c=hub[h].color, s=500, edgecolors='black')
            except ValueError:
                ax.scatter(x, y, c='none', s=500, edgecolors='black')
        for c in connec:
            cx = [hub[c.z1].coor[0], hub[c.z2].coor[0]]
            cy = [hub[c.z1].coor[1], hub[c.z2].coor[1]]
            ax.plot(cx, cy, color='black')
        return ax

    def add_path(self, path: list[list[tuple[int, int]]]) -> None:
        for p in path:
            pathpath = self.duplicate(p)
            tmp = np.array(pathpath, dtype=float)
            smooth = self.smooth_path(tmp)
            self.smooth.append(smooth)

    def create_drone(self, nb: int, ax: Any) -> None:
        for i in range(nb):
            drone, = ax.plot([], [], 'yo', markersize=10)
            self.drone.append(drone)

    def generate(self, hub: dict[str, Any], connec: list[Connection],
                 nb_drones: int, paths: list[list[Any]]) -> None:
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        ax = self.map(hub, connec, ax)

        # gérer les paths
        self.add_path(paths)

        # créer les drones
        turn = Line2D([], [], color='none', label=f'Turn : {self.turn}')
        self.legend_turn = [turn]
        ax.legend(handles=self.legend_turn, loc='upper left', framealpha=0)
        self.create_drone(nb_drones, ax)

        # speed = 5 - (((self.max - self.min) / 3) * 1.5)
        speed = 1 + 4 / (1 + 0.5 * abs(self.max - self.min))
        # print(speed)
        # speed = 1

        ani = FuncAnimation(fig, self.update, frames=len(self.smooth[0]),
                            interval=speed)
        self.ani = ani

    def show(self, save: bool) -> None:
        if save:
            self.ani.save("flyin.gif", writer="pillow", fps=50)
        plt.show()
