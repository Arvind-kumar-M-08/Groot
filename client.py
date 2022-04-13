import json
import sys

import socketio
import random

if len(sys.argv) != 2:
    print("Usage: python client.py <player_id>")
    exit(1)

sio = socketio.Client()

if sys.argv[1] == "1":
    PLAYER_ID = 'player1'
    PLAYER_PASSWORD = 'player1'
else:
    PLAYER_ID = 'player2'
    PLAYER_PASSWORD = 'player2'
PLAYER_ROOM = 'gameRoom'


@sio.event
def connect():
    print("I'm connected!")


counter = 1

visited = []
stack = []

@sio.event
def action(state):

    cells = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    cell = random.choice(cells)
    guardians = ["Gamora", "Drax", "Rocket", "Groot", "StarLord"]
    guardian = random.choice(guardians)
    coordinates = state['movegen'][guardian]['current_cell']['coordinates']
    coordinates = coordinates.strip('(').strip(')').split(', ')

    new_cell = (int(coordinates[0]) + int(cell[0]), int(coordinates[1]) + cell[1])

    action_type = ['MOVE', 'ATTACK']
    action_selected = random.choice(action_type)

    # print(action_selected, guardian, new_cell)

    action = {
        "action_type": action_selected,
        "troop": guardian,
        "target": str(new_cell),
        'player_id': PLAYER_ID,
        'round_no': state['round_no']
    }
    print("Sending action:", action)
    sio.emit('action', action)


@sio.event
def connected(data):
    print("Response:", data)


sio.connect('http://127.0.0.1:8000',
            {"auth": json.dumps({'player_id': PLAYER_ID, 'password': PLAYER_PASSWORD, 'room': PLAYER_ROOM})})
