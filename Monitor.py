#!/usr/bin/env python3
from Connection import Connection
from Visualizer import Visualizer
from Drone import Drone
# from typing import Any
from Hub import Hub


class Monitor():
    def __init__(self):
        self.drone = list()
        self.hub = dict()
        # self.start
        # self.end
        self.connection = list()

    def init(self, nb: int, hub: list[dict], connection: list[dict]):
        self.nb_drones = nb
        for d in range(nb):
            self.drone.append(Drone(d))
        for c in connection:
            self.connection.append(Connection(c))
        for h in hub:
            self.hub.update({h['name']: Hub(h)})
            if h['category'] == 'start':
                self.start = self.hub[h['name']]
            elif h['category'] == 'end':
                self.end = self.hub[h['name']]
            for w in self.connection:
                if w.z1 == h['name'] or h['name'] == w.z2:
                    self.hub[h['name']].connections.append(w)
        for connec in self.connection:
            connec.position(self.hub[connec.z1].coor, self.hub[connec.z2].coor)
            
    
    def find_connection(self, hub1: Hub, hub2: Hub) -> Connection:
        for c in self.connection:
            if c.z1 == hub1.name or c.z2 == hub1.name:
                if c.z2 == hub2.name or c.z1 == hub2.name:
                    return c
        return self.connection[0]


    def search_path(self):
        unknown = [self.hub[h] for h in self.hub
            if self.hub[h].zone != 'blocked']
        self.start.distance = 0

        while unknown:
            actual = min(unknown, key=lambda x: x.distance)
            unknown.remove(actual)
            for c in actual.connections:
                neighbour = self.hub[c.get_neighbour(actual.name)]
                if neighbour in unknown:
                    total = actual.distance + neighbour.cost
                    if neighbour.distance != 1000 and total < neighbour.distance:
                        neighbour.distance = total
                        neighbour.prev = actual

        now = self.end
        path = [now]
        while now != self.start:
            if path[-1].zone == "restricted":
                path.append(self.find_connection(now.prev, path[-1]))
            path.append(now.prev)
            now = now.prev
        path.reverse()
        # print(path)
        return path


    def finished(self):
        for d in self.drone:
            if d.active is True:
                return False
        return True


    def start_sim(self, path):
        for d in self.drone:
            d.coor = self.start.coor
            d.index = 0
        while not self.finished():
            for d in self.drone:
                d.path.append(d.coor)
                if d.active:
                    if path[d.index + 1].max_drones != 0:
                        d.coor = path[d.index + 1].coor
                        path[d.index + 1].max_drones -= 1
                        path[d.index].max_drones += 1
                        d.index += 1
                    if d.coor == self.end.coor:
                        d.active = False
        for d in self.drone:
            d.path.append(d.coor)

    def simulate(self):
        path = self.search_path()
        self.start_sim(path)


    def visualize(self, save: bool=True):
        visu = Visualizer()
        visu.generate(self.hub, self.connection,
            self.nb_drones, [d.path for d in self.drone])
        visu.show(save)
        