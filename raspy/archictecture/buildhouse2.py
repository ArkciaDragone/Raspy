#将buildhouse的最新版本改成函数

import sys
sys.path.append("..")

import mcpi.minecraft as minecraft
import mcpi.block as block

import random

mc=minecraft.Minecraft.create()

def house():

    midx=x+SIZE/2
    midy=y+SIZE/2
    midz=z+SIZE/2

    #整体

    mc.setBlocks(x,y,z,x+SIZE,y+SIZE,z+SIZE,block.COBBLESTONE.id)

    #填入空气

    mc.setBlocks(x+1,y,z+1,x+SIZE-2,y+SIZE-1,z+SIZE-2,block.AIR.id)

    #门

    mc.setBlocks(midx-SIZE/10,y,z,midx+SIZE/10,y+SIZE*3/10,z,block.AIR.id)

    #玻璃窗户
    mc.setBlocks(x+3*SIZE/10,y+SIZE-3*SIZE/10,z,midx-3*SIZE/10,midy+3*SIZE/10,z,block.GLASS.id)
    mc.setBlocks(midx+3*SIZE/10,y+SIZE-3*SIZE/10,z,x+SIZE-3*SIZE/10,midy+3*SIZE/10,z,block.GLASS.id)

    #增加一个木制屋顶
    mc.setBlocks(x,y+SIZE-1,z,x+SIZE,y+SIZE,z+SIZE,block.WOOD.id)

    #开个天窗
    mc.setBlocks(midx-SIZE/4,y+SIZE-1,midz-SIZE/4,midx+SIZE/4,y+SIZE,midz+SIZE/4,block.GLASS.id)


    #增加一个羊毛毯
    c=random.randint(0,15)
    
    mc.setBlocks(x+1,y-1,z+1,x+SIZE-2,y-1,z+SIZE-2,block.WOOL.id,c)

pos=mc.player.getTilePos()

#确定基准点

SIZE=eval(input("The size of the house?"))

x=pos.x+2
y=pos.y
z=pos.z

for i in range(5):

    house()

    x=x+SIZE

house()
