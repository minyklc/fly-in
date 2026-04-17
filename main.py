#!/usr/bin/env python3
# from Connection import Connection
# from Visualizer import Visualizer
from Parsing import Parsing
from Monitor import Monitor
# from Drone import Drone
# from Hub import Hub


def main() -> None:
    try:
        nb_drones, hub_d, \
        connection_d = Parsing.parsing('maps/medium/01_dead_end_trap.txt')
        # print(nb_drones_d, hub_d, connection_d, sep='\n\n')
    except Exception as e:
        return print(e)
    monitor = Monitor()
    monitor.init(nb_drones, hub_d, connection_d)
    monitor.simulate()
    monitor.visualize(save=True)


if __name__ == "__main__":
	main()
