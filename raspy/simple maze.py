# Universal initialization
import tools
import mcpi.minecraft as mmc
import mcpi.vec3 as vec3
import mcpi.block as block
import mcpi.entity as entity
import mcpi.vec3 as vec3

V3 = vec3.Vec3
print("Loading simple maze...")
while True:
    try:
        natappPort = int(input("Please specify the natapp port if given; \
                               otherwise input 0 to connect to local host: "))
    except ValueError:
        print("That wasn't a valid integer.")
    else:
        break
if natappPort:
    mc = mmc.Minecraft.create("server.natappfree.cc", natappPort)
else:
    mc = mmc.Minecraft.create()
print('Minecraft connection "mc" established!')

# Game init
from room import Room, Gate
import random

H, L = 7, 7  # const room Height & Length
SIZE = 9  # Maze grid size (should be odd)
DIR = ['n', 's', 'e', 'w']
vertex = V3(0, 64, 0)
spawn = vertex + V3(L + L // 2, 0, L + L // 2)  # As bottom
mc.setBlocks(vertex.cubeVertex((SIZE + 2) * L), block.AIR.id)  # Clean up the field
tools.makeCubeVertex(mc, vertex, (SIZE + 2) * L, block.STONE.id, b=False)
rooms = []
# Room generation
for r in range(SIZE):
    rooms.insert(r, [])
    for c in range(SIZE):
        rooms[r].append(Room(spawn + V3(r * L, 0, c * L), L, H))
        if r != 0:
            rooms[r][c].link(rooms[r - 1][c], 'n', Gate.SEP)
        if c != 0:
            rooms[r][c].link(rooms[r][c - 1], 'w', Gate.SEP)
# Path creation
RMSPAWN, RMEXIT = rooms[0][0], rooms[SIZE - 1][SIZE - 1]
path = [None, RMSPAWN]
go: Room = RMSPAWN
random.seed()
while go is not RMEXIT:
    while True:
        to = go.adjacent.get(random.choice(DIR))
        if to not in path:
            path.append(to)
            go.gates[to] = to.gates[go] = Gate.AIR
            go = to
            break
# Obfuscations
GATES = [1, 1, 2, 2, 2, 2, 3, 3, 4]
pass  # TODO
# Minecraft block construction
from mcpi.util import flatten

for r in flatten(rooms):

