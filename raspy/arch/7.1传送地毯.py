#传送地毯

import sys
sys.path.append("..")

import mcpi.minecraft as minecraft
import time

mc=minecraft.Minecraft.create()


x,y,z=eval(input("enter the position you want to move to? (x,y,z)"))

time.sleep(3)

pos=mc.player.getTilePos()

print(pos.x,pos.y,pos.z)

if pos.x >=14 and pos.z>=-2:

    mc.player.setTilePos(x,y,z)

    mc.postToChat("change!!!")
else:

    pass
    


