import random
import time

from Action import Action
from Cells.Beast import Beast
from Cells.Cell import Cell
from Cells.Clue import Clue
from Cells.HealPoint import HealPoint
from Cells.Teleporter import Teleporter
# from Cells.Cell import Cell
from Feedback import Feedback
from InfinityStone import InfinityStone
from Player import Player
from State import State


class Environment:
    def __init__(self, room_id, start_time, height, width, max_penalty_score, player_timeout, max_rounds) -> None:
        self.__env = {'__name__': 'GuardAIns', '__version__': '0.1'}
        self.__room_id = room_id
        self.__start_time = start_time
        self.__graph = None
        self.__rounds = 0
        self.__player1_feedback = []
        self.__player2_feedback = []
        self.__player1 = None
        self.__player2 = None
        self.__width = width
        self.__height = height
        self.__printable_matrix = None
        self.__player1_actions = []
        self.__player2_actions = []
        self.__player1_penalty_score = max_penalty_score
        self.__player2_penalty_score = max_penalty_score
        self.__max_penalty_score = max_penalty_score
        self.__player_timeout = player_timeout
        self.__winner = None
        self.__game_over = False
        self.__max_rounds = max_rounds
        self.__infinity_stone = None

    def get_env(self):
        return self.__env

    def get_start_time(self):
        return self.__start_time

    def get_room_id(self):
        return self.__room_id

    def get_graph(self):
        return self.__graph

    def get_rounds(self):
        return self.__rounds

    def get_player1(self) -> Player:
        return self.__player1

    def get_player2(self) -> Player:
        return self.__player2

    def set_player1(self, player1: Player) -> None:
        self.__player1 = player1

    def set_player2(self, player2: Player) -> None:
        self.__player2 = player2

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_player1_actions(self):
        return self.__player1_actions

    def get_player2_actions(self):
        return self.__player2_actions

    def get_player1_penality_score(self):
        return self.__player1_penalty_score

    def get_player2_penality_score(self):
        return self.__player2_penalty_score

    def get_winner(self):
        return self.__winner

    def add_action_to_player1(self, action: Action) -> None:
        self.__player1_actions.append(action)

    def add_action_to_player2(self, action: Action) -> None:
        self.__player2_actions.append(action)

    def get_player1_feedbacks(self):
        return self.__player1_feedback

    def get_player2_feedbacks(self):
        return self.__player2_feedback

    def add_player1_feedback(self, feedback: Feedback) -> None:
        self.__player1_feedback.append(feedback)

    def add_player2_feedback(self, feedback: Feedback) -> None:
        self.__player2_feedback.append(feedback)

    def create_graph(self) -> None:

        matrix = []
        wall = ['|'] + ['-', '|'] * self.__width
        printable_matrix = [wall, ]

        for i in range(self.__height):
            temp_matrix = []
            for j in range(self.__width):
                temp_matrix.append(Cell((j, i)))
            matrix.append(temp_matrix)
            cell_spaces = ['|'] + [' ', '|'] * self.__width
            printable_matrix.append(cell_spaces.copy())
            printable_matrix.append(wall.copy())

        stack = [matrix[0][0]]
        visited = [[0 for _ in range(self.__width)] for _ in range(self.__height)]
        while len(stack):
            current_cell = stack.pop()
            if visited[current_cell.get_coordinates()[1]][current_cell.get_coordinates()[0]] > 1:
                continue
            visited[current_cell.get_coordinates()[1]][current_cell.get_coordinates()[0]] += 1
            possible_neighbours = [[1, 0], [-1, 0], [0, 1], [0, -1]]
            random.shuffle(possible_neighbours)
            # possible_neighbours = random.choices(possible_neighbours, k=3)

            for neighbour in possible_neighbours:
                if neighbour[1] + current_cell.get_coordinates()[1] < 0 \
                        or neighbour[1] + current_cell.get_coordinates()[1] >= self.__height:
                    continue
                if neighbour[0] + current_cell.get_coordinates()[0] < 0 \
                        or neighbour[0] + current_cell.get_coordinates()[0] >= self.__width:
                    continue

                if visited[neighbour[1] + current_cell.get_coordinates()[1]][
                    neighbour[0] + current_cell.get_coordinates()[0]] > 1:
                    continue
                if matrix[neighbour[1] + current_cell.get_coordinates()[1]][
                    neighbour[0] + current_cell.get_coordinates()[0]] in stack:
                    continue

                current_cell.add_neighbour_cell(matrix[neighbour[1] + current_cell.get_coordinates()[1]][
                                                    neighbour[0] + current_cell.get_coordinates()[0]])
                matrix[neighbour[1] + current_cell.get_coordinates()[1]][
                    neighbour[0] + current_cell.get_coordinates()[0]].add_neighbour_cell(current_cell)
                stack.append(matrix[neighbour[1] + current_cell.get_coordinates()[1]][
                                 neighbour[0] + current_cell.get_coordinates()[0]])
                printable_matrix[
                    2 * (current_cell.get_coordinates()[1]) + 1 + neighbour[1]][
                    2 * (current_cell.get_coordinates()[0]) + 1 + neighbour[0]] = ' '

        self.__graph = matrix
        self.__printable_matrix = printable_matrix

    def print_graph(self):
        if not self.__printable_matrix:
            return False
        for i in range(len(self.__printable_matrix)):
            print("".join(self.__printable_matrix[i]))

        return True

    def is_graph_connected(self):
        all_cells = []

        for i in range(self.__height):
            for j in range(self.__width):
                all_cells.append(self.__graph[i][j])

        queue = [self.__graph[0][0]]
        visited = []

        while len(queue):
            node = queue.pop(0)

            for cell in node.get_neighbour_cells():

                if cell in visited:
                    continue

                if cell in all_cells:
                    all_cells.remove(cell)

                visited.append(cell)
                queue.append(cell)

        if len(all_cells) == 0:
            return True
        else:
            return False

    def place_special_cells(self, no_of_teleporters, no_of_healpoints, no_of_clues, no_of_beasts):

        if no_of_teleporters + no_of_healpoints + no_of_clues + no_of_beasts > self.__width * self.__height:
            print("Not enough cells to place all the special cells")
            raise RuntimeError("Not enough cells to place all the special cells")
            return False

        for i in range(no_of_teleporters):
            x = random.randint(0, self.__width - 1)
            y = random.randint(0, self.__height - 1)

            while self.__graph[y][x].get_cell_type() != 'Normal':
                x = random.randint(0, self.__width - 1)
                y = random.randint(0, self.__height - 1)

            if self.__graph[y][x].get_cell_type() == 'Normal':
                prev_cell = self.__graph[y][x]
                self.__graph[y][x] = Teleporter(self.__graph[y][x])
                # replace the cell with teleporter in the neighbour cells
                for cell in self.__graph[y][x].get_neighbour_cells():
                    cell.remove_neighbour_cell(prev_cell)
                    cell.add_neighbour_cell(self.__graph[y][x])

        for i in range(no_of_healpoints):
            x = random.randint(0, self.__width - 1)
            y = random.randint(0, self.__height - 1)

            while self.__graph[y][x].get_cell_type() != 'Normal':
                x = random.randint(0, self.__width - 1)
                y = random.randint(0, self.__height - 1)

            if self.__graph[y][x].get_cell_type() == 'Normal':
                prev_cell = self.__graph[y][x]
                self.__graph[y][x] = HealPoint(self.__graph[y][x])
                # replace the cell with healpoint in the neighbour cells
                for cell in self.__graph[y][x].get_neighbour_cells():
                    cell.remove_neighbour_cell(prev_cell)
                    cell.add_neighbour_cell(self.__graph[y][x])

        for i in range(no_of_clues):
            x = random.randint(0, self.__width - 1)
            y = random.randint(0, self.__height - 1)

            while self.__graph[y][x].get_cell_type() != 'Normal':
                x = random.randint(0, self.__width - 1)
                y = random.randint(0, self.__height - 1)

            if self.__graph[y][x].get_cell_type() == 'Normal':
                prev_cell = self.__graph[y][x]
                self.__graph[y][x] = Clue(self.__graph[y][x])
                # replace the cell with clue in the neighbour cells
                for cell in self.__graph[y][x].get_neighbour_cells():
                    cell.remove_neighbour_cell(prev_cell)
                    cell.add_neighbour_cell(self.__graph[y][x])

        for i in range(no_of_beasts):
            x = random.randint(0, self.__width - 1)
            y = random.randint(0, self.__height - 1)

            while self.__graph[y][x].get_cell_type() != 'Normal':
                x = random.randint(0, self.__width - 1)
                y = random.randint(0, self.__height - 1)

            if self.__graph[y][x].get_cell_type() == 'Normal':
                prev_cell = self.__graph[y][x]
                self.__graph[y][x] = Beast(self.__graph[y][x])
                # replace the cell with beast in the neighbour cells
                for cell in self.__graph[y][x].get_neighbour_cells():
                    cell.remove_neighbour_cell(prev_cell)
                    cell.add_neighbour_cell(self.__graph[y][x])

        x = random.randint(0, self.__width - 1)
        y = random.randint(0, self.__height - 1)

        while self.__graph[y][x].get_cell_type() != 'Normal':
            x = random.randint(1, self.__width - 2)
            y = random.randint(0, self.__height - 1)

        if self.__graph[y][x].get_cell_type() == 'Normal':
            power_stone = InfinityStone(self.get_graph()[y][x])
            self.__infinity_stone = power_stone

        return True

    def movegen(self, player: Player) -> dict:
        # sent as input for the player object, it contains the neighboring cells,
        # current locations of troops, health of troops and feedback.

        return_dict = {
            # 0 - up, 1 - left, 2 - down, 3 - right
            'Gamora': [[], [], [], []],
            'Drax': [[], [], [], []],
            'Rocket': [[], [], [], []],
            'Groot': [[], [], [], []],
            'StarLord': [[], [], [], []]
        }
        for key in player.get_guardians().keys():
            # for all directions
            current_guardian_obj = player.get_guardians()[key]
            for i in range(4):  # 0 - up, 1 - left, 2 - down, 3 - right
                dir_ver = 0
                dir_hor = 0
                current_coordinates = current_guardian_obj.coordinates.get_coordinates()
                current_cell = current_guardian_obj.coordinates
                if i == 0 or i == 2:
                    dir_ver = i - 1  # dir_ver = -1 or 1

                else:
                    dir_hor = i - 2  # dir_hor = -1 or 1
                for x in range(1, current_guardian_obj.get_vision() + 1):
                    possible_neighbour = (
                        current_coordinates[1] + dir_ver * x, current_coordinates[0] + dir_hor * x)
                    if possible_neighbour[0] < 0 or possible_neighbour[0] >= self.__height or possible_neighbour[
                        1] < 0 or possible_neighbour[1] >= self.__width:
                        break
                    neighbour_cells_tuples = [x.get_coordinates() for x in current_cell.get_neighbour_cells()]

                    if self.__graph[possible_neighbour[0]][
                        possible_neighbour[1]].get_coordinates() in neighbour_cells_tuples:
                        return_dict[key][i].append(
                            self.__graph[possible_neighbour[0]][possible_neighbour[1]])
                        current_cell = self.__graph[possible_neighbour[0]
                        ][possible_neighbour[1]]
                    else:
                        break

            if key == "StarLord":
                return_dict[key] = [return_dict[key], [[], [], [], []]]
                # return all the cells that are in the vision of StarLord even if wall is in between
                for i in range(4):  # 0 - up, 1 - left, 2 - down, 3 - right
                    dir_ver = 0
                    dir_hor = 0
                    current_coordinates = current_guardian_obj.coordinates.get_coordinates()
                    current_cell = current_guardian_obj.coordinates
                    if i == 0 or i == 2:
                        dir_ver = i - 1
                    else:
                        dir_hor = i - 2
                    for x in range(1, current_guardian_obj.get_vision() + 1):
                        possible_neighbour = (
                            current_coordinates[0] + dir_ver * x, current_coordinates[1] + dir_hor * x)
                        if possible_neighbour[0] < 0 or possible_neighbour[0] >= self.__height or possible_neighbour[
                            1] < 0 or possible_neighbour[1] >= self.__width:
                            break
                        return_dict[key][1][i].append(
                            self.__graph[possible_neighbour[0]][possible_neighbour[1]])
        return return_dict

    def update_rounds(self, sio):
        while self.get_start_time() - time.time() > 0:
            print('Game Starts in ' + str(self.get_start_time() - time.time()) + " seconds")
            sio.emit('game_status', 'Game Starts in ' + str(self.get_start_time() - time.time()) + " seconds")
            time.sleep(1)

        print('Starting Update Rounds')
        print(self.get_player1(), self.get_player2())

        if self.get_player1() is None:
            if self.get_player2() is None:
                # both players are dead
                print("Both players are Not Connected")
                self.__winner = None
                self.__game_over = True
                return True
            else:
                # player 2 is alive
                self.__winner = self.get_player2()
                self.__game_over = True
                print("Player 2 is the Winner")
                sio.emit('game_status', 'Player 2 is the Winner')
                return True
        else:
            if self.get_player2() is None:
                # player 1 is alive
                self.__winner = self.get_player1()
                self.__game_over = True
                print("Player 1 is the Winner")
                sio.emit('game_status', 'Player 1 is the Winner')
                return True

        while True:
            print("Round: ", self.__rounds)
            if self.__infinity_stone:
                if self.__infinity_stone.get_coordinates() == self.get_player1().get_base_coordinates():
                    self.__winner = self.get_player1()
                    self.__game_over = True
                    self.__infinity_stone.set_returned_to_base(True)
                    print("Player 1 is the Winner, because of Infinity Stone reached to base",
                          self.__infinity_stone.get_coordinates())
                    sio.emit('game_status', 'Player 1 is the Winner')

                    return True
                if self.__infinity_stone.get_coordinates() == self.get_player2().get_base_coordinates():
                    self.__winner = self.get_player2()
                    self.__game_over = True
                    self.__infinity_stone.set_returned_to_base(True)
                    print("Player 2 is the Winner because of Infinity Stone reached to base",
                          self.__infinity_stone.get_coordinates())
                    sio.emit('game_status', 'Player 2 is the Winner')
                    return True
            if self.__player1_penalty_score < 0 <= self.__player2_penalty_score:  # player 2 wins
                self.__winner = self.__player2
                self.__game_over = True
                print("Player 2 is the Winner because of Penalty Score")
                sio.emit('game_status', 'Player 2 is the Winner')
                return True
            if self.__player2_penalty_score < 0 <= self.__player1_penalty_score:  # player 1 wins
                self.__winner = self.__player1
                self.__game_over = True
                print("Player 1 is the Winner because of Penalty Score")
                sio.emit('game_status', 'Player 1 is the Winner')
                return True
            if self.__player1_penalty_score < 0 and self.__player2_penalty_score < 0:  # draw
                winner = self.evaluate_draw()
                if winner is self.__player1:
                    self.__winner = self.__player1
                    self.__game_over = True
                    print("Player 1 is the Winner because of Draw and evaluate draw said ")
                    sio.emit('game_status', 'Player 1 is the Winner')
                    return True
                elif winner is self.__player2:
                    self.__winner = self.__player2
                    self.__game_over = True
                    print("Player 2 is the Winner")
                    sio.emit('game_status', 'Player 2 is the Winner')
                    return True
                else:
                    self.__winner = None
                    self.__game_over = True
                    print("Draw")
                    sio.emit('game_status', 'Draw')
                    return True

            if self.__max_rounds < self.__rounds:  # If Max Rounds is reached
                winner = self.evaluate_draw()
                if winner == self.get_player1():
                    self.__winner = self.get_player1()
                    print("Player 1 is the Winner")
                    sio.emit('game_status', 'Player 1 is the Winner')
                elif winner == self.get_player2():
                    self.__winner = self.get_player2()
                    print("Player 2 is the Winner")
                    sio.emit('game_status', 'Player 2 is the Winner')
                else:
                    self.__winner = None
                    print("Draw")
                    sio.emit('game_status', 'Game is a Draw')

                print("Game Over")
                sio.emit('game_status', 'Game Over')
                return True

            player1_state = State(self.movegen(self.get_player1()), self.__player1_feedback,
                                  self.__player1_penalty_score, self.get_rounds(), self.get_player1(),
                                  self.__infinity_stone)
            player2_state = State(self.movegen(self.get_player2()), self.__player2_feedback,
                                  self.__player2_penalty_score, self.get_rounds(), self.get_player2(),
                                  self.__infinity_stone)

            player1_error = False
            player2_error = False

            player1_action = None
            player2_action = None

            self.__player1_feedback = []
            if self.get_player1().is_connected():
                try:
                    sio.call("action", to=self.get_player1().get_socket_id(), data=player1_state.json(),
                             timeout=self.__player_timeout)
                    if len(self.__player1_actions):
                        player1_action = self.__player1_actions[-1]
                        if player1_action.get_round_no() != self.get_rounds():
                            raise RuntimeError("Player 1 Action Data Inconsistent")
                    else:
                        raise RuntimeError('Player 1 Action Not found')
                except TimeoutError:
                    self.add_player1_feedback(Feedback("timeout"))
                    player1_error = True
                    self.reduce_score(self.get_player1().get_player_id(), "timeout")
                except Exception as e:
                    print(e)
                    self.add_player1_feedback(Feedback("error", {"error": str(e)}))
                    player1_error = True
                    self.reduce_score(self.get_player1().get_player_id(), "error")
            else:
                player1_error = True

            self.__player2_feedback = []
            if self.get_player2().is_connected():
                try:
                    sio.call("action", to=self.get_player2().get_socket_id(), data=player2_state.json(),
                             timeout=self.__player_timeout)

                    if len(self.__player2_actions):
                        player2_action = self.__player2_actions[-1]
                        if player2_action.get_round_no() != self.get_rounds():
                            raise RuntimeError("Player 2 Action Data Inconsistent")
                    else:
                        raise RuntimeError('Player 2 Action Not found')

                except TimeoutError:
                    self.add_player2_feedback(Feedback("timeout"))
                    player2_error = True
                    self.reduce_score(self.get_player2().get_player_id(), "timeout")
                except Exception as e:
                    print(e)
                    self.add_player2_feedback(Feedback("error", {'error': str(e)}))
                    player2_error = True
                    self.reduce_score(self.get_player2().get_player_id(), "error")
            else:
                player2_error = True

            self.execute_action(player1_action, player2_action, player1_error, player2_error)
            if self.__infinity_stone:
                feedback, feedback_to_player, player_id = self.__infinity_stone.update_coordinates()
                if feedback:
                    self.add_player1_feedback(feedback)
                    self.add_player2_feedback(feedback)
                    if player_id == self.get_player1().get_player_id():
                        self.add_player1_feedback(feedback_to_player)
                    elif player_id == self.get_player2().get_player_id():
                        self.add_player2_feedback(feedback_to_player)
                    else:
                        raise RuntimeError("Invalid Player ID")

            for troop in self.get_player1().get_guardians().values():
                troop.add_score(troop.get_health() / troop.MAX_HEALTH)
                if troop.get_type() == "Groot":
                    troop.special_ability(self.get_rounds())

                if troop.get_coordinates().get_cell_type() == Cell.Teleporter:
                    dest = troop.get_coordinates().generate_destination(self.__infinity_stone, self.get_graph())
                    if dest.get_cell_type() == Cell.Normal:
                        troop.get_coordinates().remove_guardian_from_cell(troop)
                        troop.set_coordinates(dest)
                        troop.get_coordinates().add_guardian_to_cell(troop)
                        self.add_player1_feedback(Feedback("teleport_success", {"coordinates": dest.get_coordinates(),
                                                                                "guardian": troop.get_type()}))
                elif troop.get_coordinates().get_cell_type() == Cell.Clue:
                    clue, two_players_present = troop.get_coordinates().get_clue(self.get_player2(),
                                                                                 self.__infinity_stone,
                                                                                 troop)
                    # two_players_present = False
                    if clue:
                        self.add_player1_feedback(clue)
                        if not two_players_present:
                            new_cell = Cell(troop.get_coordinates().get_coordinates(),
                                            troop.get_coordinates().get_guardians_present(),
                                            troop.get_coordinates().get_neighbour_cells(), Cell.Normal)
                            self.__graph[troop.get_coordinates().get_coordinates()[1]][
                                troop.get_coordinates().get_coordinates()[0]] = new_cell
                            troop.set_coordinates(new_cell)
                            for guardian_in_cell in troop.get_coordinates().get_guardians_present():
                                guardian_in_cell.set_coordinates(troop.get_coordinates())

                elif troop.get_coordinates().get_cell_type() == Cell.Beast:
                    feedback, two_players_present = troop.get_coordinates().update_health(self.get_player1(),
                                                                                          self.get_player2(),
                                                                                          self.__infinity_stone,
                                                                                          self.get_rounds())
                    if feedback:
                        if feedback.get_feedback_code() == "GUARDIAN_DEAD":
                            feedback.set_data({"attacker_type": "Beast",
                                               'victim_type': troop.get_type()})
                        self.add_player1_feedback(feedback)
                        if not two_players_present:
                            new_cell = Cell(troop.get_coordinates().get_coordinates(),
                                            troop.get_coordinates().get_guardians_present(),
                                            troop.get_coordinates().get_neighbour_cells(), Cell.Normal)
                            self.__graph[troop.get_coordinates().get_coordinates()[1]][
                                troop.get_coordinates().get_coordinates()[0]] = new_cell
                            troop.set_coordinates(new_cell)
                            for guardian_in_cell in troop.get_coordinates().get_guardians_present():
                                guardian_in_cell.set_coordinates(troop.get_coordinates())

                elif troop.get_coordinates().get_cell_type() == Cell.HealPoint:
                    feedback = troop.get_coordinates().update_rounds_present(self.get_rounds())
                    if feedback:
                        self.add_player1_feedback(feedback)

            for troop in self.get_player2().get_guardians().values():
                troop.add_score(troop.get_health() / troop.MAX_HEALTH)

                if troop.get_type() == "Groot":
                    troop.special_ability(self.get_rounds())

                if troop.get_coordinates().get_cell_type() == Cell.Teleporter:
                    dest = troop.get_coordinates().generate_destination(self.__infinity_stone, self.get_graph())
                    if dest.get_cell_type() == Cell.Normal:
                        troop.get_coordinates().remove_guardian_from_cell(troop)
                        troop.set_coordinates(dest)
                        troop.get_coordinates().add_guardian_to_cell(troop)
                        self.add_player2_feedback(Feedback("teleport_success", {"coordinates": dest.get_coordinates(),
                                                                                "guardian": troop.get_type()}))
                elif troop.get_coordinates().get_cell_type() == Cell.Clue:
                    clue, _ = troop.get_coordinates().get_clue(self.get_player1(), self.__infinity_stone, troop)
                    if clue:
                        self.add_player2_feedback(clue)
                        new_cell = Cell(troop.get_coordinates().get_coordinates(),
                                        troop.get_coordinates().get_guardians_present(),
                                        troop.get_coordinates().get_neighbour_cells(), Cell.Normal)
                        self.__graph[troop.get_coordinates().get_coordinates()[1]][
                            troop.get_coordinates().get_coordinates()[0]] = new_cell
                        troop.set_coordinates(new_cell)
                        for guardian_in_cell in troop.get_coordinates().get_guardians_present():
                            guardian_in_cell.set_coordinates(troop.get_coordinates())
                    else:
                        raise Exception("Clue not found but cell type is clue")

                elif troop.get_coordinates().get_cell_type() == Cell.Beast:
                    feedback, two_players_present = troop.get_coordinates().update_health(self.get_player2(),
                                                                                          self.get_player1(),
                                                                                          self.__infinity_stone,
                                                                                          self.get_rounds())
                    if feedback:
                        if feedback.get_feedback_code() == "GUARDIAN_DEAD":
                            feedback.set_data({"attacker_type": "Beast",
                                               'victim_type': troop.get_type()})
                        self.add_player2_feedback(feedback)
                        new_cell = Cell(troop.get_coordinates().get_coordinates(),
                                        troop.get_coordinates().get_guardians_present(),
                                        troop.get_coordinates().get_neighbour_cells(), Cell.Normal)
                        self.__graph[troop.get_coordinates().get_coordinates()[1]][
                            troop.get_coordinates().get_coordinates()[0]] = new_cell
                        troop.set_coordinates(new_cell)
                        for guardian_in_cell in troop.get_coordinates().get_guardians_present():
                            guardian_in_cell.set_coordinates(troop.get_coordinates())


                elif troop.get_coordinates().get_cell_type() == Cell.HealPoint:
                    feedback = troop.get_coordinates().update_rounds_present(self.get_rounds())
                    if feedback:
                        self.add_player2_feedback(feedback)

            self.__rounds += 1
            sio.emit('game_status', "Game Running - Round " + str(self.__rounds))
            self.get_reduced_score()
            print("Player 1 Penality Score: ", self.get_player1_penality_score())
            print("Player 2 Penality Score: ", self.get_player2_penality_score())
            print("Player 1 Feedback: ", self.__player1_feedback)
            print("Player 2 Feedback: ", self.__player2_feedback)
            print("player 1 Guardians: ", self.get_player1().get_guardians())
            print("player 2 Guardians: ", self.get_player2().get_guardians())

        return True

    def validate_action(self, action: Action) -> bool:
        # Always check if the acting guardian is alive or not
        if action is None:
            print("Action is None")
            return False

        player = action.get_player_id()
        if player == self.get_player1().get_player_id():
            guardian = self.__player1.get_guardian_by_type(action.get_guardian_type())
        elif player == self.get_player2().get_player_id():
            guardian = self.__player2.get_guardian_by_type(action.get_guardian_type())
        else:
            guardian = None
        if guardian is not None:
            if guardian.is_alive():
                if action.get_action_type() == "SPECIAL":
                    if guardian.get_cooldown() > self.get_rounds():
                        return False
                    # check for cool down first then this
                    if action.get_guardian_type() == "Gamora":
                        tg = action.get_target(self.get_graph()).get_coordinates()
                        cg = guardian.get_coordinates().get_coordinates()
                        if ((tg[0] - cg[0]) ** 2 + (tg[1] - cg[1]) ** 2) <= 25:
                            return True
                        else:
                            print("target out of range SPECIAL jump")
                            return False
                    elif action.get_guardian_type() == "Drax":
                        tg = action.get_target(self.get_graph()).get_coordinates()
                        cg = guardian.get_coordinates().get_coordinates()
                        if ((tg[0] == 1 + cg[0] or tg[0] == cg[0] - 1) and tg[1] == cg[1]) or (
                                (tg[1] == 1 + cg[1] or tg[1] == cg[1] - 1) and tg[0] == cg[0]):
                            return True
                        else:
                            print("target range out of range SPECIAL break walls")
                            return False
                    else:
                        print("Invalid guardian type SPECIAL")
                        return False
                elif action.get_action_type() == "ATTACK":

                    if ((guardian.coordinates.get_coordinates()[0] - guardian.get_vision()) <=
                        action.get_target_coordinates()[0] <=
                        (guardian.coordinates.get_coordinates()[0] + guardian.get_vision())) and (
                            guardian.coordinates.get_coordinates()[1] - guardian.get_vision() <=
                            action.get_target_coordinates()[1] <=
                            guardian.coordinates.get_coordinates()[1] + guardian.get_vision()):
                        return True
                    print("Target out of range")
                    return False
                elif action.get_action_type() == "MOVE":
                    if ((guardian.coordinates.get_coordinates()[0] - guardian.get_speed()) <=
                        action.get_target_coordinates()[
                            0] <=
                        (guardian.coordinates.get_coordinates()[0] + guardian.get_speed())) and (
                            guardian.coordinates.get_coordinates()[1] - guardian.get_speed() <=
                            action.get_target_coordinates()[1] <=
                            guardian.coordinates.get_coordinates()[1] + guardian.get_speed()):
                        return True
                    print("Target out of range MOVE")
                    return False
            else:
                print("Guardian is dead")
                return False
        else:
            print("Guardian not found")
            return False

    def execute_action(self, player1_action: Action, player2_action: Action, player1_error: bool, player2_error: bool):
        if not player1_error:
            if not self.validate_action(player1_action):
                player1_error = True
                self.add_player1_feedback(Feedback("invalid_action"))
                self.reduce_score(self.get_player1().get_player_id(), 'invalid_action')
        if not player2_error:
            if not self.validate_action(player2_action):
                player2_error = True
                self.add_player2_feedback(Feedback("invalid_action"))
                self.reduce_score(self.get_player2().get_player_id(), 'invalid_action')
        if not player1_error:
            if player1_action.get_action_type() == Action.ATTACK and player1_action.get_guardian_type() == "Rocket":
                # PLAYER 1 ROCKET
                guardians_present = player1_action.get_target(self.get_graph()).get_guardians_present()
                our_guardian = self.__player1.get_guardian_by_type(
                    player1_action.get_guardian_type())

                if guardians_present and our_guardian:
                    for guardian in guardians_present:
                        # if multiple enemy __guardians are present then attack all, if none of them are there then
                        # for __guardians present would be empty
                        if guardian.get_belongs_to_player() == self.__player2 and guardian.is_alive():
                            # update get_troop to return guardian object after checking if the guardian is not dead
                            feedback = guardian.set_health(guardian.get_health() - our_guardian.get_attack_damage(),
                                                           self.get_rounds())
                            if feedback:
                                feedback.set_data({"attacker_type": our_guardian.get_type(),
                                                   'victim_type': guardian.get_type()})
                                self.add_player2_feedback(feedback)
                            self.add_player1_feedback(Feedback("attack_success",
                                                               {"victim_type": guardian.get_type(),
                                                                "attacker": our_guardian.get_type()}))
                            self.add_player2_feedback(Feedback("you_have_been_attacked",
                                                               {"attacker": our_guardian.get_type(),
                                                                "victim_type": guardian.get_type()}))

        if not player2_error:
            if player2_action.get_action_type() == Action.ATTACK and player2_action.get_guardian_type() == "Rocket":
                # PLAYER 2 ROCKET
                guardians_present = player2_action.get_target(self.get_graph()).get_guardians_present()
                our_guardian = self.__player2.get_guardian_by_type(
                    player2_action.get_guardian_type())

                if guardians_present and our_guardian:
                    for guardian in guardians_present:

                        # if multiple enemy __guardians are present then attack all, if none of them are there then
                        # for __guardians present would be empty
                        if guardian.get_belongs_to_player() == self.__player1 and guardian.is_alive():
                            # update get_troop to return guardian object after checking if the guardian is not dead
                            feedback = guardian.set_health(guardian.get_health() - our_guardian.get_attack_damage(),
                                                           self.get_rounds())
                            if feedback:
                                feedback.set_data({"attacker_type": our_guardian.get_type(),
                                                   'victim_type': guardian.get_type()})
                                self.add_player1_feedback(feedback)
                            self.add_player2_feedback(Feedback("attack_success",
                                                               {"victim_type": guardian.get_type(),
                                                                "attacker": our_guardian.get_type()}))
                            self.add_player1_feedback(Feedback("you_have_been_attacked",
                                                               {"attacker": our_guardian.get_type(),
                                                                "victim_type": guardian.get_type()}))

        if not player1_error:
            if player1_action.get_action_type() == Action.SPECIAL:
                # PLAYER 1 SPECIAL Gamora or Drax
                if (player1_action.get_guardian_type() == "Gamora"):
                    tg = player1_action.get_target(self.get_graph())
                    cg = self.__player1.get_guardian_by_type(player1_action.get_guardian_type()).get_coordinates()
                    guardian = self.__player1.get_guardian_by_type(
                        player1_action.get_guardian_type())  # update it to return
                    # guardian object directly
                    cg.remove_guardian_from_cell(guardian)
                    guardian.set_coordinates(tg)
                    tg.add_guardian_to_cell(guardian)
                    guardian.set_cooldown(self.get_rounds())
                    # self.add_player1_feedback(Feedback("move_success",
                    #                                     {"guardian_type": player1_action.get_guardian_type(),
                    #                                     "target_type": tg.get_type()}))

                elif (player1_action.get_guardian_type() == "Drax"):
                    tg = player1_action.get_target(self.get_graph())
                    cg = self.__player1.get_guardian_by_type(player1_action.get_guardian_type()).get_coordinates()
                    guardian = self.__player1.get_guardian_by_type(
                        player1_action.get_guardian_type())
                    tg.add_neighbour_cell(cg)
                    cg.add_neighbour_cell(tg)

                    guardian.set_cooldown(self.get_rounds())

        if not player2_error:
            if player2_action.get_action_type() == Action.SPECIAL:
                # PLAYER 2 SPECIAL Gamora or Drax
                if (player2_action.get_guardian_type() == "Gamora"):
                    tg = player2_action.get_target(self.get_graph())
                    cg = self.__player2.get_guardian_by_type(player2_action.get_guardian_type()).get_coordinates()
                    guardian = self.__player2.get_guardian_by_type(
                        player2_action.get_guardian_type())  # update it to return
                    # guardian object directly
                    cg.remove_guardian_from_cell(guardian)
                    guardian.set_coordinates(tg)
                    tg.add_guardian_to_cell(guardian)
                    guardian.set_cooldown(self.get_rounds())

                    # self.add_player1_feedback(Feedback("move_success",
                    #                                     {"guardian_type": player1_action.get_guardian_type(),
                    #                                     "target_type": tg.get_type()}))

                elif (player2_action.get_guardian_type() == "Drax"):
                    tg = player2_action.get_target(self.get_graph())
                    cg = self.__player2.get_guardian_by_type(player2_action.get_guardian_type()).get_coordinates()
                    guardian = self.__player2.get_guardian_by_type(
                        player1_action.get_guardian_type())
                    tg.add_neighbour_cell(cg)
                    cg.add_neighbour_cell(tg)
                    guardian.set_cooldown(self.get_rounds())

        if not player1_error:
            if player1_action.get_action_type() == Action.MOVE:
                guardian = self.__player1.get_guardian_by_type(
                    player1_action.get_guardian_type())  # update it to return
                # guardian object directly
                if player1_action.get_target(self.__graph) != guardian.get_coordinates():
                    guardian.get_coordinates().remove_guardian_from_cell(guardian)
                    guardian.set_coordinates(player1_action.get_target(self.__graph))
                    guardian.get_coordinates().add_guardian_to_cell(guardian)

        if not player2_error:
            if player2_action.get_action_type() == Action.MOVE:
                guardian = self.__player2.get_guardian_by_type(
                    player2_action.get_guardian_type())  # update it to return
                # guardian object directly
                if player2_action.get_target(self.__graph) != guardian.get_coordinates():
                    guardian.get_coordinates().remove_guardian_from_cell(guardian)
                    guardian.set_coordinates(player2_action.get_target(self.__graph))
                    guardian.get_coordinates().add_guardian_to_cell(guardian)

        if not player1_error:
            if player1_action.get_action_type() == Action.ATTACK and not player1_action.get_guardian_type() == "Rocket":
                guardians_present = player1_action.get_target(self.get_graph()).get_guardians_present()
                our_guardian = self.__player1.get_guardian_by_type(
                    player1_action.get_guardian_type())

                if guardians_present and our_guardian:
                    for guardian in guardians_present:
                        # if multiple enemy __guardians are present then attack all, if none of them are there then
                        # for __guardians present would be empty
                        if guardian.get_belongs_to_player() == self.__player2 and guardian.is_alive():
                            # update get_troop to return guardian object after checking if the guardian is not dead
                            feedback = guardian.set_health(guardian.get_health() - our_guardian.get_attack_damage(),
                                                           self.get_rounds())
                            if feedback:
                                feedback.set_data({"attacker_type": our_guardian.get_type(),
                                                   'victim_type': guardian.get_type()})
                                guardian.get_coordinates().remove_guardian_from_cell(guardian)

                                self.add_player2_feedback(feedback)
                            self.add_player1_feedback(Feedback("attack_success",
                                                               {"victim_type": guardian.get_type(),
                                                                "attacker": our_guardian.get_type()}))
                            self.add_player2_feedback(Feedback("you_have_been_attacked",
                                                               {"attacker": our_guardian.get_type(),
                                                                "victim_type": guardian.get_type()}))

        if not player2_error:
            if player2_action.get_action_type() == Action.ATTACK and not player2_action.get_guardian_type() == "Rocket":

                guardians_present = player2_action.get_target(self.get_graph()).get_guardians_present()
                our_guardian = self.__player2.get_guardian_by_type(
                    player2_action.get_guardian_type())
                if guardians_present and our_guardian:
                    for guardian in guardians_present:

                        if guardian.get_belongs_to_player() == self.__player1 and guardian.is_alive():
                            # update get_troop to return guardian object after checking if the guardian is not dead
                            feedback = guardian.set_health(guardian.get_health() - our_guardian.get_attack_damage(),
                                                           self.get_rounds())
                            if feedback:
                                feedback.set_data({"attacker_type": our_guardian.get_type(),
                                                   'victim_type': guardian.get_type()})

                                guardian.get_coordinates().remove_guardian_from_cell(guardian)

                                self.add_player1_feedback(feedback)

                            self.add_player2_feedback(Feedback("attack_success",
                                                               {"victim_type": guardian.get_type(),
                                                                "attacker": our_guardian.get_type()}))
                            self.add_player1_feedback(Feedback("you_have_been_attacked",
                                                               {"attacker": our_guardian.get_type(),
                                                                "victim_type": guardian.get_type()}))

        return True

    def reduce_score(self, player: str, feedback_code: str):

        FEEDBACKS_CODES = {
            "timeout": -1,
            "error": -2,
            "invalid_action": -2,
        }

        if feedback_code in FEEDBACKS_CODES.keys():
            if player == self.get_player1().get_player_id():
                self.__player1_penalty_score += FEEDBACKS_CODES[feedback_code]
            elif player == self.get_player2().get_player_id():
                self.__player2_penalty_score += FEEDBACKS_CODES[feedback_code]
            else:
                raise Exception("Invalid player id")
        else:
            raise ValueError("Invalid feedback code")

    def evaluate_draw(self):
        reduced_score_player1, reduced_score_player2 = self.get_reduced_score()
        if reduced_score_player1 > reduced_score_player2:
            return self.__player1
        elif reduced_score_player1 < reduced_score_player2:
            return self.__player2
        else:
            return None

    def get_reduced_score(self):
        reduced_score_player1 = (self.__player1_penalty_score / self.__max_penalty_score) * 0.5
        reduced_score_player2 = (self.__player2_penalty_score / self.__max_penalty_score) * 0.5

        player1_alive_score = 0
        for guardian in self.__player1.get_guardians().values():
            player1_alive_score += guardian.get_score()
        reduced_score_player1 += (player1_alive_score / (self.__rounds * 5)) * 0.5

        player2_alive_score = 0
        for guardian in self.__player2.get_guardians().values():
            player2_alive_score += guardian.get_score()

        reduced_score_player2 += (player2_alive_score / (self.__rounds * 5)) * 0.5

        print("Reduced score player 1: ", reduced_score_player1)
        print("Reduced score player 2: ", reduced_score_player2)

        return reduced_score_player1, reduced_score_player2
