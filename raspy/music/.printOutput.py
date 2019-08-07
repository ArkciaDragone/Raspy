import sys
sys.path.append("..")

from numpy import gcd

import mcpi.minecraft as mmc
import tools
import readMidiFile as rmf

mc = tools.start(0)

mc.postToChat("Test mode, please input a path.")

while True:
    posts = mc.events.pollChatPosts()
    if len(posts) > 0:
        pathWithHyphen = posts[0].message
        path = pathWithHyphen.lstrip("-")
        a = list(rmf.readAndProcessMidi(path))
        b = rmf.getBpmSet(path)
        print("This is the gcd:\n")
        print(gcd.reduce([hit[0] for hit in a]))
        print("\nThis is the hitlist:\n")
        print([hit for hit in a])
        print("\nThis is BPM:\n")
        print(b)
        break