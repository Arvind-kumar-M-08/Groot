from Cells.Cell import Cell
from Guardian import Guardian


# from Player import Player


class Groot(Guardian):
    MAX_HEALTH = 200

    def __init__(self, belongs, init_coordinates: Cell, alive=True):
        self.__health = 200
        self.__attack_damage = 25
        self.__vision = 2
        self.__speed = 1
        self.__cooldown = 0
        super().__init__(belongs, init_coordinates, alive)

    def special_ability(self, round_no):
        self.set_health(self.get_health() + 5, round_no)

    def get_health(self):
        return self.__health

    def set_health(self, health, round_no):
        if self.is_alive():
            self.__health = health
            if self.__health < 0:
                self.__health = 0
            elif self.__health > 200:
                self.__health = 200

            if self.__health <= 0:
                return self.mark_as_dead(round_no)
            return None
        return None

    def get_attack_damage(self):
        return self.__attack_damage

    def get_vision(self):
        return self.__vision

    def get_speed(self):
        return self.__speed

    def get_cooldown(self):
        return self.__cooldown

    def set_cooldown(self):
        self.__cooldown = 0

    def update_cooldown(self):
        if self.__cooldown > 0:
            self.__cooldown -= 1

    def get_type(self):
        return "Groot"

    def __repr__(self):
        return "Groot( " + self.coordinates.__repr__() + " " + str(self.__health) + " " + str(self.__cooldown) + " )"
