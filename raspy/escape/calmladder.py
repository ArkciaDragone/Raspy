"""
Author: HarryTerpee
Theme: Calm ladder
"""
from .interface import *
import random


class CalmLadder(Level):
    HEIGHT = 12
    def exitWin(entrance: Window):
        entrance.height = CalmLadder.HEIGHT
        if entrance.direction == Dir.N:
            entrance.direction = Dir.E
            entrance.middle.x += entrance.width // 2
            entrance.middle.y += CalmLadder.HEIGHT
            entrance.middle.z -= entrance.width // 2 + 1
        elif entrance.direction == Dir.E:
            entrance.direction = Dir.N
            entrance.middle.x += entrance.width // 2 + 1
            entrance.middle.y += CalmLadder.HEIGHT
            entrance.middle.z -= entrance.width // 2
        elif entrance.direction == Dir.S:
            entrance.direction = Dir.W
            entrance.middle.x -= entrance.width // 2
            entrance.middle.y += CalmLadder.HEIGHT
            entrance.middle.z += entrance.width // 2 + 1
        elif entrance.direction == Dir.W:
            entrance.direction = Dir.S
            entrance.middle.x -= entrance.width // 2 + 1
            entrance.middle.y += CalmLadder.HEIGHT
            entrance.middle.z += entrance.width // 2
        return entrance

    def setblock(self, x, y, z):
        self.mc.setBlock(x, y, z, 45)
        self.mc.setBlock(x + 1, y, z, 65, 5)
        self.mc.setBlock(x - 1, y, z, 65, 4)
        self.mc.setBlock(x, y, z + 1, 65, 3)
        self.mc.setBlock(x, y, z - 1, 65, 2)

    def _construct(self):
        direc = self.entWin.direction
        width = self.entWin.width
        halfwidth = width // 2
        x, y, z = self.entWin.middle
        if direc == Dir.N:
            for i in range(x - halfwidth, x + halfwidth, 2):
                for j in range(y - 1, y + self.HEIGHT, 3):
                    for k in range(z - width - 2, z - 1, 2):
                        m = random.randint(0, 3)
                        self.setblock(i + m, j + m, k + m)
        elif direc == Dir.S:
            for i in range(x - halfwidth, x + halfwidth, 2):
                for j in range(y - 1, y + self.HEIGHT, 3):
                    for k in range(z + 1, z + width + 2, 2):
                        m = random.randint(0, 3)
                        self.setblock(i + m, j + m, k + m)
        elif direc == Dir.E:
            for i in range(x + 1, x + width + 2, 2):
                for j in range(y - 1, y + self.HEIGHT, 3):
                    for k in range(z - halfwidth, z + halfwidth, 2):
                        m = random.randint(0, 3)
                        self.setblock(i + m, j + m, k + m)
        elif direc == Dir.W:
            for i in range(x - width - 2, x - 1, 2):
                for j in range(y - 1, y + self.HEIGHT, 3):
                    for k in range(z - halfwidth, z + halfwidth, 2):
                        m = random.randint(0, 3)
                        self.setblock(i + m, j + m, k + m)

    def _loop(self):
        """静态关卡"""
        pass

    def _cleanup(self):
        pass
