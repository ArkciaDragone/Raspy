import sys
sys.path.append("..")
import mcpi.minecraft as minecraft
import mcpi.block as block
mc=minecraft.Minecraft.create()

pos=mc.player.getTilePos()

mc.setBlocks(pos.x,pos.y,pos.z-50,pos.x+50,pos.y+50,pos.z+50,block.LAVA.id)

while True:

    pos=mc.player.getTilePos()

    mc.setBlocks(pos.x,pos.y,pos.z-10,pos.x+10,pos.y+70,pos.z+10,block.AIR.id)
