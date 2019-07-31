#做一个骰子

import sys
sys.path.append("..")


import mcpi.minecraft as minecraft
import mcpi.block as block

mc=minecraft.Minecraft.create()

pos=mc.player.getTilePos()


# 一面白墙
for h in range(6):   # h=height
    for w in range(7):  # w=width
        mc.setBlock(pos.x+3,pos.y+h,pos.z-1+w,251)

# 点数
mc.setBlock(pos.x+3,pos.y,pos.z,2)
mc.setBlock(pos.x+3,pos.y+2,pos.z,2)
mc.setBlock(pos.x+3,pos.y+4,pos.z,2)
mc.setBlock(pos.x+3,pos.y,pos.z+4,2)
mc.setBlock(pos.x+3,pos.y+2,pos.z+4,2)
mc.setBlock(pos.x+3,pos.y+4,pos.z+4,2)
