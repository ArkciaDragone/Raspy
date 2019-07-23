import sys
sys.path.append("..")

import mcpi.minecraft as mmc
import tools
from . import readMidiFile as rmf

mc = tools.start(0)

mc.postToChat("Test mode, please input a path.")

while True:
    posts = mc.events.pollChatPosts()
    if len(posts) > 0:
        pathWithHyphen = posts[0].message
        path = pathWithHyphen.lstrip("-")
        print([hit for hit in rmf.readAndProcessMidi(path)])
        break
