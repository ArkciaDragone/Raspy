# Universal initialization
import tools
import mcpi.minecraft as mmc
import mcpi.vec3 as vec3
import mcpi.block as block
import mcpi.entity as entity
from mcpi.util import flatten
import time

V3 = vec3.Vec3
print("Loading simple maze...")
mc = tools.start(0)

# Game init
from room import Room, Gate
import random

H, L = 7, 7  # const room Height & Length (should be odd)
SIZE = 7  # Maze grid size
DIR = ['n', 's', 'e', 'w']
vertex = V3(3000, 64, 3000)
spawn = vertex + V3(L + L // 2, 0, L + L // 2)  # As bottom
mc.setBlocks(vertex.cubeVertex((SIZE + 2) * L), block.AIR.id)  # Clean up the field
tools.makeCubeVertex(mc, vertex, (SIZE + 2) * L, block.GLASS.id, b=False, t=False)
rooms = []

# Room generation
for r in range(SIZE):
    rooms.insert(r, [])
    for c in range(SIZE):
        rooms[r].append(Room(spawn + V3(r * L, 0, c * L), L, H))
        if r != 0:
            rooms[r][c].link(rooms[r - 1][c], 'w', Gate.SEP)
        if c != 0:
            rooms[r][c].link(rooms[r][c - 1], 'n', Gate.SEP)

# Path search
RMSPAWN, RMEXIT = rooms[0][0], rooms[SIZE - 1][SIZE - 1]
path = [None, RMSPAWN]
go: Room = RMSPAWN
random.seed()
deadends = [None]
pathdir = ''
while go is not RMEXIT:
    dirs = DIR[:]
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
print(pathdir, len(path))

# Room connection
for i in range(1, len(path) - 1):  # First element is "None"
    print(path[i], path[i + 1])
    go, to = path[i], path[i + 1]
    go.gates[to] = to.gates[go] = Gate.AIR
    go.walls['t'] = False

# Obfuscations
GATES = [1, 1, 2, 2, 2, 2, 3, 3, 4]
pass  # TODO

# Block construction
for r in flatten(rooms):
    r.construct(mc)

# Game begins!
time.sleep(3)
for p in mc.getPlayerEntityIds():
    mc.entity.setTilePos(p, RMSPAWN.bottom.up(2))
mc.postToChat("Maze begins! Try to find the exit.")
time.sleep(6)
mc.postToChat("Well")