# --------------------
# (main) startMidi.py
# v0.3.2 - 2019/8/10
# Double-click this to launch the program!
# --------------------

import sys
sys.path.append("..")

import mcpi.minecraft as mmc
import tools
from setSystem import setRedstoneSystem
from constructSystem import constructRedstoneSystem

mc = tools.start(0)

# --------------------
# main
# --------------------

if __name__ == "__main__":
    
    mc.postToChat("")
    mc.postToChat("Music Lab v0.3.2 initiated!")
    mc.postToChat("")
    mc.postToChat("Please input (in-game) the path of the midi file you want to realize, beginning with an additional hyphen: (i.e. -C:\\Raspy\\test.mid or -/Users/<your-name>/Documents/test.mid)")
    mc.postToChat("")

    while True:
        
        posts = mc.events.pollChatPosts()

        if len(posts) > 0:

            try:
                zeroOrNot = int(posts[0].message)

            except ValueError:
                None

            else:
                if zeroOrNot == 0:
                    mc.events.clearAll()
                    mc.postToChat("")
                    mc.postToChat("Process aborted.")
                    sys.exit(0)

                else:
                    None
            
            pathWithHyphen = posts[0].message
            path = pathWithHyphen.lstrip("-")

            try:
                configurationList = setRedstoneSystem(path, mc)
            
            except FileNotFoundError:
                mc.postToChat("")
                mc.postToChat("Cannot find a file at your path, or your input isn't indicating a path.")
                mc.postToChat("Please input another path, or input 0 to abort the process.")
                mc.postToChat("")
                continue

            except PermissionError:
                mc.postToChat("")
                mc.postToChat("Uh-oh, seems like the program doesn't have the permission to visit that path. Try putting the file in a different folder.")
                mc.postToChat("Please input another path, or input 0 to abort the process.")
                mc.postToChat("")
                continue

            except IndexError:
                mc.postToChat("")
                mc.postToChat("The file you requested isn't midi file, or your midi file cannot be processed at the moment. Sorry!")
                mc.postToChat("Please input another path, or input 0 to abort the process.")
                mc.postToChat("")
                continue

            except ValueError as ve:
                mc.postToChat("")
                if ve.args[0] == "Nothing":
                    mc.postToChat("There's literally nothing in your midi file. Therefore we cannot proceed.")
                    mc.postToChat("Please input another path, or input 0 to abort the process.")
                    mc.postToChat("")
                    continue

            else:
                mc.events.clearAll()
                constructRedstoneSystem(configurationList, mc)
                break