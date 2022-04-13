import random

from .Cell import Cell


class Teleporter(Cell):
    def __init__(self, cell: Cell):
        super().__init__(cell.get_coordinates(), cell.get_guardians_present(), cell.get_neighbour_cells(),
                         Cell.Teleporter)

    def generate_destination(self, goal_cell: Cell, graph) -> Cell:
        new_x = random.randint(max(min(self.get_coordinates()[0],
                                       (2 * goal_cell.get_coordinates().get_coordinates()[0] -
                                        self.get_coordinates()[
                                            0])),
                                   0),
                               min(max(self.get_coordinates()[0],
                                       (2 * goal_cell.get_coordinates().get_coordinates()[0] -
                                        self.get_coordinates()[
                                            0])),
                                   len(graph[0]) - 1)
                               )
        new_y = random.randint(max(min(self.get_coordinates()[1],
                                       (2 * goal_cell.get_coordinates().get_coordinates()[1] -
                                        self.get_coordinates()[
                                            1])),
                                   0),
                               min(max(self.get_coordinates()[1],
                                       (2 * goal_cell.get_coordinates().get_coordinates()[1] -
                                        self.get_coordinates()[
                                            1])),
                                   len(graph) - 1)

                               )
        return graph[new_x][new_y]
