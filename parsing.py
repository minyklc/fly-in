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
    def count(data: str) -> int:
        tab = data.split(':')
        if not tab[0].startswith('nb_drones'):
            raise NameError('nb_drones paramater missing')
        nb = int(tab[1])
        if nb < 0:
            raise ValueError('nb_drones must be positive')
        return nb

    @staticmethod
    def hub_metadata(data: str, zone: str, color: str,
                     max: int, total: int,
                     category: str | None) -> tuple[str, str, int]:
        boool = [False, False, False]
        if '[' not in data:
            raise NameError('oups missing a bracket in hub definition!')
        meta = data.split('[')[1]
        if not meta.rstrip().endswith(']'):
            raise NameError('oups missing the other '
                            'bracket in hub definition!')
        meta = meta.rstrip().replace(']', '')
        metadata = meta.split(' ')
        for md in metadata:
            if '=' not in md:
                raise NameError('equal symbol missing')
            if md.startswith('zone'):
                if boool[0]:
                    raise NameError('two zone key are not accepted')
                zone = md.split('=')[1]
                zone.lstrip()
                if zone not in ['normal', 'blocked', 'restricted', 'priority']:
                    raise ValueError('metadata zone should be either '
                                     'normal, blocked, restricted or priority')
                if zone == 'blocked' and category is not None:
                    raise ValueError('start or end cannot be blocked zone')
                boool[0] = True
            elif md.startswith('color'):
                if boool[1]:
                    raise NameError('two color key are not accepted')
                color = md.split('=')[1]
                color.lstrip()
                boool[1] = True
            elif md.startswith('max_drones'):
                if boool[2]:
                    raise NameError('two max_drones key are not accepted')
                max = int(md.split('=')[1])
                if max < 0:
                    raise ValueError('max_drones must be a positive integer')
                if max < total and category is not None:
                    raise ValueError('start or end must handle '
                                     'at least the total number of drones')
                boool[2] = True
            else:
                raise NameError('unknown hub metadata key')
        return zone, color, max

    @staticmethod
    def new_hub(data: str, total: int,
                category: str | None = None) -> dict[str, Any]:
        hub = dict()
        zone = 'normal'
        color = 'none'
        max = 1
        name, x, y, *_ = data.split(' ')
        if '-' in name:
            raise NameError("hub name shouldn't contain dashes")
        hub.update({'name': name, 'x': int(x), 'y': int(y)})
        if len(data.split(' ')) > 3:
            zone, color, max = Parsing.hub_metadata(data, zone, color,
                                                    max, total, category)
        hub.update({'zone': zone, 'color': color,
                    'max_drones': max, 'category': 'hub'})
        return hub

    @staticmethod
    def hub(data: list[str], nb_drones: int) -> list[dict[str, Any]]:
        start: dict[str, Any] = dict()
        end: dict[str, Any] = dict()
        hub = list()
        i = 1
        while data[i] and not data[i].startswith('connection'):
            if data[i].startswith('start_hub'):
                if start:
                    raise ValueError('multiple start hub is not accepted')
                _, tmp = data[i].split(':')
                start = Parsing.new_hub(tmp.lstrip(),
                                        nb_drones, category='start')
                start.update({'category': 'start', 'max_drones': nb_drones})
                hub.append(start)
            elif data[i].startswith('end_hub'):
                if end:
                    raise ValueError('multiple end hub is not accepted')
                _, tmp = data[i].split(':')
                end = Parsing.new_hub(tmp.lstrip(), nb_drones, category='end')
                end.update({'category': 'end', 'max_drones': nb_drones})
                hub.append(end)
            elif data[i].startswith('hub'):
                _, tmp = data[i].split(':')
                hub.append(Parsing.new_hub(tmp.lstrip(), nb_drones))
            else:
                raise NameError('unknown hub keyname')
            i += 1
        return hub

    @staticmethod
    def checkname(name: list[str]) -> None:
        for n in name:
            if name.count(n) != 1:
                raise NameError('hub name should be unique')

    @staticmethod
    def checkzone(name: str, data: list[str]) -> None:
        if data.count(name) == 0:
            raise NameError('any zone name should be already defined as a hub')

    @staticmethod
    def checkconnection(data: list[dict[str, Any]]) -> None:
        connections = [{d['z1'], d['z2']} for d in data]
        for c in connections:
            if connections.count(c) > 1:
                raise ValueError("can't have duplicate connection")

    @staticmethod
    def con_metadata(data: str) -> int:
        link = 1
        bol = False
        if '[' not in data:
            raise NameError('oups missing a bracket in hub definition')
        _, meta = data.split('[')
        if not meta.rstrip().endswith(']'):
            raise NameError('oups missing the other bracket in hub definition')
        meta = meta.rstrip().replace(']', '')
        metadata = meta.split(' ')
        for md in metadata:
            if '=' not in md:
                raise NameError('equal symbol missing')
            if md.startswith('max_link_capacity'):
                if bol:
                    raise NameError('two zone key are not accepted')
                _, tmp = md.split('=')
                link = int(tmp)
                if link < 0:
                    raise ValueError('max_link_capacity '
                                     'must be a positive integer')
                bol = True
            else:
                raise NameError('unknown hub metadata key')
        return link

    @staticmethod
    def new_connection(data: str, name: list[str]) -> dict[str, Any]:
        connec = dict()
        max_link = 1
        tmp = data.split(' ')
        z1, z2 = tmp[0].split('-')
        Parsing.checkzone(z1, name)
        Parsing.checkzone(z2, name)
        if z1 == z2:
            raise NameError('connection should not be among the same hub')
        if len(tmp) >= 2:
            max_link = Parsing.con_metadata(data)
        connec.update({'z1': z1, 'z2': z2, 'max_link_capacity': max_link})
        return connec

    @staticmethod
    def connection(data: list[str], name: list[str]) -> list[dict[str, Any]]:
        i = int()
        conex = list()
        for index, d in enumerate(data):
            if d.startswith('connection'):
                i = index
                break
        if not i:
            raise NameError('other key than "connection" found')
        while i < len(data):
            if not data[i].startswith('connection'):
                raise NameError('other key than "connection" found')
            _, tmp = data[i].split(':')
            conex.append(Parsing.new_connection(tmp.lstrip(), name))
            i += 1
        return conex

    @staticmethod
    def parsing(file: str) -> tuple[int, list[dict[str, Any]],
                                    list[dict[str, Any]]]:
        data = Parsing.read(file)
        nb_drones = Parsing.count(data[0])
        hub = Parsing.hub(data, nb_drones)
        name = [h['name'] for h in hub]
        Parsing.checkname(name)
        connection = Parsing.connection(data, name)
        Parsing.checkconnection(connection)
        return nb_drones, hub, connection


if __name__ == "__main__":
    Parsing.read('maps/easy/01_linear_path.txt')
