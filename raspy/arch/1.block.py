#自动放置一个方块

import sys
sys.path.append("..")

import mcpi.minecraft as minecraft
import mcpi.block as block

mc=minecraft.Minecraft.create()

pos=mc.player.getTilePos()

mc.setBlock(pos.x+3,pos.y,pos.z,35)


"""
#这三根柱子是用来找x,y,z正方向用的。
for i in range(5):
    mc.setBlock(pos.x+i,pos.y,pos.z,i+1)
    mc.setBlock(pos.x,pos.y+2+i,pos.z,i+1)
    mc.setBlock(pos.x,pos.y,pos.z+i,i+1)

"""

"""

#通天神塔，hhh~
for i in range(30):
    mc.setBlock(pos.x+1,pos.y+i,pos.z,41)

"""
    
