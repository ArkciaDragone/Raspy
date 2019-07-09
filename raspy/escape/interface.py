"""
Defines a few interfaces that should be used to communicate

The controlling program is called "Chase"
Level generators, defined below, are called "Level"
"""
import sys
from typing import List, Tuple
from time import sleep

sys.path.append("..")
import mcpi.minecraft as mmc
from abc import ABC, abstractmethod
from mcpi.vec3 import Vec3 as V3
from enum import Enum, IntEnum
from multiprocessing.connection import Connection


class Dir(Enum):
    """North, South, East, West, Bottom, Top"""
    N, S, E, W, B, T = 'n', 's', 'e', 'w', 'b', 't'


class Cmd(IntEnum):
    """Commands for Chase & Level communication"""
    TERM, ENT, EXI = 0, 1, 2


class Window:
    """The beginning and the end window frame of a Level"""
    def __init__(self, middle: V3, width: int, height: int, direction: Dir):
        """Middle for window bottom center (Vec3, int, int, Direction)"""
        self.middle = middle
        self.width = width
        self.height = height
        self.direction = direction

    def __repr__(self):
        return "<Window w={}, h={}, mid={}, d={}".format(
            self.width, self.height, self.middle, self.direction
        )


class Level(ABC):
    """Implement all the abstract methods to become a Level!"""
    players: List[int]

    @staticmethod  # The exit window is universally calculated for all instances
    @abstractmethod
    def exitWin(entrance: Window):
        """Tell Chase your exit Window. Both Chase and Level can make use of it"""
        pass

    def __init__(self, conn: Connection, address: str, port: int, entWin: Window):
        """Initialize a level generator

        conn: Used to communicate with the Chase
        address: Connection address to start a new mcpi connection
        port: Connection port to start a new mcpi connection
        entrance: The entrance window to begin level with
        """
        self.conn = conn
        self.mc = mmc.Minecraft.create(address, port)
        self.entWin = entWin
        self.__construct()
        self.players = []  # Player id, read from here
        while True:
            while conn.poll():
                rec: Tuple[Cmd, List] = conn.recv()  # New msg
                if rec[0] == Cmd.TERM:
                    self.__cleanup()
                    return
                elif rec[0] == Cmd.ENT:
                    self.players.extend(rec[1])
                elif rec[0] == Cmd.EXI:
                    for i in rec[1]:
                        try:
                            self.players.remove(i)
                        except ValueError:
                            sys.stderr.write("Player(id) {} not found in {}!".format(
                                i, self.__repr__()
                            ))
            self.__loop()

    @abstractmethod
    def __construct(self):
        """This will only be called once at the beginning. Window in "self.entWin\""""
        pass

    @abstractmethod
    def __loop(self):
        """Main loop to maintain your level. Player ids in "self.players\""""
        pass

    @abstractmethod
    def __cleanup(self):
        """Called when exit to do some clean up job if necessary"""
        pass
