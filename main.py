import json
import sys

import socketio

if len(sys.argv) != 6:
    print("Usage: python3 temp_client.py <url> <port_no> <room_id> <player_id> <player_password>")
    exit(1)

sio = socketio.Client()

URL = sys.argv[1]
PORT_NO = sys.argv[2]
PLAYER_ROOM = sys.argv[3]
PLAYER_ID = sys.argv[4]
PLAYER_PASSWORD = sys.argv[5]

@sio.event
def connect():
    print("I'm connected!")


@sio.event
def game_status(status):
    #Code here to get the game status
    pass

@sio.event
def action(state):
    #Add the code to 
    #read the feedback object provided 

    #send the action object in the specified json format
    # It should be in the following format 
    # action = {
    #         "action_type": '',
    #         "troop": "",
    #         'target': '',
    #         'player_id': ,
    #         'round_no': 
    #     }
    pass


@sio.event
def connected(data):
    print("Response:", data)


sio.connect(URL+':'+PORT_NO,
            {"auth": json.dumps({'player_id': PLAYER_ID, 'password': PLAYER_PASSWORD, 'room': PLAYER_ROOM})})