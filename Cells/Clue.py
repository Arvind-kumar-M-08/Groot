import random

from Cells.Cell import Cell
from Feedback import Feedback
from InfinityStone import InfinityStone
from Player import Player

type_of_clue = ["enemy_seen", "node_Optimal_path"]


class Clue(Cell):
    def __init__(self, cell: Cell, cell_type=None):
        if cell_type is None:
            super().__init__(cell.get_coordinates(), cell.get_guardians_present(), cell.get_neighbour_cells(),
                             Cell.Clue)
        else:
            super().__init__(cell.get_coordinates(), cell.get_guardians_present(), cell.get_neighbour_cells(),
                             cell_type)
        self.type = random.choice(type_of_clue)  # equal probability
        self.is_clue_active = True
        self.give_clue_to_player = []

    def enemy_location(self, opponentPlayer: Player):
        return_dict = {}
        for troop_name, troop in opponentPlayer.get_guardians().items():
            if troop.is_alive():
                return_dict[troop_name] = troop.get_coordinates().get_coordinates()
        return {"clue_type": "get_enemy_locations", "data": return_dict}

    def get_best_direction(self, infinityStone: InfinityStone, guardian):
        if self.get_coordinates()[1] == infinityStone.get_coordinates().get_coordinates()[1]:
            direction_slope = (self.get_coordinates()[0] - infinityStone.get_coordinates().get_coordinates()[0])
            if direction_slope > 0:
                return {"clue_type": "get_direction_to_infinity_stone", "direction": "inf",
                        'guardian': guardian.get_type()}
            else:
                return {"clue_type": "get_direction_to_infinity_stone", "direction": "-inf",
                        'guardian': guardian.get_type()}
        if self.get_coordinates()[0] == infinityStone.get_coordinates().get_coordinates()[0]:
            direction_slope = (self.get_coordinates()[1] - infinityStone.get_coordinates().get_coordinates()[1])
            if direction_slope > 0:
                return {"clue_type": "get_direction_to_infinity_stone", "direction": "0",
                        'guardian': guardian.get_type()}
            else:
                return {"clue_type": "get_direction_to_infinity_stone", "direction": "-0",
                        'guardian': guardian.get_type()}

        direction_slope = (self.get_coordinates()[0] - infinityStone.get_coordinates().get_coordinates()[0]) / (
                self.get_coordinates()[1] - infinityStone.get_coordinates().get_coordinates()[1])
        return {"clue_type": "get_direction_to_infinity_stone", "direction": str(round(direction_slope, 2)),
                'guardian': guardian.get_type()}

    def get_clue(self, opponentPlayer: Player, infinityStone: InfinityStone, guardian):
        two_players_present = False
        if opponentPlayer not in self.give_clue_to_player:
            if self.is_clue_active:
                for guardain_present in self.get_guardians_present():
                    if guardain_present.get_belongs_to_player() == opponentPlayer:
                        two_players_present = True
                        break
                if self.type == "enemy_seen" and False:
                    self.give_clue_to_player.append(opponentPlayer)
                    return Feedback("clue", self.enemy_location(opponentPlayer)), two_players_present
                elif self.type == "node_Optimal_path" or True:
                    self.give_clue_to_player.append(opponentPlayer)
                    return Feedback("clue", self.get_best_direction(infinityStone, guardian)), two_players_present
                else:
                    return None, None
            else:
                return None, None
        else:
            return None, None

    def get_clue_type(self):
        return self.type

    def get_clue_active(self):
        return self.is_clue_active

    def set_clue_to_inactive(self):
        self.is_clue_active = False
