#!/usr/bin/env python3
from parsing import Parsing


def main():
    try:
        data = Parsing.read('maps/easy/01_linear_path.txt')
        nb_drones = Parsing.count(data[0])
        start, end, hub = Parsing.hub(data)
        name = [h['name'] for h in hub]
        name.append(start['name'])
        name.append(end['name'])
        Parsing.checkname(name)
        connection = Parsing.connection(data, name)
        Parsing.checkconnection(connection)
        print(data, nb_drones, start, end, hub, connection, sep='\n\n')
    except Exception as e:
        print(e)


if __name__ == "__main__":
	main()
