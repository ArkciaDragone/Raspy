"""Author: HarryTerpee
   Theme: Angry Anvil!!!"""
from escape.interface import *
from mcpi import block
import random
from time import sleep


class AngryAnvil(Level):
    LENGTH = 20
    NUMBER = LENGTH // 4
    FLASH_PERIOD = 0.5
    FLASH_TIMES = 3
    ANV = block.ANVIL.id
    SHC = block.STAINED_HARDENED_CLAY.id
    SND = block.SANDSTONE.id

    @staticmethod
    def exitWin(entrance: Window):
        dir = entrance.direction
        if dir == Dir.N:
            entrance.middle.z -= AngryAnvil.LENGTH
        elif dir == Dir.S:
            entrance.middle.z += AngryAnvil.LENGTH
        elif dir == Dir.E:
            entrance.middle.x += AngryAnvil.LENGTH
        elif dir == Dir.W:
            entrance.middle.x -= AngryAnvil.LENGTH
        entrance.height = 10
        return entrance

    def _construct(self):
        LENGTH = self.LENGTH
        setbs = self.mc.setBlocks
        x, y, z = self.entWin.middle
        width = self.entWin.width
        if self.entWin.direction == Dir.N:
            setbs(x - 1, y - 1, z, x + 1, y - 1, z - LENGTH, self.SHC, 4)
            setbs(x - 2, y - 1, z, x - 2, y + 10, z - LENGTH, self.SND, 1)
            setbs(x + 2, y - 1, z, x + 2, y + 10, z - LENGTH, self.SND, 1)
            setbs(x - width // 2, y - 1, z, x - 2, y + 10, z, self.SND, 1)
            setbs(x + width // 2, y - 1, z, x + 2, y + 10, z, self.SND, 1)
        elif self.entWin.direction == Dir.S:
            setbs(x - 1, y - 1, z, x + 1, y - 1, z + LENGTH, self.SHC, 4)
            setbs(x - 2, y - 1, z, x - 2, y + 10, z + LENGTH, self.SND, 1)
            setbs(x + 2, y - 1, z, x + 2, y + 10, z + LENGTH, self.SND, 1)
            setbs(x - width // 2, y - 1, z, x - 2, y + 10, z, self.SND, 1)
            setbs(x + width // 2, y - 1, z, x + 2, y + 10, z, self.SND, 1)
        elif self.entWin.direction == Dir.E:
            setbs(x, y - 1, z - 1, x + LENGTH, y - 1, z + 1, self.SHC, 4)
            setbs(x, y - 1, z - 2, x + LENGTH, y + 10, z - 2, self.SND, 1)
            setbs(x, y - 1, z + 2, x + LENGTH, y + 10, z + 2, self.SND, 1)
            setbs(x, y - 1, z - width // 2, x, y + 10, z - 2, self.SND, 1)
            setbs(x, y - 1, z + width // 2, x, y + 10, z + 2, self.SND, 1)
        elif self.entWin.direction == Dir.W:
            setbs(x, y - 1, z - 1, x - LENGTH, y - 1, z + 1, self.SHC, 4)
            setbs(x, y - 1, z - 2, x - LENGTH, y + 10, z - 2, self.SND, 1)
            setbs(x, y - 1, z + 2, x - LENGTH, y + 10, z + 2, self.SND, 1)
            setbs(x, y - 1, z - width // 2, x, y + 10, z - 2, self.SND, 1)
            setbs(x, y - 1, z + width // 2, x, y + 10, z + 2, self.SND, 1)

    def area(self) -> List[Tuple[int, int, int]]:
        """选定并返回闪烁地点"""
        x, y, z = self.entWin.middle
        direction = self.entWin.direction
        pos = []
        for _ in range(0, self.NUMBER):
            if direction == Dir.S:
                i = random.randint(x - 1, x + 1)
                j = random.randint(z, z + self.LENGTH)
                pos.append((i, y, j))
            elif direction == Dir.N:
                i = random.randint(x - 1, x + 1)
                j = random.randint(z - self.LENGTH, z)
                pos.append((i, y, j))
            elif direction == Dir.W:
                i = random.randint(z - 1, z + 1)
                j = random.randint(x - self.LENGTH, x)
                pos.append((j, y, i))
            elif direction == Dir.E:
                i = random.randint(z - 1, z + 1)
                j = random.randint(x, x + self.LENGTH)
                pos.append((j, y, i))
        return pos

    def _loop(self):
        """闪烁，落铁砧"""
        setb = self.mc.setBlock
        pos = self.area()
        i = 0
        while i < self.FLASH_TIMES:
            for m in range(0, self.NUMBER):
                setb(pos[m][0], pos[m][1] - 1, pos[m][2], self.SHC, 4)  # yellow clay
            sleep(self.FLASH_PERIOD)
            for m in range(0, self.NUMBER):
                setb(pos[m][0], pos[m][1] - 1, pos[m][2], self.SHC, 14)  # red clay
            sleep(self.FLASH_PERIOD)
            for m in range(0, self.NUMBER):
                if i == 1: setb(pos[m][0], pos[m][1] + 7, pos[m][2], self.ANV)  # anvil
            i += 1

    def _cleanup(self):
        pass
