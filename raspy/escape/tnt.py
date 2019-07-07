import time, os
import tools
import mcpi.entity as entity


# 输入TNT数量，0表示无限
def tntfollow(server_port=0, number=0):
    """Generate TNT to follow the first player (server_port, tnt count)"""
    print("TNT follow started on {}".format(os.getpid()))
    mc = tools.start(server_port)
    spawn = mc.spawnEntity
    pId = mc.getPlayerEntityIds()[0]
    pos = mc.entity.getTilePos(pId)
    if number == 0:
        while True:
            spawn(pos.up(7), entity.PRIMED_TNT.id)
            pos = mc.entity.getTilePos(pId)
            time.sleep(1)
    else:
        i = 0
        while i < number:
            spawn(pos.up(7), entity.PRIMED_TNT.id)
            pos = mc.entity.getTilePos(pId)
            time.sleep(1)
            i += 1
