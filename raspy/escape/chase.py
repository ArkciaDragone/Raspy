"""
The Chase - Escape Control Program

Works with interface Level. Connects to Minecraft server and perform
game initilization. Maintains level and player status.
"""
import sys

sys.path.append("..")
from typing import Dict, Type
from random import choice, randint
from multiprocessing import Process, Pipe
from escape.angryanvil import AngryAnvil
from escape.funnyglass import FunnyGlass
from escape.funny import Funny
from escape.terrifylava import TerrifyLava
from escape.calmladder import CalmLadder
from escape.interface import *
from mcpi import minecraft as mmc
from mcpi import block as block
from copy import deepcopy
import tools


class Chase:
    connections: List[Connection]
    levels: List[Process]
    windows: List[Window]
    positions: Dict[int, int]
    SPAWN_LEN = 9
    SPAWN_HEI = 9
    SPAWN_BLK = block.QUARTZ_BLOCK.id
    # LEVEL_LIST: List[Type[Level]] = [AngryAnvil]
    LEVEL_LIST: List[Type[Level]] = [AngryAnvil, TerrifyLava, FunnyGlass,Funny]

    def __init__(self, address='localhost', port=4711, spawn_point=V3(-1234, 64, -1234), direction=Dir.S):
        self.frontier = 0  # The index of the next level to construct
        self.spawn_point = spawn_point
        self.init_dir = direction
        self.address, self.port = address, port
        self.mc = mmc.Minecraft.create(address, port)

    def run(self):
        self.mc.execute("gamerule doTileDrops false")
        self.mc.clearDrop()
        players = self.mc.getPlayerEntityIds()
        # Window 0 -> Level 0 -> W1 -> L1 -> W2 -> ...
        self.levels, self.windows = [], [self._spawn()]
        self.mc.setBlock(self.windows[0].middle.down(), block.GLOWSTONE_BLOCK.id)
        # Positive for Level, negative for Window; 0 treated as Level 0
        self.positions = dict((p, 0) for p in players)
        self.connections = []
        for p in players:
            self.mc.clearInventory(p)
            self.mc.entity.setTilePos(p, self.spawn_point.up().randFlatCenter(min(self.SPAWN_LEN - 2, 3)))
            # self.mc.setGamemode(p, "adventure")
        self.forward()
        while True:
            self.update_pos()
            self.forward()

    def _spawn(self) -> Window:
        """Construct spawn and return the first Window"""
        walls = {'t': False, self.init_dir.value: False}
        tools.makeCubeAbove(self.mc, self.spawn_point, self.SPAWN_LEN + 2,
                            block.AIR.id, **walls)
        tools.makeCubeAbove(self.mc, self.spawn_point, self.SPAWN_LEN + 1,
                            self.SPAWN_BLK, **walls)
        return Window(tools.east_shift(self.spawn_point, V3(self.SPAWN_LEN // 2 + 1), self.init_dir).up(),
                      self.SPAWN_LEN // 2, self.SPAWN_HEI, self.init_dir)

    def forward(self):
        """Push the frontier farther with a new level"""
        while self.frontier < abs(max(self.positions.values(), key=abs)) + 2:
            level: Type[Level] = choice(self.LEVEL_LIST)
            my_conn, level_conn = Pipe()
            self.connections.append(my_conn)
            proc = Process(target=level,
                           args=(level_conn, self.address, self.port, self.windows[self.frontier]))
            self.levels.append(proc)
            self.windows.append(level.exitWin(deepcopy(self.windows[self.frontier])))
            proc.start()
            self.frontier += 1
            print(f"Forward with {level}, total: {self.frontier}")
            if self.frontier >= 5:
                i = self.frontier - 5
                self.connections[i].send((Cmd.TERM, []))
                self.connections[i].close()
                print(f"  TERM sent to level {i}")

    def update_pos(self):
        """Update the positions of players and inform the levels"""
        for pid, lvl in self.positions.items():
            if self.windows[lvl + 1].has_pos(self.mc.entity.getPos(pid)):
                # Reached the next level (window)
                self.connections[lvl].send((Cmd.EXI, [pid]))
                lvl += 1
                self.positions[pid] += 1
                self.connections[lvl].send((Cmd.ENT, [pid]))
                print(f"  Player {pid} proceeded to {lvl}")
                self.mc.postToChat(f"Player {pid} proceeded to {lvl}")


if __name__ == '__main__':
    start = V3(randint(-3000, 3000), 64, randint(-3000, 3000))
    c = Chase(spawn_point=start)
    print(f"Starting at {start}...")
    c.run()
