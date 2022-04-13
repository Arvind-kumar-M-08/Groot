class Cell:
    Normal = 'Normal'
    Teleporter = 'Teleporter'
    Clue = 'Clue'
    HealPoint = 'HealPoint'
    Beast = 'Beast'

    def __init__(self, coordinates, guardian_present=[], neighbour_cells=[], cell_type=Normal):
        self.__coordinates = coordinates
        self.__guardian_present = guardian_present.copy()  # This should have the guardian sub class object of the
        # guardian
        # present in the cell
        self.__neighbour_cells = neighbour_cells.copy()

        if cell_type == Cell.Normal:
            self.__cell_type = Cell.Normal
        elif cell_type == Cell.Teleporter:
            self.__cell_type = Cell.Teleporter
        elif cell_type == Cell.Clue:
            self.__cell_type = Cell.Clue
        elif cell_type == Cell.HealPoint:
            self.__cell_type = Cell.HealPoint
        elif cell_type == Cell.Beast:
            self.__cell_type = Cell.Beast
        else:
            raise (ValueError("Invalid cell type"))

    def add_neighbour_cell(self, cell: 'Cell'):
        if cell not in self.__neighbour_cells:
            self.__neighbour_cells.append(cell)

    def remove_neighbour_cell(self, cell: 'Cell'):
        if cell in self.__neighbour_cells:
            self.__neighbour_cells.remove(cell)

    def get_neighbour_cells(self):
        return self.__neighbour_cells

    def get_coordinates(self):
        return self.__coordinates

    def get_is_guardian_present(self):
        return True if len(self.__guardian_present) > 0 else False

    def add_guardian_to_cell(self, guardian):  # this guardian should be of the type Drax, Gamora etc

        self.__guardian_present.append(guardian)
        if self.get_cell_type() == Cell.HealPoint:
            self.add_to_rounds_present(guardian)

    def remove_guardian_from_cell(self, guardian):
        if guardian in self.__guardian_present:
            self.__guardian_present.remove(guardian)
            if self.get_cell_type() == Cell.HealPoint:
                self.remove_from_rounds_present(guardian)
        else:
            raise (ValueError("Guardian not present in the cell"))
            print("Guardian not found in the cell")

    def get_guardians_present(self):  # Returns a list of __guardians present in the cell
        return self.__guardian_present

    def get_cell_type(self):
        return self.__cell_type

    def remove_neighbours(self):
        self.__neighbour_cells = []

    def __str__(self) -> str:
        return str(self.__coordinates)

    def __repr__(self):
        return "Cell" + str(self.__coordinates)
