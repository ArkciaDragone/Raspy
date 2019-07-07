import tools,time
#输入TNT数量，0表示无限
def tntfollow(number):
    mc=tools.start(0)
    setb=mc.setBlock
    setbs=mc.setBlocks
    spawn=mc.spawnEntity
    pId=mc.getPlayerEntityId(map(mc.entity.getName, mc.getPlayerEntityIds()))
    start=mc.entity.getTilePos(pId)
    if number==0:
        while True:
            spawn(start.x,start.y+7,start.z,20)
            start=mc.entity.getTilePos(pId)
            time.sleep(1)
    else:
        i=0
        while i<number:
            spawn(start.x,start.y+7,start.z,20)
            start=mc.entity.getTilePos(pId)
            time.sleep(1)
            i+=1
    
            
