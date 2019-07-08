# Universal initialization
from typing import List

import tools
import mcpi.vec3 as vec3
import mcpi.block as block
from mcpi.util import flatten
import time
from room import Room, Gate
import random

V3 = vec3.Vec3
print("Loading simple maze...")
mc = tools.start(0)
mc.postToChat("The Maze is afoot...")

# Game init
H, L = 7, 7  # const room Height & Length (should be odd)
SIZE = random.randint(5, 10)  # Maze grid size
print("  Maze size:", SIZE)
DIR = ['n', 's', 'e', 'w']
vertex = V3(3000, 64, 3000)
spawn = vertex + V3(L + L // 2, 0, L + L // 2)  # As bottom
mc.setBlocks(vertex.cubeVertex((SIZE + 2) * L), block.AIR.id)  # Clean up the field
# tools.makeCubeVertex(mc, vertex, (SIZE + 2) * L, block.GLASS.id, b=False, t=False)
rooms: List[List[Room]] = []

# Room generation
print("Generating maze...")
for r in range(SIZE):
    rooms.insert(r, [])
    for c in range(SIZE):
        rooms[r].append(Room(spawn + V3(r * L, 0, c * L), L, H))
        if r != 0:
            rooms[r][c].link(rooms[r - 1][c], 'w', Gate.SEP)
        if c != 0:
            rooms[r][c].link(rooms[r][c - 1], 'n', Gate.SEP)

# Path search
print("Searching path...")
RMSPAWN: Room = rooms[random.randint(0, SIZE - 1)][random.randint(0, SIZE - 1)]
RMEXIT: Room = rooms[random.randint(0, SIZE - 1)][random.randint(0, SIZE - 1)]
RMSPAWN.blockid = block.WOOD_PLANKS
RMEXIT.blockid = block.BRICK_BLOCK
RMEXIT.walls['b'] = False
path = [None, RMSPAWN]
go: Room = RMSPAWN
random.seed()
deadends = [None]
pathdir = ''
while go is not RMEXIT:
    dirs = DIR.copy()
    random.shuffle(dirs)
    for dir in dirs:
        to = go.adjacent.get(dir)
        if to not in deadends and to not in path:
            path.append(to)
            go = to
            pathdir += dir
            break
    else:  # Dead end, backtrack
        go = path[-2]
        deadends.append(path[-1])
        pathdir = pathdir[:-1]
        del path[-1]
print("  Standard Path:", pathdir)
print("  Standard Path length:", len(path))

# Room connection
print("Connecting path...")
for i in range(1, len(path) - 1):  # First element is "None"
    go, to = path[i], path[i + 1]
    go.gates[to] = to.gates[go] = Gate.randConn()
    # go.walls['t'] = False

# Obfuscations
print("Obfuscating...")
i = 0
for row in rooms:
    for room in row:
        # room.walls['t'] = False
        for to, _ in room.gates.items():
            if random.random() < 0.2:
                room.gates[to] = to.gates[room] = Gate.randConn()
                i += 1
print("  Opened {} extra door(s)".format(i))

# Block construction
print("Constructing blocks...")
for r in flatten(rooms):
    r.construct(mc)
    time.sleep(0.05)

# Game begins!
print("Maze ready. Teleporting players...")
for p in mc.getPlayerEntityIds():
    mc.entity.setTilePos(p, RMSPAWN.bottom.up(2))
mc.postToChat("Maze begins! Try to find the exit.")
time.sleep(6)
mc.postToChat("Good luck!")
