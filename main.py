#!/usr/bin/env python3
# from Connection import Connection
# from Visualizer import Visualizer
from Parsing import Parsing
from Monitor import Monitor
import sys
# from Drone import Drone
# from Hub import Hub


def main() -> None:
    try:
        args = sys.argv
        if len(args) < 2:
            raise Exception("must execute with filename")
        elif len(args) > 2:
            raise Exception("one argument accepted")
        file = args[1]
    except Exception as e:
        return print(e)

    try:
        nb_drones, hub_d, connection_d = Parsing.parsing(file)
    except Exception as e:
        return print(e)
    monitor = Monitor()
    monitor.init(nb_drones, hub_d, connection_d)
    monitor.simulate(flag=False)
    monitor.visualize(save=False)


if __name__ == "__main__":
    main()
