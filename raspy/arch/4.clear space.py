

#用来清理空间用的，输入需要清理的空间的对角坐标即可。

import sys
sys.path.append("..")

import mcpi.minecraft as minecraft
import mcpi.block as block

mc=minecraft.Minecraft.create()


pos=mc.player.getTilePos()
size = int(input("size of the area to clear?"))


mc.setBlocks(pos.x,pos.y,pos.z,pos.x+size,pos.y+size,pos.z+size,block.WATER.id)


"""


#用来清理空间用的，以我为中心……站在地面上，结果基岩穿了……

import sys
sys.path.append("..")

import mcpi.minecraft as minecraft
import mcpi.block as block

mc=minecraft.Minecraft.create()


pos=mc.player.getTilePos()
size = int(input("size of the area to clear?"))


mc.setBlocks(pos.x-size/2,pos.y-size/2,pos.z-size/2,pos.x+size/2,pos.y+size/2,pos.z+size/2,block.AIR.id)


"""
