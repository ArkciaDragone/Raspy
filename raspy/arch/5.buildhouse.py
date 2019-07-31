"""

#建造一个房子

import sys
sys.path.append("..")

import mcpi.minecraft as minecraft
import mcpi.block as block

mc=minecraft.Minecraft.create()

SIZE=20

pos=mc.player.getTilePos()

#确定基准点
x=pos.x+2
y=pos.y
z=pos.z

midx=x+SIZE/2
midy=y+SIZE/2

#整体

mc.setBlocks(x,y,z,x+SIZE,y+SIZE,z+SIZE,block.COBBLESTONE.id)

#填入空气

mc.setBlocks(x+1,y,z+1,x+SIZE-2,y+SIZE-1,z+SIZE-2,block.AIR.id)

#门

mc.setBlocks(midx-1,y,z,midx+1,y+3,z,block.AIR.id)

#玻璃窗户
mc.setBlocks(x+3,y+SIZE-3,z,midx-3,midy+3,z,block.GLASS.id)
mc.setBlocks(midx+3,y+SIZE-3,z,x+SIZE-3,midy+3,z,block.GLASS.id)

#增加一个木制屋顶
mc.setBlocks(x,y+SIZE-1,z,x+SIZE,y+SIZE-1,z+SIZE,block.WOOD.id)

#增加一个羊毛毯
mc.setBlocks(x+1,y-1,z+1,x+SIZE-2,y-1,z+SIZE-2,block.WOOL.id,14)

"""

"""


#房顶换成了玻璃的，这样不容易刷怪

import sys
sys.path.append("..")

import mcpi.minecraft as minecraft
import mcpi.block as block

mc=minecraft.Minecraft.create()

SIZE=20

pos=mc.player.getTilePos()

#确定基准点
x=pos.x+2
y=pos.y
z=pos.z

midx=x+SIZE/2
midy=y+SIZE/2

#整体

mc.setBlocks(x,y,z,x+SIZE,y+SIZE,z+SIZE,block.COBBLESTONE.id)

#填入空气

mc.setBlocks(x+1,y,z+1,x+SIZE-2,y+SIZE-1,z+SIZE-2,block.AIR.id)

#门

mc.setBlocks(midx-1,y,z,midx+1,y+3,z,block.AIR.id)

#玻璃窗户
mc.setBlocks(x+3,y+SIZE-3,z,midx-3,midy+3,z,block.GLASS.id)
mc.setBlocks(midx+3,y+SIZE-3,z,x+SIZE-3,midy+3,z,block.GLASS.id)

#增加一个木制屋顶
mc.setBlocks(x,y+SIZE,z,x+SIZE,y+SIZE,z+SIZE,block.GLASS.id)

#增加一个羊毛毯
mc.setBlocks(x+1,y-1,z+1,x+SIZE-2,y-1,z+SIZE-2,block.WOOL.id,14)

"""


"""

#太黑了，点蜡烛啊！

import sys
sys.path.append("..")

import mcpi.minecraft as minecraft
import mcpi.block as block

mc=minecraft.Minecraft.create()

SIZE=20

pos=mc.player.getTilePos()

#确定基准点
x=pos.x+2
y=pos.y
z=pos.z

midx=x+SIZE/2
midy=y+SIZE/2
midz=z+SIZE/2


#整体

mc.setBlocks(x,y,z,x+SIZE,y+SIZE,z+SIZE,block.COBBLESTONE.id)

#填入空气

mc.setBlocks(x+1,y,z+1,x+SIZE-2,y+SIZE-1,z+SIZE-2,block.AIR.id)

#门

mc.setBlocks(midx-1,y,z,midx+1,y+3,z,block.AIR.id)

#玻璃窗户
mc.setBlocks(x+3,y+SIZE-3,z,midx-3,midy+3,z,block.GLASS.id)
mc.setBlocks(midx+3,y+SIZE-3,z,x+SIZE-3,midy+3,z,block.GLASS.id)

#增加一个木制屋顶
mc.setBlocks(x,y+SIZE-1,z,x+SIZE,y+SIZE-1,z+SIZE,block.WOOD.id)

#增加一个羊毛毯
mc.setBlocks(x+1,y-1,z+1,x+SIZE-2,y-1,z+SIZE-2,block.WOOL.id,14)

#点蜡烛
#八个角
mc.setBlock(x+1,y,z,block.TORCH.id)
mc.setBlock(x+SIZE-1,y,z,block.TORCH.id)
mc.setBlock(x,y,z+SIZE-1,block.TORCH.id)
mc.setBlock(x+SIZE-1,y,z+SIZE-1,block.TORCH.id)
mc.setBlock(x+1,y+SIZE-1,z,block.TORCH.id)
mc.setBlock(x+SIZE-1,y+SIZE-1,z,block.TORCH.id)
mc.setBlock(x,y+SIZE-1,z+SIZE-1,block.TORCH.id)
mc.setBlock(x+SIZE-1,y+SIZE-1,z+SIZE-1,block.TORCH.id)

#六个面中心
mc.setBlock(midx,midy,z,block.TORCH.id)
mc.setBlock(midx,midy,z+SIZE,block.TORCH.id)
mc.setBlock(x,midy+SIZE,midz+SIZE,block.TORCH.id)
mc.setBlock(x,midy+SIZE,midz+SIZE,block.TORCH.id)
mc.setBlock(midx,y+SIZE-1,midz,block.TORCH.id)
mc.setBlock(midx,y,midz,block.TORCH.id)

"""



#算了，还是开天窗吧。……效果非常好！！！比插蜡烛什么的采光好多了！！！顺便修改了门和窗户的参数使门也是按比例操作。

import sys
sys.path.append("..")

import mcpi.minecraft as minecraft
import mcpi.block as block

mc=minecraft.Minecraft.create()

SIZE=eval(input("The size of the house?"))

pos=mc.player.getTilePos()

#确定基准点
x=pos.x+2
y=pos.y
z=pos.z

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
mc.setBlocks(x+1,y-1,z+1,x+SIZE-2,y-1,z+SIZE-2,block.WOOL.id,14)











