#!/usr/bin/env python3
from parsing import Parsing


def main():
	try:
		data = Parsing.read('maps/easy/01_linear_path.txt')
		nb_drones = Parsing.count(data[0])
		start, end, hub = Parsing.hub(data)
		print(data, nb_drones)
	except Exception as e:
		print(e)


if __name__ == "__main__":
	main()