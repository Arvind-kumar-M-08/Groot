from Cells.Cell import Cell
from Guardian import Guardian


# from Player import Player


class StarLord(Guardian):
    MAX_HEALTH = 100

    def __init__(self, belongs, init_coordinates: Cell, alive=True):
        self.__health = 100
        self.__attack_damage = 35
        self.__vision = 5
        self.__speed = 2
        self.__cooldown = 0
        super().__init__(belongs, init_coordinates, alive)

    def special_ability(self):
        # See Through Walls, upto range one,
        # i.e one block behind a wall can be seen
        return 0

    def get_health(self):
        return self.__health

    def set_health(self, health, round_no):
        if self.is_alive():
            self.__health = health
            if self.__health < 0:
                self.__health = 0
            elif self.__health > 100:
                self.__health = 100

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
        return "StarLord"

    def __repr__(self):
        return "StarLord( " + self.coordinates.__repr__() + " " + str(self.__health) + " " + str(self.__cooldown) + " )"
