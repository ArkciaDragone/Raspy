#通天金塔

import sys
sys.path.append("..")
import mcpi.minecraft as minecraft
import mcpi.block as block
mc=minecraft.Minecraft.create()

pos=mc.player.getTilePos()

h=eval(input("Enter the height of the golden tower?"))

for i in range(h):

    mc.setBlock(pos.x+3,pos.y+i,pos.z,block.GOLD_BLOCK.id)
