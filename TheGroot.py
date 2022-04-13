from itertools import count
import json
from os import stat
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
Found_powerstone = False

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

Visited = {"Drax" : [],
    "Groot" : [],
    "StarLord" : [],
    "Rocket" : [],
    "Gamora" : []}

Visited_by_anyone = []
start_node = ""
we_got_with_tele = False
moved_with_tele = False

parent =dict()
new_parent = dict()
front_parent = dict()
alive = ["Rocket","Gamora","StarLord","Drax","Groot"]

def dist(d1,d2):
    l1 = list(map(int, (d1[1:-1].split(", "))))
    l2 = list(map(int, (d2[1:-1].split(", "))))
    return abs(l1[0]-l2[0])+abs(l1[1]-l2[1])



def dfs(data, guardian):
    global start_node, parent, we_got_with_tele, moved_with_tele
    target = ""
    heu = 0
    move = "MOVE"
    max_heu = 1
    current = data["movegen"][guardian]["current_cell"]
    cur_health = data["movegen"][guardian]["health"]


    target = parent[current["coordinates"]]
    opponents = []
    if cur_health>50:
        for i in data["movegen"][guardian]["neighbour_cells"]:
            for j in range(len(i)): 
                coor_distance =  dist(i[j]["coordinates"],current["coordinates"])
                
                for k in i[j]["guardians_present"]:
                    
                    if( k["belongs_to"] != "you"):
                        if(vision[k["guardian_name"]] < coor_distance):
                            heu += 100
                        if(cur_health*attack[guardian] - health[k["guardian_name"]]*attack[k["guardian_name"]]>0):
                            heu += 50

                    if(heu > max_heu):
                        move = "ATTACK"
                        max_heu = heu
                        target = i[j]["coordinates"][:]
                    heu = 0
                

                    
        if(max_heu > 2):
            # print("\n\n\n\n\n\n\n\n\n\n")
            if(guardian == "Rocket" or guardian[1] == "o"):
                return ["ATTACK",max_heu,target]    

            return [move,max_heu,target]


    heu = 0
    max_heu = 0
    target = parent[current["coordinates"]]
    for i in data["movegen"][guardian]["neighbour_cells"]:
        for j in range(len(i)): 
            print(i[j]["cell_type"])              
            if((i[j]["coordinates"] not in parent) and (dist(i[j]["coordinates"],current["coordinates"]) <= speed[guardian])):
                print(i[j]["coordinates"],i[j]["coordinates"] not in parent)
                if(i[j]["cell_type"] == "Teleporter" and i[j]["is_powerStone_present"] != "True" and data["round_no"]!=0):
                    parent[i[j]["coordinates"]] = current["coordinates"]
                    print("disojojdsojfoj\n\n\n\n")
                    continue
                if(i[j]["cell_type"] == "Beast" and i[j]["is_powerStone_present"] != "True" and data["round_no"]!=0):
                    parent[i[j]["coordinates"]] = current["coordinates"]
                    continue

                if(i[j]["cell_type"] == "Teleporter" and i[j]["is_powerStone_present"] == "True"):
                    heu = 100
                    we_got_with_tele = True

                if(i[j]["cell_type"] != "Teleporter" and i[j]["is_powerStone_present"] == "True"):
                    heu = 200

                if(i[j]["is_powerStone_present"] != "True"):
                    heu = 50
                
                if(heu>max_heu):
                    move = "MOVE"
                    max_heu = heu
                    target = i[j]["coordinates"][:]
                heu = 0
    # print(parent)
    if(target not in parent):
        parent[target] = current["coordinates"]
        
                    
    return [move,max_heu,target]

    

def dfs_back(data, guardian):
    global start_node, parent, we_got_with_tele
    target = ""
    heu = 0
    move = "MOVE"
    current = data["movegen"][guardian]["current_cell"]
    target = parent[current["coordinates"]]           
    return [move,heu,target]

def dfs_tele(data, guardian):
    global start_node, we_got_with_tele, new_parent, Found_powerstone
    target = ""
    heu = 0
    move = "MOVE"
    max_heu = 1
    current = data["movegen"][guardian]["current_cell"]
    cur_health = data["movegen"][guardian]["health"]

    target = parent[current["coordinates"]]
    opponents = []
    for i in data["movegen"][guardian]["neighbour_cells"]:
        for j in range(len(i)): 
            coor_distance =  dist(i[j]["coordinates"],current["coordinates"])
            for k in i[j]["guardians_present"]:
                # print(k)
                if( k["belongs_to"] != "you"):
                    if(vision[k["guardian_name"]] < coor_distance):
                        heu += 100
                    if(cur_health*attack[guardian] - health[k["guardian_name"]]*attack[k["guardian_name"]]>0):
                        heu += 50

                if(heu > max_heu):
                    move = "ATTACK"
                    max_heu = heu
                    target = i[j]["coordinates"][:]
                heu = 0
                

                    
    if(max_heu > 2 and guardian != "Rocket"):
        # print("\n\n\n\n\n\n\n\n\n\n")
        return [move,max_heu,target]

    heu = 0
    move = "MOVE"
    cell_type = ""
    max_heu = 1

    for i in data["movegen"][guardian]["neighbour_cells"]:
        for j in range(len(i)):            
            if((i[j]["coordinates"] not in new_parent) and (dist(i[j]["coordinates"],current["coordinates"]) <= speed[guardian])): 
                if(i[j]["is_powerStone_present"] == "True"): 
                    heu = 200
                    Found_powerstone = True
                elif(i[j]["cell_type"] == "Teleporter"):
                    heu = 100 
                else:
                    heu = 50
                
                if(heu > max_heu):
                    max_heu = heu
                    cell_type = i[j]["cell_type"][:]
                    target = i[j]["coordinates"][:]


                heu = 0
    
                    
    if(target not in new_parent):
        new_parent[target] = current["coordinates"]
    if(cell_type == "Teleporter"):
        moved_with_tele = True

    return [move,heu,target]

def dfs_tele_back(data, guardian):
    global start_node, we_got_with_tele, front_parent, Found_powerstone
    target = ""
    move = "MOVE"
    max_heu = 1
    current = data["movegen"][guardian]["current_cell"]
    cur_health = data["movegen"][guardian]["health"]

    heu = 100001
    move = "MOVE"
    cell_type = ""
    min_heu = 100000

    for i in data["movegen"][guardian]["neighbour_cells"]:
        for j in range(len(i)):
            if(i[j]["coordinates"] in parent and (dist(i[j]["coordinates"],current["coordinates"]) <= speed[guardian])):
                heu = 1000
                we_got_with_tele = False
                target = i[j]["coordinates"][:]
                return [move,heu,target]
                
 


            if((i[j]["coordinates"] not in front_parent) and (dist(i[j]["coordinates"],current["coordinates"]) <= speed[guardian])): 
                
                heu = dist(i[j]["coordinates"],start_node)


                
                if(heu < min_heu):
                    min_heu = heu
                    cell_type = i[j]["cell_type"][:]
                    target = i[j]["coordinates"][:]

    


            heu = 100001
    
    
    if(target not in front_parent):
    
        front_parent[target] = current["coordinates"]
    if(cell_type == "Teleporter"):
        moved_with_tele = True

    return [move,heu,target]


@sio.event
def game_status(status):
    pass




@sio.event
def action(state):
    global alive, parent,start_node, Found_powerstone, new_parent, moved_with_tele

    if(moved_with_tele):
        front_parent.clear()
        new_parent.clear()
        new_parent[state["movegen"][alive[0]]["current_cell"]["coordinates"]] = []
        front_parent[state["movegen"][alive[0]]["current_cell"]["coordinates"]] = []
        moved_with_tele = False

    if state['round_no'] == 0:
        start_node = (state["movegen"]["Gamora"]["current_cell"]["coordinates"])
    
    parent[start_node] = []
    guardian = ""
    target = ""

    for i in state["feedback"]:
        if(i["code"] == "GUARDIAN_DEAD"):
            # print(i)
            attacker = i["data"]["attacker_type"]
            victim = i["data"]["victim_type"]
            if(alive[0] == victim):
                parent = dict()
            alive.remove(victim)
        if(i["code"] == "GUARDIAN_PICKED_UP_INFINITY_STONE"):
            Found_powerstone = True
        if(i["code"] == "GUARDIAN_DEAD_AND_INFINITY_STONE_DROPPED"):
            Found_powerstone = False
    base_attack_heu = 0
    max_base_attack = 1
    for guard in alive[1:]:
        for i in state["movegen"][guard]["neighbour_cells"]:
            for j in range(len(i)):
                for k in i[j]["guardians_present"]:
                    if( k["belongs_to"] != "you"):
                        base_attack_heu = attack[guard]

                    if(base_attack_heu > max_base_attack):
                        move = "ATTACK"
                        guardian = guard[:]
                        max_base_attack = base_attack_heu
                        target = i[j]["coordinates"][:]
                    base_attack_heu = 0
    
    if(max_base_attack > 2):
        best_move = "ATTACK"

    else:

        if(we_got_with_tele == False):

            if(Found_powerstone == False):
                # print("dfs")
                move = dfs(state,alive[0])
                best_move = move[0]
                guardian = alive[0]
                max_heur = move[1]
                target = move[2]

            if(target == []):
                we_got_with_tele == True
            

            if(Found_powerstone == True):
                move = dfs_back(state,alive[0])
                best_move = move[0]
                guardian = alive[0]
                max_heur = move[1]
                target = move[2]
        

        if(we_got_with_tele == True):
            if(Found_powerstone == False):
                move = dfs_tele(state,alive[0])
                best_move = move[0]
                guardian = alive[0]
                max_heur = move[1]
                target = move[2]

            else:
                move = dfs_tele_back(state,alive[0])
                best_move = move[0]
                guardian = alive[0]
                max_heur = move[1]
                target = move[2]
                

    

    
    
    
        
        
    if best_move=="MOVE" and Found_powerstone== False:
        Visited[guardian].append(target)
        Visited_by_anyone.append(target)
    #send the action object in the specified json format
    # It should be in the following format 
    action = {
            "action_type": best_move,
            "troop": guardian,
            'target': target,
            'player_id': PLAYER_ID,
            'round_no': state['round_no']
        }
    print(action)
    print(Found_powerstone)
    sio.emit('action', action)
    pass


@sio.event
def connected(data):
    print("Response:", data)
    


sio.connect(URL+':'+PORT_NO,
            {"auth": json.dumps({'player_id': PLAYER_ID, 'password': PLAYER_PASSWORD, 'room': PLAYER_ROOM})})