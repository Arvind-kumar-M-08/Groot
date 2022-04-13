from Cells.Cell import Cell
from Guardian import Guardian


class Gamora(Guardian):
    MAX_HEALTH = 125

    def __init__(self, belongs, init_coordinates: Cell, alive=True):
        self.__health = 125
        self.__attack_damage = 50
        self.__vision = 2
        self.__speed = 2
        self.__cooldown = 0
        super().__init__(belongs, init_coordinates, alive)

    def special_ability(self):
        # First check self.cooldown
        # then do whatever is required
        # JUMP anywhere within the radius
        return 0

    def set_health(self, health, round_no):
        if self.is_alive():
            self.__health = health
            if self.__health < 0:
                self.__health = 0
            elif self.__health > 125:
                self.__health = 125

            if self.__health <= 0:
                return self.mark_as_dead(round_no)
            return None
        return None

    def get_health(self):
        return self.__health

    def get_attack_damage(self):
        return self.__attack_damage

    def get_vision(self):
        return self.__vision

    def get_speed(self):
        return self.__speed

    def get_cooldown(self):
        return self.__cooldown

    def set_cooldown(self, round_no):
        self.__cooldown = 3 + round_no

    def update_cooldown(self):
        if self.__cooldown > 0:
            self.__cooldown -= 1

    def get_type(self):
        return "Gamora"

    def __repr__(self):
        return "Gamora( " + self.coordinates.__repr__() + " " + str(self.__health) + " " + str(self.__cooldown) + " )"
