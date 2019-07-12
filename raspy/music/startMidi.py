# --------------------
# startMidi.py
# Process midi file and realize in Minecraft
# --------------------

import sys
sys.path.append("..")

import mcpi.minecraft as mmc
import tools
import music.readMidiFile as rmf

mc = tools.start(0)

mc.postToChat("Please input (in-game) the path of the midi file you want to realize, beginning with an additional hyphen: (i.e. -C:\\Raspy\\test.mid or -/Users/<your-name>/Documents/test.mid)")

# Following codes haven't been tested in-game

while True:

    posts = mc.events.pollChatPosts()

    if len(posts) > 0:
        pathWithHyphen = posts[0].message
        path = pathWithHyphen.lstrip("-")

        try:
            rmf.readandProcessMidi(path) # need to be revised

        except BaseException:
            mc.postToChat("Wrong path, or the file you requested cannot be processed.")
            mc.postToChat("Input 1 to try again, or input anything besides 1 to abort the process.")

            mc.events.clearAll()

            while True:
                userChoicePost = mc.events.pollChatPosts()
                if len(userChoicePost) > 0:
                    userChoice = posts[0].message
                    if int(userChoice) == 1:
                        mc.postToChat("Process restarted.")
                        mc.postToChat("Please input (in-game) the path of the midi file you want to realize, beginning with an additional hyphen: (i.e. -C:\\Raspy\\test.mid or -/Users/<your-name>/Documents/test.mid)")
                        mc.events.clearAll()
                        break
                    else:
                        sys.exit(o)

            continue

        else:
            mc.postToChat("Midi file successfully processed!")
            break

mc.events.clearAll()

# import music.defPlaceNoteBlock as dpnb
# dpnb.testPlaceNoteBlock()