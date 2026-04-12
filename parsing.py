#!/usr/bin/env python3
from typing import Any


class Parsing():

    @staticmethod
    def read(file: str) -> list[Any]:
        tab = []
        try:
            with open(file, 'r') as f:
                for line in f:
                    if not line.startswith('#') and not line.isspace():
                        tab.append(line.rstrip('\n'))
        except FileNotFoundError:
            print('[error]: file name')
        finally:
            return tab
	
    @staticmethod
    def count(data: str):
        tab = data.split(':')
        if not tab[0].startswith('nb_drones'):
            raise NameError('nb_drones paramater missing')
        return int(tab[1])
    
    @staticmethod
    def hub_metadata(data: str, zone: str, color: str, max: int) -> tuple[str, str, int]:
        return zone, color, max

    @staticmethod
    def checkname(data: str):
        ...

    @staticmethod
    def start_hub(data: str) -> dict:
        start = dict()
        zone = 'normal'
        color = 'none'
        max = 1
        name, x, y = data.split(' ')
        Parsing.checkname(name)
        start.update({'name': name, 'x': int(x), 'y': int(y)})
        if len(data.split(' ')) > 3:
            zone, color, max = Parsing.hub_metadata(data, zone, color, max)
        start.update({'zone': zone, 'color': color, 'max_drones': max})
        return start
        
    
    @staticmethod
    def end_hub(data: str) -> dict:
        ...
    
    @staticmethod
    def new_hub(data: str) -> dict:
        ...
    
    @staticmethod
    def hub(data: list[str]):
        start = dict()
        end = dict()
        hub = list()
        i = 1
        while data[i] and not data[i].startswith('connection'):
            if data[i].startswith('start_hub'): 
                if start:
                    raise ValueError('multiple start hub is not accepted')
                _, tmp = data[i].split(':')
                start = Parsing.start_hub(tmp)
            elif data[i].startswith('end_hub'): 
                if end:
                    raise ValueError('multiple end hub is not accepted')
                _, tmp = data[i].split(':')
                end = Parsing.end_hub(tmp)
            elif data[i].startswith('hub'):
                _, tmp = data[i].split(':')
                hub.append(Parsing.new_hub(tmp))
            else:
                raise NameError('unknown hub keyname')
            i += 1
        return start, end, hub
                
            


if __name__ == "__main__":
	Parsing.read('maps/easy/01_linear_path.txt')
