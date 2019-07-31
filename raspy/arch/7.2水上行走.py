#水上行走/脚底产生玻璃

import sys
sys.path.append("..")

import mcpi.minecraft as minecraft
import mcpi.block as block

mc=minecraft.Minecraft.create()


while True:

    pos=mc.player.getTilePos()

    mc.setBlock(pos.x,pos.y-1,pos.z,block.GLASS.id) #将玩家脚下的方块替换成玻璃。

   
