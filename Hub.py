#!/usr/bin/env python3
from typing import Any
from Connection import Connection


class Hub():
    def __init__(self, hub_data: dict[str, Any]):
        self.category = hub_data['category']
        if hub_data['category'] == 'priority':
            self.cost = 1
        elif hub_data['category'] == 'restricted':
            self.cost = 3
        elif hub_data['category'] == 'blocked':
            self.cost = 1000
        else:
            self.cost = 2
        self.name = hub_data['name']
        self.coor = (hub_data['x'], hub_data['y'])
        self.zone = hub_data['zone']
        self.color = hub_data['color']
        self.max_drones = hub_data['max_drones']
        self.maxmax = hub_data['max_drones']
        self.connections: list[Connection] = list()
        self.distance = 100
        if hub_data['zone'] == 'blocked':
            self.distance = 1000
        self.prev = None
