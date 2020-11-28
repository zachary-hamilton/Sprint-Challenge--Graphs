from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from collections import deque

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
traversal_path = []

def document_room(room):
    global world_graph
    # global unexplored_count
    if room.id not in world_graph:
        world_graph[room.id] = {}
        for each in room.get_exits():
            world_graph[room.id][each] = '?'

def add_to_traversal(temp_path):
    global traversal_path
    for move in temp_path:
        traversal_path.append(move)

def bfs(starting_node):
    global world_graph
    shortest_path = []
    visited = set()
    queue = deque()
    queue.append([starting_node])
    while len(queue) > 0:
        curr_path = queue.popleft()
        curr_node = curr_path[-1]
        if curr_node not in visited:
            visited.add(curr_node)
            for key, value in world_graph[curr_node.id].items():
                if value == '?':
                    for room in curr_path:
                        shortest_path.append(room.id)
                    return shortest_path, True
                next_path = curr_path.copy()
                next_room = curr_node.get_room_in_direction(key)
                next_path.append(next_room)    
                queue.append(next_path)
    return shortest_path, False

def translate_to_movements(path):
    global world_graph
    movements = []
    for i in range(0, len(path) - 1):
        for key, value in world_graph[path[i]].items():
            if value == path[i + 1]:
                movements.append(key)
    return movements




opposite_direction_dict = {'n':'s',
                        'e':'w',
                        'w':'e',
                        's':'n'}

world_graph = {}
searching = True
while searching:
    current_room = player.current_room
    document_room(current_room)
    temp_path = []
    queue = deque()
    queue.append([current_room])
    while len(queue) > 0:
        curr_path = queue.pop()
        curr_node = curr_path[-1]
        # select the next room to move to
        unexplored_list = []
        for key, value in world_graph[curr_node.id].items():
            if value == '?':
                unexplored_list.append(key)
        if len(unexplored_list) > 0:        
            next_direction = unexplored_list[0]
            # get direction of room coming from with next room as reference
            opposite_direction = opposite_direction_dict[next_direction]

            temp_path.append(next_direction)
            next_room = curr_node.get_room_in_direction(next_direction)
            document_room(next_room) # add it to world_graph
            world_graph[curr_node.id][next_direction] = next_room.id
            world_graph[next_room.id][opposite_direction] = curr_node.id
            next_path = curr_path.copy()
            next_path.append(next_room)
            queue.append(next_path)
    
    for move in temp_path:
        player.travel(move)
    add_to_traversal(temp_path)
    # find the next unexplored room
    path, searching = bfs(curr_node)
    movements = translate_to_movements(path)
    for move in movements:
        player.travel(move)
    add_to_traversal(movements)     

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
'''
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
'''
