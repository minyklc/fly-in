#!/usr/bin/env python3


class Connection():
    def __init__(self, connec_data):
        self.z1 = connec_data['z1']
        self.z2 = connec_data['z2']
        self.max_link = connec_data['max_link_capacity']

    def get_neighbour(self, name: str):
        if name == self.z1:
            return self.z2
        return self.z1

    # @staticmethod
    # def create_connections(data: list[dict]) -> list[Any]:
    #     connections = list()
    #     for d in data:
    #         connections.append(Connection(d))
    #     return connections
