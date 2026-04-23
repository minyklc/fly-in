#!/usr/bin/env python3
from typing import Any


class Connection():
    def __init__(self, connec_data: dict[str, Any]):
        self.z1 = connec_data['z1']
        self.z2 = connec_data['z2']
        self.max_drones = connec_data['max_link_capacity']
        self.max_link = connec_data['max_link_capacity']
        self.zone = "connection"

    def get_neighbour(self, name: str) -> Any:
        if name == self.z1:
            return self.z2
        return self.z1

    def position(self, coor_z1: tuple[int, int],
                 coor_z2: tuple[int, int]) -> None:
        x = (coor_z1[0] + coor_z2[0]) / 2
        y = (coor_z1[1] + coor_z2[1]) / 2
        self.coor = (x, y)

    # @staticmethod
    # def create_connections(data: list[dict]) -> list[Any]:
    #     connections = list()
    #     for d in data:
    #         connections.append(Connection(d))
    #     return connections
