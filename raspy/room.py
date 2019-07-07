import mcpi.vec3 as vec3
import mcpi.minecraft as mmc
import mcpi.block as block
from enum import Enum
import tools

V3 = vec3.Vec3


class Gate(Enum):
    SEP = 0  # Separated
    AIR = 1  # Connected
    WOOD = 2  # Wooden door


REVERSED = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', 'b': 't', 't': 'b'}


class Room:

    def __init__(self, bottom: V3, length: int, height: int,
                 blockid=block.STONE_BRICK.id, **adjacent_rooms: dict):
        """Adjacent rooms: {s, n, e, w, b, t}"""
        self.blockid = blockid
        self.height = height
        self.length = length
        self.bottom = bottom
        self.adjacent = adjacent_rooms  # Direction: Room
        self.gates = {}  # Room: Gate
        self.walls = {'s': True, 'n': True, 'e': True, 'w': True, 'b': True, 't': True}

    def is_viable(self, rhs) -> bool:
        """Are the two rooms connected or not?"""
        return rhs in self.adjacent.values() and self.gates.get(rhs) != Gate.SEP

    def link(self, rhs, direction: str, connection: Gate):
        """Link two rooms"""
        self.adjacent[direction] = rhs
        rhs.adjacent[REVERSED[direction]] = self
        self.gates[rhs] = rhs.gates[self] = connection
        return self

    def __door(self, dir: str, type: Gate):
        if dir == 'b':
            pos = self.bottom
        else:
            pos = self.bottom.__dict__[dir](self.height if dir == 't' else self.length // 2)

    def construct(self, mc: mmc.Minecraft):
        tools.makeCubeAbove(mc, self.bottom, self.length, self.blockid, **self.walls)
        for dir, room in self.adjacent.items():
            if self.gates[room] == Gate.AIR: