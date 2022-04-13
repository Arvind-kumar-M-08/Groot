from Cells.Cell import Cell
from Feedback import Feedback


class InfinityStone:
    def __init__(self, coordinates: Cell):
        self.__coordinates = coordinates
        self.__guardian = None
        self.__is_returned_to_base = False

    def update_coordinates(self):
        if not self.__is_returned_to_base:
            if self.__guardian is not None:
                if self.__guardian.is_alive():
                    if self.__guardian.get_coordinates() != self.__coordinates:
                        self.__coordinates = self.__guardian.get_coordinates()
                        return Feedback("infinity_stone_moved"), Feedback("guardian_moved_infinity_stone", {
                            "guardian_coordinates": self.__guardian.get_coordinates().get_coordinates(),
                            "guardian": self.__guardian.get_type()

                        }), self.__guardian.get_belongs_to_player().get_player_id()
                    return None, None, None
                else:
                    prev_guardian = self.__guardian
                    self.__guardian = None

                    return Feedback("infinity_stone_dropped"), Feedback(
                        "guardian_died_and_infinity_stone_dropped", {"guardian": prev_guardian.get_type()}), \
                           prev_guardian.get_belongs_to_player().get_player_id()
            else:
                player1_present = False
                player2_present = False
                counter = 0
                while counter < len(self.__coordinates.get_guardians_present()):
                    if player1_present and player2_present:
                        break

                    if self.__coordinates.get_guardians_present()[counter] == "player1":
                        player1_present = True
                    elif self.__coordinates.get_guardians_present()[counter] == "player2":
                        player2_present = True
                    counter += 1

                if not (player1_present and player2_present) and len(self.__coordinates.get_guardians_present()) > 0:

                    if self.__coordinates.get_guardians_present()[0].is_alive():
                        self.__guardian = self.__coordinates.get_guardians_present()[0]
                        return Feedback("infinity_stone_picked_up"), Feedback("guardian_picked_up_infinity_stone", {
                            "guardian": self.__guardian.get_type()}), \
                               self.__guardian.get_belongs_to_player().get_player_id()
                    else:
                        print("Removed form Infinity stone -2323")
                        self.__coordinates.remove_guardian_from_cell(self.__coordinates.get_guardians_present()[0])
                        return None, None, None
                else:
                    self.__guardian = None
                    return None, None, None

    def get_coordinates(self):
        return self.__coordinates

    def get_guardian(self):
        return self.__guardian

    def set_guardian(self, guardian):
        self.__guardian = guardian

    def is_returned_to_base(self):
        return self.__is_returned_to_base

    def set_returned_to_base(self, is_returned_to_base):
        self.__is_returned_to_base = is_returned_to_base
