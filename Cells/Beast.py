from Cells.Cell import Cell
from Cells.Clue import Clue
from Player import Player


class Beast(Clue):
    def __init__(self, cell: Cell):
        super().__init__(cell, Cell.Beast)
        self.__damage = 25

    def update_health(self, player: Player, opponent: Player, infinity_stone, round_no):
        if self.get_clue_active():
            guardian = self.get_guardians_present()[0]
            counter = 0
            while guardian.get_belongs_to_player() != player:
                guardian = self.get_guardians_present()[counter]
                counter += 1
            if guardian.belongs_to_player == player:
                if opponent not in self.give_clue_to_player:
                    two_guardians_present = False
                    for guardian_present in self.get_guardians_present():
                        if guardian_present.belongs_to_player == opponent:
                            two_guardians_present = True
                            break
                    reduce_health = guardian.set_health(guardian.get_health() - self.__damage, round_no)
                    if reduce_health is not None:
                        self.give_clue_to_player.append(opponent)
                        return reduce_health, two_guardians_present
                    else:
                        return self.get_clue(opponent, infinity_stone, guardian)
                else:
                    return None, None
            else:
                return None, None
