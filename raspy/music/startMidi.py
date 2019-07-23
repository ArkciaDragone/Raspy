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

# --------------------
# retry
# --------------------

def retry():
    mc.events.clearAll()

    while True:
        
        userChoicePost = mc.events.pollChatPosts()
        
        if len(userChoicePost) > 0:
            userChoice = userChoicePost[0].message
            
            if int(userChoice) == 1:
                mc.postToChat("Process restarted.")
                mc.postToChat("Please input (in-game) the path of the midi file you want to realize, beginning with an additional hyphen: (i.e. -C:\\Raspy\\test.mid or -/Users/<your-name>/Documents/test.mid)")
                mc.events.clearAll()
                break
            
            else:
                mc.postToChat("Process aborted.")
                sys.exit(0)

# --------------------
# main
# --------------------

while True:

    posts = mc.events.pollChatPosts()

    if len(posts) > 0:
        pathWithHyphen = posts[0].message
        path = pathWithHyphen.lstrip("-")

        try:
            rmf.readandProcessMidi(path)
            
        except FileNotFoundError:
            mc.postToChat("Cannot find a file at your path, maybe used a false grammar?")
            mc.postToChat("Input 1 to try again, or input anything besides 1 to abort the process.")
            retry()
            continue

        except IndexError:
            mc.postToChat("The file you requested isn't Midi file.")
            mc.postToChat("Input 1 to try again, or input anything besides 1 to abort the process.")
            retry()
            continue

        else:
            mc.postToChat("Midi file successfully processed!")
            break

mc.events.clearAll()

# import music.defPlaceNoteBlock as dpnb
# dpnb.testPlaceNoteBlock()
