#!/usr/bin/env python3


class Drone():
    def __init__(self, nb: int):
        self.n = nb
        self.restricted = False
        self.path = list()
        self.active = True
        #self.coor
