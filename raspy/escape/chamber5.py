import sys
sys.path.append("..")
import tools, random, time
mc=tools.start(0)
setbs=mc.setBlocks
pId = mc.getPlayerEntityId(map(mc.entity.getName, mc.getPlayerEntityIds()))
start = mc.entity.getTilePos(pId)
WIDTH=10
LENGTH=20
BLOCK_ID=57
HEIGHT=5

def track(direction,x,z):
    if direction=='s':
        setbs(x-WIDTH//2,HEIGHT-2,z+1,x+WIDTH//2,HEIGHT-2,z+LENGTH+1,29,1)
        setbs(x-WIDTH//2,HEIGHT-1,z+1,x+WIDTH//2,HEIGHT-1,z+LENGTH+1,BLOCK_ID)
        setbs(x-(WIDTH//2+1),HEIGHT,z,x+(WIDTH//2+1),HEIGHT,z+LENGTH+2,BLOCK_ID)
        setbs(x-WIDTH//2,HEIGHT,z+1,x+WIDTH//2,HEIGHT,z+LENGTH+1,11)#lava
        setbs(x-WIDTH//2,HEIGHT-4,z+1,x+WIDTH//2,HEIGHT-4,z+LENGTH+1,3)#dirt
        setbs(x-WIDTH//2,HEIGHT-3,z+1,x+WIDTH//2,HEIGHT-3,z+LENGTH+1,0)#air
    elif direction=='n':
        setbs(x-WIDTH//2,HEIGHT-2,z-1,x+WIDTH//2,HEIGHT-2,z-LENGTH-1,29,1)
        setbs(x-WIDTH//2,HEIGHT-1,z-1,x+WIDTH//2,HEIGHT-1,z-LENGTH-1,BLOCK_ID)
        setbs(x-(WIDTH//2+1),HEIGHT,z,x+(WIDTH//2+1),HEIGHT,z-LENGTH-2,BLOCK_ID)
        setbs(x-WIDTH//2,HEIGHT,z-1,x+WIDTH//2,HEIGHT,z-LENGTH-1,11)
        setbs(x-WIDTH//2,HEIGHT-4,z-1,x+WIDTH//2,HEIGHT-4,z-LENGTH-1,3)
        setbs(x-WIDTH//2,HEIGHT-3,z-1,x+WIDTH//2,HEIGHT-3,z-LENGTH-1,0)
    elif direction=='e':
        setbs(x+1,HEIGHT-2,z-WIDTH//2,x+LENGTH+1,HEIGHT-2,z+WIDTH//2,29,1)
        setbs(x+1,HEIGHT-1,z-WIDTH//2,x+LENGTH+1,HEIGHT-1,z+WIDTH//2,BLOCK_ID)
        setbs(x,HEIGHT,z-(WIDTH//2+1),x+LENGTH+2,HEIGHT,z+(WIDTH//2+1),BLOCK_ID)
        setbs(x+1,HEIGHT,z-WIDTH//2,x+LENGTH+1,HEIGHT,z+WIDTH//2,11)
        setbs(x+1,HEIGHT-4,z-WIDTH//2,x+LENGTH+1,HEIGHT-4,z+WIDTH//2,3)
        setbs(x+1,HEIGHT-3,z-WIDTH//2,x+LENGTH+1,HEIGHT-3,z+WIDTH//2,0)
    elif direction=='w':
        setbs(x-1,HEIGHT-2,z-WIDTH//2,x-LENGTH-1,HEIGHT-2,z+WIDTH//2,29,1)
        setbs(x-1,HEIGHT-1,z-WIDTH//2,x-LENGTH-1,HEIGHT-1,z+WIDTH//2,BLOCK_ID)
        setbs(x,HEIGHT,z-(WIDTH//2+1),x-LENGTH-2,HEIGHT,z+(WIDTH//2+1),BLOCK_ID)
        setbs(x-1,HEIGHT,z-WIDTH//2,x-LENGTH-1,HEIGHT,z+WIDTH//2,11)
        setbs(x-1,HEIGHT-4,z-WIDTH//2,x-LENGTH-1,HEIGHT-4,z+WIDTH//2,3)
        setbs(x-1,HEIGHT-3,z-WIDTH//2,x-LENGTH-1,HEIGHT-3,z+WIDTH//2,0)

direction=input('the direction is:')
track(direction,start.x,start.z)


