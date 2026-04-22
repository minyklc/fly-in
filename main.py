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
        connection_d = Parsing.parsing('maps/challenger/01_the_impossible_dream.txt')
        # connection_d = Parsing.parsing('maps/medium/03_priority_puzzle.txt')
    except Exception as e:
        return print(e)
    monitor = Monitor()
    monitor.init(nb_drones, hub_d, connection_d)
    monitor.simulate()
    monitor.visualize(save=False)


if __name__ == "__main__":
	main()
