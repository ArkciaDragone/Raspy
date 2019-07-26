"""
Author: HarryTerpee
Theme: Funny Glass
"""
from escape.interface import *
import random
from time import sleep

LENGTH = 50


class FunnyGlass(Level):

    def exitWin(entrance: Window):
        dir = entrance.direction
        if dir == Dir.N:
            entrance.middle.z -= LENGTH
        elif dir == Dir.S:
            entrance.middle.z += LENGTH
        elif dir == Dir.E:
            entrance.middle.x += LENGTH
        elif dir == Dir.W:
            entrance.middle.x -= LENGTH
        entrance.height = 7
        return entrance
        
    def _construct(self):
        setbs = self.mc.setBlocks
        x, y, z = self.entWin.middle
        WIDTH = self.entWin.width
        HALFWIDTH = WIDTH//2
        direction = self.entWin.direction
        color = random.randint(1, 16)
        if direction == 'e':
            setbs(x + 1, y - 1, z - HALFWIDTH, x + LENGTH, y - 1, z + HALFWIDTH, 160, color)
            setbs(x + 1, y - 1, z - WIDTH // 2 - 1, x + LENGTH, y + 7, z - WIDTH // 2 - 1, 95, color)
            setbs(x + 1, y - 1, z + WIDTH // 2 + 1, x + LENGTH, y + 7, z + WIDTH // 2 + 1, 95, color)
            setbs(x + 1, y + 7, z + WIDTH // 2 + 1, x + LENGTH, y + 7, z - WIDTH // 2 - 1, 95, color)
            setbs(x + 1, y - 2, z - HALFWIDTH, x + LENGTH, 0, z + HALFWIDTH, 0)
            setbs(x + 1, y - 1, z - HALFWIDTH, x + LENGTH, 0, z - WIDTH // 2, 0)
            setbs(x + 1, y - 1, z + HALFWIDTH, x + LENGTH, 0, z + WIDTH // 2, 0)
            for i in range(x + 1, x + LENGTH - 2, 2):
                for j in range(z - HALFWIDTH, z + HALFWIDTH, 2):
                    m = random.randint(0, 2)
                    setbs(i + m, y - 1, j + m, i + m + 1, y - 1, j + m, 0)
        elif direction == 'w':
            setbs(x - 1, y - 1, z - HALFWIDTH, x - LENGTH, y - 1, z + HALFWIDTH, 160, color)
            setbs(x - 1, y - 1, z - WIDTH // 2 - 1, x - LENGTH, y + 7, z - WIDTH // 2 - 1, 95, color)
            setbs(x - 1, y - 1, z + WIDTH // 2 + 1, x - LENGTH, y + 7, z + WIDTH // 2 + 1, 95, color)
            setbs(x - 1, y + 7, z + WIDTH // 2 + 1, x - LENGTH, y + 7, z - WIDTH // 2 - 1, 95, color)
            setbs(x - 1, y - 2, z - HALFWIDTH, x - LENGTH, 0, z + HALFWIDTH, 0)
            setbs(x - 1, y - 1, z - HALFWIDTH, x - LENGTH, 0, z - WIDTH // 2, 0)
            setbs(x - 1, y - 1, z + HALFWIDTH, x - LENGTH, 0, z + WIDTH // 2, 0)
            for i in range(x - LENGTH, x - 3, 2):
                for j in range(z - HALFWIDTH, z + HALFWIDTH, 2):
                    m = random.randint(0, 2)
                    setbs(i + m, y - 1, j + m, i + m + 1, y - 1, j + m, 0)
        elif direction == 'n':
            setbs(x - HALFWIDTH, y - 1, z - 1, x + HALFWIDTH, y - 1, z - LENGTH, 160, color)
            setbs(x - WIDTH // 2 - 1, y - 1, z - 1, x - WIDTH // 2 - 1, y + 7, z - LENGTH, 95, color)
            setbs(x + WIDTH // 2 + 1, y - 1, z - 1, x + WIDTH // 2 + 1, y + 7, z - LENGTH, 95, color)
            setbs(x + WIDTH // 2 + 1, y + 7, z - 1, x - WIDTH // 2 - 1, y + 7, z - LENGTH, 95, color)
            setbs(x - HALFWIDTH, y - 2, z - 1, x + HALFWIDTH, 0, z - LENGTH, 0)
            setbs(x - HALFWIDTH, y - 1, z - 1, x - WIDTH // 2, 0, z - LENGTH, 0)
            setbs(x + HALFWIDTH, y - 1, z - 1, x + WIDTH // 2, 0, z - LENGTH, 0)
            for i in range(z - LENGTH, z - 3, 2):
                for j in range(x - HALFWIDTH, x + HALFWIDTH, 2):
                    m = random.randint(0, 2)
                    setbs(j + m, y - 1, i + m, j + m, y - 1, i + m + 1, 0)
        elif direction == 's':
            setbs(x - HALFWIDTH, y - 1, z + 1, x + HALFWIDTH, y - 1, z + LENGTH, 160, color)
            setbs(x - WIDTH // 2 - 1, y - 1, z + 1, x - WIDTH // 2 - 1, y + 7, z + LENGTH, 95, color)
            setbs(x + WIDTH // 2 + 1, y - 1, z + 1, x + WIDTH // 2 + 1, y + 7, z + LENGTH, 95, color)
            setbs(x + WIDTH // 2 + 1, y + 7, z + 1, x - WIDTH // 2 - 1, y + 7, z + LENGTH, 95, color)
            setbs(x - HALFWIDTH, y - 2, z + 1, x + HALFWIDTH, 0, z + LENGTH, 0)
            setbs(x - HALFWIDTH, y - 1, z + 1, x - WIDTH // 2, 0, z + LENGTH, 0)
            setbs(x + HALFWIDTH, y - 1, z + 1, x + WIDTH // 2, 0, z + LENGTH, 0)
            for i in range(z + 1, z + LENGTH - 2, 2):
                for j in range(x - HALFWIDTH, x + HALFWIDTH, 2):
                    m = random.randint(0, 2)
                    setbs(j + m, y - 1, i + m, j + m, y - 1, i + m + 1, 0)
    def _loop(self):
        """静态关卡"""
        pass

    def _cleanup(self):
        pass