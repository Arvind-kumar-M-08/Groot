import json
import sys
from numpy import False_

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

health = {
    "Drax" : 150,
    "Groot" : 200,
    "StarLord" : 100,
    "Rocket" : 75,
    "Gamora" : 125
}
attack = {
    "Drax" : 70,
    "Groot" : 25,
    "StarLord" : 35,
    "Rocket" : 35,
    "Gamora" : 50
}
vision = {
    "Drax" : 1,
    "Groot" : 2,
    "StarLord" : 5,
    "Rocket" : 4,
    "Gamora" : 2
}
speed = {
    "Drax" : 1,
    "Groot" : 1,
    "StarLord" : 2,
    "Rocket" : 3,
    "Gamora" : 2
}
coolDown = {
    "Drax" : 3,
    "Groot" : 0,
    "StarLord" : 0,
    "Rocket" : 0,
    "Gamora" : 3
}
heal = {
    "Drax" : 0,
    "Groot" : 0,
    "StarLord" : 0,
    "Rocket" : 0,
    "Gamora" : 0
}

action = {
        "action_type": '',
        "troop": "",
        'target': '',
        'player_id': PLAYER_ID,
        'round_no': 0
}

gotHit = {
    "Drax" : [150,0],
    "Groot" : [200,0],
    "StarLord" : [100,0],
    "Rocket" : [75,0],
    "Gamora" : [125,0]
}

Visited = []


def dist(d1,d2):
    l1 = list(map(int, (d1[1:-1].split(", "))))
    l2 = list(map(int, (d2[1:-1].split(", "))))
    return abs(l1[0]-l2[0])+abs(l1[1]-l2[1])


def heuristic(guardian, data):
    max_hue = float('-inf')
    target = ""
    heu = 0
    opponent = False
    move = "MOVE"
    cur_health = data["movegen"][guardian]["health"]
    cooldown = data["movegen"][guardian]["cooldown"]
    current = data["movegen"][guardian]["current_cell"]

    #MOVING
    # if(Found_powerstone!= True):
    for i in data["movegen"][guardian]["neighbour_cells"]:
        if(i != [] and dist(i[0]["coordinates"],current["coordinates"]) <= speed[guardian]):
            if(i[0]["is_powerStone_present"] == True):
                heur += 100
            if(i[0]["cell_type"] == "Teleporter"):
                heu += 100
            for j in i[0]["guardians_present"]:
                if( j["belongs_to"] != "you"):
                    opponent = True
                    heu -= 100
                    break
            if(i[0]["coordinates"] in Visited):
                heu -= 25
            
            heu = heu*(dist(i[0]["coordinates"],current["coordinates"]))

            if(heu > max_hue ):
                max_hue = heu
                target = i[0]["coordinates"]
                
        heu = 0
    
    
    heu = 0

    #ATTACKING

    if(opponent):
        for i in data["movegen"][guardian]["neighbour_cells"]:
            heu = 0
            if(i != []):
                coor_distance =  dist(i[0]["coordinates"],current["coordinates"])
                for j in i[0]["guardians_present"]:
                    if( j["belongs_to"] != "you"):
                        if(vision[j["guardian_name"]] < coor_distance):
                            heu += 100
                        if(cur_health > attack[j["guardian_name"]]):
                            heu += 50
                        
                        heu += cur_health*attack[guardian] - gotHit[j["guardian_name"]][0]*attack[j["guardian_name"]]
                    
                    

        






    # dist = abs(move["cur"][0] -move["target"][0]) + abs(move["cur"][1] -move["target"][1])
    
    # if(move["action"] == 1):
    #     if(move["infinity"] == True and move["opponent"] == ""):
    #         heur += 200
    #     elif(move["infinity"] == True and move["opponent"] != ""):
    #         heur -= 200
    #     elif(move["opponent"] != ""):
    #         heur -= 300
    #     else:
    #         pass
    
    # if(move["action"] == 2):
    #     if(move["opponent"] == ""):
    #         heuristic -= 500
    #     elif(move["infinity"] == True):
    #         heur += 500
    #     else:
    #         if(move["health"] < attack[move["opponent"]]):
    #             heu -= 500
    #         elif(move["health"])


    return [move,heu]

@sio.event
def game_status(status):
    
    data = json.load(status)
    
    # print(data)
    max_heur = float('-inf')
    best_move = ""
    guardian = ""
    for i in data["movegen"]:
        move = heuristic(i)
        if(move[1] > max_heur):
            best_move = move[0]
            guardian = i[:]
            max_heur = move[1]
    




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