#!/usr/bin/env python3
from Connection import Connection
from Hub import Hub


class Drone():
    def __init__(self, nb: int):
        self.id = nb
        self.restricted = False
        self.path: list[Connection | Hub] = list()
        self.active = True
        # self.coor = start.coor
        # self.index = 0
