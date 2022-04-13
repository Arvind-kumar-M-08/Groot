from Feedback import Feedback
from InfinityStone import InfinityStone
from Player import Player


class State:
    # This class is data given for users.  for now penality score, feedback, movegen, player's troops info.
    def __init__(self, movegen: dict, feedback, penalty_score, round_no, player: Player,
                 infinityStone: InfinityStone) -> None:
        self.__feedback = feedback
        self.__penalty_score = penalty_score
        self.__round_no = round_no
        self.__movegen = movegen
        self.__player = player
        self.__infinityStone = infinityStone

    def get_movegen(self):
        return self.__movegen

    def get_feedback(self):
        return self.__feedback

    def get_penality_score(self):
        return self.__penalty_score

    def json(self):
        movegen_as_json = {}
        for troop_name, troop in self.__movegen.items():
            neighbours = []
            if troop_name == "StarLord":
                starlord_list = []
                for side in troop[1]:
                    side_list = []
                    for curr_cell in side:
                        side_list.append(curr_cell.get_coordinates())
                    starlord_list.append(side_list)

                starLord_vision = Feedback("star_lord_special_power", {"special_vision": starlord_list})
                self.__feedback.append(starLord_vision)
                troop = troop[0]

            for cell_list in troop:
                side = []
                for cell in cell_list:
                    guardian_present_list = []
                    for i in cell.get_guardians_present():
                        if i.get_belongs_to_player().get_player_id() == self.__player.get_player_id():
                            data = {
                                "belongs_to": 'you',
                                "guardian_name": i.get_type()
                            }
                            guardian_present_list.append(data)
                        else:
                            data = {
                                "belongs_to": 'opponent',
                                "guardian_name": i.get_type()
                            }
                            guardian_present_list.append(data)
                    side.append({"coordinates": str(cell.get_coordinates()),
                                 "cell_type": cell.get_cell_type(),
                                 "is_powerStone_present": str(cell.get_coordinates(
                                 ) == self.__infinityStone.get_coordinates()),
                                 'guardians_present': guardian_present_list})

                neighbours.append(side)
            #
            guardian = self.__player.get_guardian_by_type(troop_name)

            guardian_present_list = []
            for i in guardian.get_coordinates().get_guardians_present():
                if i.get_belongs_to_player().get_player_id() == self.__player.get_player_id():
                    data = {
                        "belongs_to": 'you',
                        "guardian_name": i.get_type()
                    }
                    guardian_present_list.append(data)
                else:
                    data = {
                        "belongs_to": 'opponent',
                        "guardian_name": i.get_type()
                    }
                    guardian_present_list.append(data)

            current_cell = {"coordinates": str(guardian.get_coordinates().get_coordinates()),
                            "cell_type": guardian.get_coordinates().get_cell_type(),
                            "is_powerStone_present": str(guardian.get_coordinates(
                            ) == self.__infinityStone.get_coordinates()),
                            'guardians_present': guardian_present_list}

            movegen_as_json[troop_name] = {"health": guardian.get_health(), "cooldown": guardian.get_cooldown(),
                                           "current_cell": current_cell, "neighbour_cells": neighbours}

        feedback_as_json = []
        for feed in self.__feedback:
            feedback_as_json.append(feed.json())

        return {
            "movegen": movegen_as_json,
            "feedback": feedback_as_json,
            "penalty_score": self.__penalty_score,
            "round_no": self.__round_no
        }
