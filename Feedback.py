class Feedback:
    # list of strings based on the events that happened in this round, and a method to display it
    feedbacks = {
        "invalid_action": {
            "code": "INVALID_ACTION",
            "message": "Invalid action, Your Score is decreased by this."
        },
        "timeout": {
            "code": "TIMEOUT",
            "message": "Time is up, Your Score is decreased by this."
        },
        "error": {
            "code": "ERROR",
            "message": "Something went wrong, Your Score is decreased by this."
        },
        "you_have_been_attacked": {
            "code": "YOU_HAVE_BEEN_ATTACKED",
            "message": "You have been attacked, Your Troops health is decreased by this."
        },
        "guardian_died": {
            "code": "GUARDIAN_DEAD",
            "message": "Guardian is dead, Your Score is decreased by this."
        },
        'attack_success': {
            'code': 'ATTACK_SUCCESS',
            'message': 'Attack Success'
        },
        "teleport_success": {
            "code": "TELEPORT_SUCCESS",
            "message": "Teleport Success"
        },
        "infinity_stone_moved": {
            "code": "INFINITY_STONE_MOVED",
            "message": "Infinity Stone moved"
        },
        "guardian_moved_infinity_stone": {
            "code": "GUARDIAN_MOVED_INFINITY_STONE",
            "message": "Guardian moved Infinity Stone"
        },
        "infinity_stone_dropped": {
            "code": "INFINITY_STONE_DROPPED",
            "message": "Infinity Stone dropped"
        },
        "guardian_died_and_infinity_stone_dropped": {
            "code": "GUARDIAN_DEAD_AND_INFINITY_STONE_DROPPED",
            "message": "Guardian is dead and Infinity Stone dropped"
        },
        "infinity_stone_picked_up": {
            "code": "INFINITY_STONE_PICKED_UP",
            "message": "Infinity Stone picked up"
        },
        "guardian_picked_up_infinity_stone": {
            "code": "GUARDIAN_PICKED_UP_INFINITY_STONE",
            "message": "Guardian picked up Infinity Stone"
        },
        "clue": {
            "code": "CLUE",
            "message": "Clue"
        },
        "star_lord_special_power": {
            "code": "STAR_LORD_SPECIAL_POWER",
            "message": "Star Lord Special Power"
        },
        'healpoint_used': {
            'code': 'HEALPOINT_USED',
            'message': 'Healpoint used'
        },

    }

    def __init__(self, feedback_code, data={}) -> None:
        self.__feedback_code = self.feedbacks[feedback_code]["code"]
        self.__feedback_message = self.feedbacks[feedback_code]["message"]
        if type(data) is dict:
            self.__data = data
        else:
            raise TypeError("Data must be a dictionary")
            self.__data = {}

    def get_feedback_code(self) -> str:
        return self.__feedback_code

    def get_feedback_message(self) -> str:
        return self.__feedback_message

    def get_data(self) -> str:
        return self.__data

    def set_data(self, data) -> None:
        if type(data) is dict:
            self.__data = data
            return True
        else:
            raise TypeError("Data must be a dictionary")
            return False

    def json(self) -> dict:
        return {
            "code": self.__feedback_code,
            "message": self.__feedback_message,
            "data": self.__data
        }

    def __str__(self) -> str:
        return f"Feedback( {self.__feedback_code} )"

    def __repr__(self) -> str:
        return f"Feedback( {self.__feedback_code} )"
