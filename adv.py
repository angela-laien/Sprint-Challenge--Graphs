from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# create a compass for opposite directions
c = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

def explore_maze(visited=[]):
    # store directions
    path = []
    # get available directions in current room using get_exist() from room.py
    for direction in player.current_room.get_exits():
        # player move in available direction to a new room
        player.travel(direction)
        # check if current room has been visited before
        if player.current_room.id not in visited:
            # add current room to the visited list
            visited.append(player.current_room.id)
            # add direction to path
            path.append(direction)
            # update path with new directions and new visited room
            path = path + explore_maze(visited)
            # player can go backard to find new room
            player.travel(c[direction])
            # store player's backward directions
            path.append(c[direction])
        else:
            # player move in opposite direction to look for new room
            player.travel(c[direction])

    return path

traversal_path = explore_maze()
    

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
