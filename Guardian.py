# from Cells.Cell import Cell
# from Player import Player
from Feedback import Feedback


class Guardian:

    def __init__(self, belongs, init_coordinates, alive=True):
        self.belongs_to_player = belongs
        self.coordinates = init_coordinates
        self.__is_alive = alive
        self.__died_at = None
        self.__score = 0

    def update_cooldown(self):
        # called from environment, cold own is updated after every round
        return 0

    def mark_as_dead(self, round_no):
        # marks a player as dead
        self.__is_alive = False
        self.__died_at = round_no

        return Feedback("guardian_died", {"coordinates": self.coordinates})

    def is_alive(self):
        return self.__is_alive

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def get_coordinates(self):
        return self.coordinates

    def get_belongs_to_player(self):
        return self.belongs_to_player

    def get_died_at(self):
        return self.__died_at

    def get_score(self):
        return self.__score

    def add_score(self, amount):
        self.__score += amount
