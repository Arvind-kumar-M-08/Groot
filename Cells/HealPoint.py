from Cells.Cell import Cell
from Feedback import Feedback


class HealPoint(Cell):
    def __init__(self, cell: Cell):
        super().__init__(cell.get_coordinates(), cell.get_guardians_present(), cell.get_neighbour_cells(),
                         Cell.HealPoint)

        self.__rounds_present = None

    def get_rounds_present(self):
        return self.__rounds_present

    def remove_from_rounds_present(self, guardian):
        guardian_key = (guardian.get_type(), guardian.get_belongs_to_player().get_player_id())

        if guardian_key in self.__rounds_present:
            del self.__rounds_present[(guardian.get_type(), guardian.get_belongs_to_player().get_player_id())]

    def add_to_rounds_present(self, guardian):
        if not self.__rounds_present:
            self.__rounds_present = {}
        if guardian in self.__rounds_present:
            self.__rounds_present[(guardian.get_type(), guardian.get_belongs_to_player().get_player_id())] += 1
        else:
            self.__rounds_present[(guardian.get_type(), guardian.get_belongs_to_player().get_player_id())] = 1

    def update_rounds_present(self, current_round_no):
        if self.__rounds_present:
            for guardian in self.get_guardians_present():
                guardian_key = (guardian.get_type(), guardian.get_belongs_to_player().get_player_id())
                if guardian_key in self.__rounds_present:
                    self.__rounds_present[guardian_key] += 1
                else:
                    self.__rounds_present[guardian_key] = 1

                if self.__rounds_present[guardian_key] >= 5 and guardian.get_health() < 300:
                    guardian.set_health(300, current_round_no)
                    return Feedback('healpoint_used', {'guardian': guardian.get_type()})
                elif self.__rounds_present[guardian_key] < 5:
                    return None
                else:
                    return None
        else:
            self.__rounds_present = {}
            return None
