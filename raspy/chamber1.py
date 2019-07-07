import mcpi.minecraft as mmc
import tools,time
import mcpi.block as block
import mcpi.entity as entity
import mcpi.vec3 as vec3
import escape.tnt
V3 = vec3.Vec3
mc=tools.start(0)
import random,math
setb=mc.setBlock
setbs=mc.setBlocks
wall=block.DIAMOND_BLOCK
deco=block.BEACON
def east(x,y,z):
    setbs(x,y-2,z-5,x+20,y-1,z+5,wall) #floor
    setbs(x,y-1,z-5,x+20,y+5,z-5,wall) #leftwall
    setbs(x,y-1,z+5,x+20,y+5,z+5,wall) #rightwall
    #setbs(x,y+5,z-5,x+20,y+5,z+5,wall) #ceiling
    setbs(x,y+2,z-5,x+20,y+2,z-5,deco) #leftBeacon
    setbs(x,y+2,z+5,x+20,y+2,z+5,deco) #rightBeacon
    setbs(x+3,y-1,z-4,x+17,y-1,z+4,10) #lava
    for i in range(x+3,x+17,3):         #step
        for j in range(z-4,z+4,3):
            m=random.randint(0,3)
            setbs(i+m,y-1,j+m,i+m+1,y-1,j+m,57)

def west(x,y,z):
    setbs(x,y-2,z-5,x-20,y-1,z+5,wall)
    setbs(x,y-1,z-5,x-20,y+5,z-5,wall)
    setbs(x,y-1,z+5,x-20,y+5,z+5,wall)
    #setbs(x,y+5,z-5,x-20,y+5,z+5,wall)
    setbs(x,y+2,z-5,x-20,y+2,z-5,deco)
    setbs(x,y+2,z+5,x-20,y+2,z+5,deco)
    setbs(x-3,y-1,z-4,x-17,y-1,z+4,10)
    for i in range(x-3,x-17,-3):
        for j in range(z-4,z+4,3):
            m=random.randint(0,3)
            setbs(i-m,y-1,j+m,i-m-1,y-1,j+m,57)

def south(x,y,z):
    setbs(x-5,y-2,z,x+5,y-1,z+20,wall)
    setbs(x-5,y-1,z,x-5,y+5,z+20,wall)
    setbs(x+5,y-1,z,x+5,y+5,z+20,wall)
    #setbs(x-5,y+5,z,x+5,y+5,z+20,wall)
    setbs(x+5,y+2,z,x+5,y+2,z+20,deco)
    setbs(x-5,y+2,z,x-5,y+2,z+20,deco)
    setbs(x-4,y-1,z+3,x+4,y-1,z+17,10)
    for i in range(z+3,z+17,3):
        for j in range(x-4,x+4,3):
            m=random.randint(0,3)
            setbs(j+m,y-1,i+m,j+m,y-1,i+m+1,57)

def north(x,y,z):
    setbs(x-5,y-2,z,x+5,y-1,z-20,wall)
    setbs(x-5,y-1,z,x-5,y+5,z-20,wall)
    setbs(x+5,y-1,z,x+5,y+5,z-20,wall)
    #setbs(x-5,y+5,z,x+5,y+5,z-20,wall)
    setbs(x+5,y+2,z,x+5,y+2,z-20,deco)
    setbs(x-5,y+2,z,x-5,y+2,z-20,deco)
    setbs(x-4,y-1,z-3,x+4,y-1,z-17,10)
    for i in range(z-3,z-17,-3):
        for j in range(x-4,x+4,3):
            m=random.randint(0,3)
            setbs(j+m,y-1,i-m,j+m,y-1,i-m-1,57)


start=map(int,input('the starting position:').split())
direction=input('''the starting direction(east='e',north='n',south='s',west='w'):''')
pId=mc.getPlayerEntityId(map(mc.entity.getName, mc.getPlayerEntityIds()))
mc.entity.setTilePos(pId,start)
start=mc.entity.getTilePos(pId)
x=start.x
y=start.y
z=start.z
setchance=int(input('this task will be set for how many times:'))

if direction=='e':
    east(x,y,z)
    i=0
    while i<setchance:
        while True:
            if mc.entity.getTilePos(pId).x > x+5:
                x+=18
                east(x,y,z)
                break
            time.sleep(0.1)
        i+=1
elif direction=='n':
    north(x,y,z)
    i=0
    while i<setchance:
        while True:
            if mc.entity.getTilePos(pId).z < z-5:
                z-=18
                nprth(x,y,z)
                break
            time.sleep(0.1)
        i+=1
elif direction=='s':
    south(x,y,z)
    i=0
    while i<setchance:
        while True:
            if mc.entity.getTilePos(pId).z > z+5:
                z+=18
                south(x,y,z)
                break
            time.sleep(0.1)
        i+=1
elif direction=='w':
    west(x,y,z)
    i=0
    while i<setchance:
        while True:
            if mc.entity.getTilePos(pId).x < x-5:
                x-=18
                west(x,y,z)
                break
            time.sleep(0.1)
        i+=1
