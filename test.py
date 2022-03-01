import json
f = open('state.json')
data = json.load(f)
# print(data["movegen"]["Gamora"]["cooldown"])
# for i in data["movegen"]:
#     # print(i)
# curr = data["movegen"]["Gamora"]["current_cell"]
# print(curr["coordinates"][1],curr["coordinates"][4])

for i in data["movegen"]["Gamora"]["neighbour_cells"]:
    if(i != []):
        # print(i[0])
        for j in i[0]["guardians_present"]:
            print(j["belongs_to"])
    # if(i != []):
    #     print(i[0]["coordinates"])

# def dist(d1,d2):
#     d1 = tuple(d1)
#     d2 = tuple(d2)
#     return (abs(int(d1[0])-int(d2[0]) )+ abs(int(d1[1])-int(d2[1])))

# print(curr["coordinates"][1],curr["coordinates"][4])