import json
import random
import sys
import threading
import time
from datetime import datetime

import eventlet
import socketio

from Action import Action
from Feedback import Feedback

eventlet.monkey_patch()

from Environment import Environment
from Player import Player

rooms = {
    'gameRoom': {
        'id': 'gameRoom',
        'start_time': "Feb 10 2022  7:48PM +0530",
        'player1': {
            'player_id': 'player1',
            "password": "player1",
        },
        'player2': {
            'player_id': 'player2',
            "password": "player2",
        }
    },
}


def create_socket():
    # create a Socket.IO server
    sio = socketio.Server(async_mode='eventlet', ping_interval=0.5, ping_timeout=1)
    # wrap with a WSGI application
    app = socketio.WSGIApp(sio)

    return sio, app


# Press the green button in the gutter to run the script.
def main(IP, PORT):
    sio, app = create_socket()

    ROOM_ID = 'gameRoom'

    if ROOM_ID not in rooms.keys():
        return False

    sio.emit("game_status", "Game Started - Waiting for players")

    # convert time string to timestamp
    start_time = datetime.strptime(rooms[ROOM_ID]['start_time'], '%b %d %Y %I:%M%p %z')
    start_time = start_time.timestamp()
    start_time = time.time() + 10
    env = Environment(ROOM_ID, start_time, 50, 50, 300, 1, 300)
    env.create_graph()

    env.print_graph()

    if not env.place_special_cells(3, 2, 2, 2):
        print("Error in placing special cells")
        return False

    update_rounds = threading.Thread(target=env.update_rounds, args=(sio,))
    update_rounds.start()

    @sio.event
    def action(sid, data):
        if sid == env.get_player1().get_socket_id():
            try:
                current_action = Action.get_obj_from_json(data, env.get_graph())
                print("Player 1 Action: ", current_action.json())
                if current_action:
                    env.add_action_to_player1(current_action)
                else:
                    raise Exception("Invalid action")

            except Exception as e:
                env.add_player1_feedback(Feedback("error", {"data": "Invalid action"}))
                env.reduce_score(env.get_player1().get_player_id(), "invalid_action")
                # print(e)
        elif sid == env.get_player2().get_socket_id():
            try:
                current_action = Action.get_obj_from_json(data, env.get_graph())
                print("Player 2 Action: ", current_action.json())
                if current_action:
                    env.add_action_to_player2(current_action)
                else:
                    raise Exception("Invalid action")
            except Exception as e:
                env.add_player2_feedback(Feedback("error", {"data": "Invalid action"}))
                env.reduce_score(env.get_player2().get_player_id(), "invalid_action")
                # print(e)
        else:
            print('Invalid User')
            sio.disconnect(sid)

    @sio.on('connect')
    def connect(sid, environ):
        global rooms
        print("Trying to connect ", sid)
        try:
            auth_details = None
            if 'HTTP_AUTH' in environ:
                auth_details = json.loads(environ['HTTP_AUTH'])
            else:
                print("No Auth Details")
                sio.disconnect(sid)
                return False

            if auth_details['room'] in rooms.keys():
                if auth_details['player_id'] == rooms[auth_details['room']]['player1']['player_id']:
                    if auth_details['password'] == rooms[auth_details['room']]['player1']['password']:
                        if env.get_player1() is None:
                            y = random.randint(0, len(env.get_graph()) - 1)
                            print("Player 1 at ({x}, {y})".format(x=0, y=y))
                            env.set_player1(Player(auth_details['player_id'], sid, env.get_graph()[y][0]))
                            print("Player 1 connected")
                        else:
                            print("Player 1 Status: ", env.get_player1().is_connected(), " Player ID: ",
                                  env.get_player1().get_player_id(), " Socket ID: ", env.get_player1().get_socket_id())
                            if not env.get_player1().is_connected():
                                env.get_player1().set_socket_id(sid)
                                env.get_player1().set_connected(True)
                                print("Player 1 Reconnected")
                            else:
                                print("Player 1 Already Connected")
                    else:
                        print("Wrong Password for Player 1")
                        sio.disconnect(sid)
                        return False
                elif auth_details['player_id'] == rooms[auth_details['room']]['player2']['player_id']:
                    if auth_details['password'] == rooms[auth_details['room']]['player2']['password']:

                        if env.get_player2() is None:
                            y = random.randint(0, len(env.get_graph()) - 1)
                            print("Player 2 at ({x}, {y})".format(x=len(env.get_graph()) - 1, y=y))
                            env.set_player2(Player(auth_details['player_id'], sid, env.get_graph()[y][-1]))
                            print("Player 2 Connected")
                        else:
                            print("Player 2 Status: ", env.get_player2().is_connected(), " Player ID: ",
                                  env.get_player2().get_player_id(), " Socket ID: ", env.get_player2().get_socket_id())
                            if not env.get_player2().is_connected():
                                env.get_player2().set_socket_id(sid)
                                env.get_player2().set_connected(True)
                                print("Player 2 Reconnected")
                            else:
                                print("Player 2 Already Connected")
                    else:
                        print("Wrong Password for Player 2")
                        sio.disconnect(sid)
                        return False
                else:
                    print("Wrong Username")
                    sio.disconnect(sid)
                    return False
            else:
                print("Wrong Room Id")
                sio.disconnect(sid)
                return False
        except Exception as e:
            print(e)
            sio.disconnect(sid)
            return False

        sio.emit('connected', {'data': 'Connected'})

    @sio.on('disconnect')
    def disconnect(sid):
        if env.get_player1() and env.get_player1().get_socket_id() == sid:
            env.get_player1().set_connected(False)
            env.get_player1().set_socket_id(None)
            print("Player 1 Disconnected")
        elif env.get_player2() and env.get_player2().get_socket_id() == sid:
            env.get_player2().set_connected(False)
            env.get_player2().set_socket_id(None)
            print("Player 2 Disconnected")
        else:
            print("Disconnecting Unknown Player")

    @sio.on('connect_error')
    def connect_error(sid):
        print('connect error ', sid)

    # start the server
    print(IP, PORT)
    # close app
    eventlet.wsgi.server(eventlet.listen((str(IP), int(PORT)), reuse_port=True), app)


if __name__ == '__main__':
    IP = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    PORT = sys.argv[2] if len(sys.argv) > 2 else '8000'
    main(IP, PORT)
