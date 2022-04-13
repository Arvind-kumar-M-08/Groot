class Action:
    # UPDATE ACTION TO SEND the acting players, drax, gamora.. objects directly with get_guardian(),
    # and update get_coordinate to send cell object directly
    MOVE = "MOVE"
    ATTACK = "ATTACK"
    SPECIAL = "SPECIAL"
    # INTERACT = "INTERACT"
    TROOPS = ('Groot', 'Rocket', 'Gamora', 'StarLord', 'Drax')

    @classmethod
    def get_obj_from_json(cls, json_data: dict, graph):
        try:
            action_type = json_data["action_type"]
            troop = json_data["troop"]
            # tuple str to tuple

            target = tuple(map(int, json_data["target"].strip('(').strip(')').split(',')))
            if not (0 <= target[0] < len(graph) and 0 <= target[1] < len(graph[0])):
                raise Exception("Invalid target coordinates")

            player_id = json_data["player_id"]
            round_no = json_data['round_no']
            return cls(action_type, troop, target, round_no, player_id)
        except KeyError:
            print("KeyError: Invalid json data")
            return False
        except Exception:
            print("Exception: Invalid json data")
            return False

    def __init__(self, action_type, troop, target_coordinates: tuple, round_no, player_id) -> None:
        if action_type in (Action.MOVE, Action.ATTACK, Action.SPECIAL):
            self.__action_type = action_type

        if troop in Action.TROOPS:
            self.__troop = troop
        else:
            print("Invalid troop:", troop)

        self.__target = target_coordinates
        self.__is_valid = False
        self.__round_no = round_no
        self.__player_id = player_id

    def get_action_type(self) -> str:
        return self.__action_type

    def get_guardian_type(self):
        return self.__troop

    def get_target(self, graph) -> tuple:
        if 0 <= self.__target[1] < len(graph) and 0 <= self.__target[0] < len(graph[0]):
            return graph[self.__target[1]][self.__target[0]]

    def get_target_coordinates(self) -> tuple:
        return self.__target

    def set_action_type(self, action_type: str) -> None:
        self.__action_type = action_type

    def get_player_id(self):
        return self.__player_id

    def get_round_no(self):
        return self.__round_no

    def json(self) -> dict:
        return {
            "action_type": self.__action_type,
            "troop": self.__troop,
            "target": list(self.__target),
            "player_id": self.__player_id,
            # "player_password": self.__player_password,
            "round_no": self.__round_no
        }
