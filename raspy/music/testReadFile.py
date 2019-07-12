import sys
sys.path.append("..")

import mcpi.minecraft as mmc
import tools

mc = tools.start(0)

mc.postToChat("Please input (in-game) the path of the midi file you want to realize, beginning with an additional hyphen: (i.e. -C:\\Raspy\\test.mid or -/Users/<your-name>/Documents/test.mid)")

while True:
    posts = mc.events.pollChatPosts()
    if len(posts)>0:
        pathWithHyphen = posts[0].message
        path = pathWithHyphen.lstrip("-")

        try:
            mid = open(path, 'r')
            # some analysis of the file (under development)
        except IOError:
            mc.postToChat("Wrong path, please input again:")
            continue
        else:
            mc.postToChat("Midi file successfully processed!")
            break

mc.events.clearAll()

import music.defPlaceNoteBlock as dpnb
dpnb.PlaceNoteBlock()