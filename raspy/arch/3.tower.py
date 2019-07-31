#建造一座巨塔


import sys
sys.path.append("..")

import mcpi.minecraft as minecraft
import mcpi.block as block
mc=minecraft.Minecraft.create()

pos=mc.player.getTilePos()

for i in range(50):
    mc.setBlock(pos.x+3,pos.y+i,pos.z,41)







"""

import sys
sys.path.append("..")
import tools
mc=tools.start(0)


import mcpi.minecraft as minecraft
import mcpi.block as block



pos=mc.player.getTilePos()

for i in range(50):
    mc.setBlock(pos.x+3,pos.y+i,pos.z,41)

"""


"""

import sys
sys.path.append("..")


import mcpi.minecraft as minecraft
import mcpi.block as block
mc=minecraft.Minecraft.create()

import sys
sys.path.append("..")
import tools
mc=tools.start(0)



pos=mc.player.getTilePos()

for i in range(50):
    mc.setBlock(pos.x+3,pos.y+i,pos.z,41)

"""

        
