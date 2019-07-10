"""Author: HarryTerpee
   Theme: Angry Anvil!!!"""
from interface import *
from typing import Dict
import random

class AngryAnvil(Level):
    LENGTH=100
    NUMBERBER=LENGTH//4
    FLASH_PERIOD=0.5
    FLASH_TIMES=3
    
    def exitWin(entrance: Window):
        if direction=Dir.N:
            entrance.middle.z-=LENGTH
        elif direction=Dir.S:
            entrance.middle.z+=LENGTH
        elif direction=Dir.E:
            entrance.middle.x+=LENGTH
        elif direction=Dir.W:
            entrance.middle.x-=LENGTH
        entrance.width=3
        entrance.height=10
        return entrance
    
    def __construct(self):
        if self.entWin.direction=Dir.N:
            setbs(x-1,y-1,z,x+1,y-1,z-LENGTH,159,4)
            setbs(x-2,y-1,z,x-2,y+10,z-LENGTH,24,1)
            setbs(x+2,y-1,z,x+2,y+10,z-LENGTH,24,1)
        elif self.entWin.direction=Dir.S:
            setbs(x-1,y-1,z,x+1,y-1,z+LENGTH,159,4)
            setbs(x-2,y-1,z,x-2,y+10,z+LENGTH,24,1)
            setbs(x+2,y-1,z,x+2,y+10,z+LENGTH,24,1)
        elif self.entWin.direction=Dir.E:
            setbs(x,y-1,z-1,x+LENGTH,y-1,z+1,159,4)
            setbs(x,y-1,z-2,x+LENGTH,y+10,z-2,24,1)
            setbs(x,y-1,z+2,x+LENGTH,y+10,z+2,24,1)
        elif self.entWin.direction=Dir.W:
            setbs(x,y-1,z-1,x-LENGTH,y-1,z+1,159,4)
            setbs(x,y-1,z-2,x-LENGTH,y+10,z-2,24,1)
            setbs(x,y-1,z+2,x-LENGTH,y+10,z+2,24,1)

    def __area(self) -> Dict:
        """选定并返回闪烁地点"""
        x=self.entWin.x
        y=self.entWin.y
        z=self.entWin.z
        direction=self.entWin.direction
        pos={}
        setbs=self.mc.setBlocks
        if direction=='s':
            for m in range(0,NUMBER):
                i=random.randint(x-1,x+1)
                j=random.randint(z,z+LENGTH)
                pos[m]=[i,y,j]
        elif direction=='n':
            for m in range(0,NUMBER):
                i=random.randint(x-1,x+1)
                j=random.randint(z-LENGTH,z)
                pos[m]=[i,y,j]
        elif direction=='w':
            for m in range(0,NUMBER):
                i=random.randint(z-1,z+1)
                j=random.randint(x-LENGTH,x)
                pos[m]=[j,y,i]
        elif direction=='e':
            for m in range(0,NUMBER):
                i=random.randint(z-1,z+1)
                j=random.randint(x,x+LENGTH)
                pos[m]=[j,y,i]
        return pos

    def __loop(self):
        """闪烁，落铁砧"""
        x=self.entWin.x
        y=self.entWin.y
        z=self.entWin.z
        setb=self.mc.setBlock
        direction=self.entWin.direction
        pos=self.__area()
        i=0
        while i<FLASH_TIMES:
            for m in range(0,NUMBER):
                setb(pos[m][0],pos[m][1]-1,pos[m][2],159,4)#yellow clay
            time.sleep(FLASH_PERIOD)
            for m in range(0,NUMBER):
                setb(pos[m][0],pos[m][1]-1,pos[m][2],159,14)#red clay
            time.sleep(FLASH_PERIOD)
            for m in range(0,NUMBER):
                if i==1:setb(pos[m][0],pos[m][1]+7,pos[m][2],145)#anvil
            i+=1
    
    
            
