from Cells.Cell import Cell
from Guardians.Drax import Drax
from Guardians.Gamora import Gamora
from Guardians.Groot import Groot
from Guardians.Rocket import Rocket
from Guardians.StarLord import StarLord


class Player:

    def __init__(self, pid, sid, base_coord: Cell):
        self.__player_id = pid
        self.__socket_id = sid
        self.__connected = True
        self.__base_coordinates = base_coord
        self.__gamora = Gamora(self, base_coord, True)
        self.__groot = Groot(self, base_coord, True)
        self.__drax = Drax(self, base_coord, True)
        self.__rocket = Rocket(self, base_coord, True)
        self.__starlord = StarLord(self, base_coord, True)

        self.__base_coordinates.add_guardian_to_cell(self.get_guardian_by_type('Gamora'))
        self.__base_coordinates.add_guardian_to_cell(self.get_guardian_by_type('Rocket'))
        self.__base_coordinates.add_guardian_to_cell(self.get_guardian_by_type('Groot'))
        self.__base_coordinates.add_guardian_to_cell(self.get_guardian_by_type('Drax'))
        self.__base_coordinates.add_guardian_to_cell(self.get_guardian_by_type('StarLord'))

    def get_guardian_by_type(self, guardian_type: str):
        if guardian_type == 'Gamora':
            return self.__gamora
        elif guardian_type == 'Rocket':
            return self.__rocket
        elif guardian_type == 'Groot':
            return self.__groot
        elif guardian_type == 'Drax':
            return self.__drax
        elif guardian_type == 'StarLord':
            return self.__starlord
        else:
            return None

    def get_guardians(self):
        return {
            'Gamora': self.__gamora,
            'Rocket': self.__rocket,
            'Groot': self.__groot,
            'Drax': self.__drax,
            'StarLord': self.__starlord
        }

    def get_player_id(self):
        return self.__player_id

    def get_socket_id(self):
        return self.__socket_id

    def set_player_id(self, player_id):
        self.__player_id = player_id

    def set_socket_id(self, socket_id):
        if socket_id is None:
            self.set_connected(False)
        self.__socket_id = socket_id

    def is_connected(self):
        return self.__connected

    def set_connected(self, connected):
        self.__connected = connected

    def get_base_coordinates(self):
        return self.__base_coordinates
