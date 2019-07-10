"""

Known errors:
1. pollChatPosts() doesn't seems to work normally (polling one post at a time), it seems to be polling continuously and endlessly.
2. No matter what block data I put in the function mc.setBlock(x,y,z,id,[data]), the execution always treats it as 0, which makes the lever down-sided.

"""

import sys
sys.path.append("..")

import mcpi.minecraft as mmc
import mcpi.block as block
import tools
from random import choice

mc = tools.start(0)

mc.postToChat("Please input (in the command line) the name of the player beside whom the note block system is placed:")
# name = str(mc.events.pollChatPosts())
name = input()

while True:
    try:
        id = mc.getPlayerEntityId(name)
    except BaseException:
        mc.postToChat("Wrong name, please input again:")
        # name = mc.events.pollChatPosts()
        name = input()
        continue
    else:
        break

loc = mc.entity.getPos(id);
# new_loc = [loc.x, loc.y, loc.z+1]

mc.setNoteBlock(loc.x, loc.y, loc.z+1, 1)      # G pitch
mc.setBlock(loc.x+1, loc.y, loc.z+1, block.REDSTONE_WIRE)

buttonNameList = [block.STONE_BUTTON, block.WOODEN_BUTTON] # 1.12.2 doesn't have buttons of other tree variants
randomButton = choice(buttonNameList)
mc.setBlock(loc.x+2, loc.y, loc.z+1, randomButton, 5)

mc.postToChat("Congratulations! A note block with G pitch has been placed beside " + str(name) + ", together with a redstone circuit. Toggle the button to activate the note block!")