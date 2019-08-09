# --------------------
# (main) startMidi.py
# v0.2.3 - 2019/8/9
# Double-click this to launch the program!
# --------------------

import sys
sys.path.append("..")

import mcpi.minecraft as mmc
import tools
import setSystem as ss
import constructSystem as cs

mc = tools.start(0)

# --------------------
# retry
# --------------------

def retry():
    
    mc.events.clearAll()

    while True:
        
        userChoicePost = mc.events.pollChatPosts()
        
        if len(userChoicePost) > 0:
            userChoice = userChoicePost[0].message
            
            try:
                a = int(userChoice)

            except ValueError:      # userChoice is not an integer
                mc.postToChat("")
                mc.postToChat("Process aborted.")
                sys.exit(0)
                
            else:

                if a == 1:
                    mc.events.clearAll()
                    mc.postToChat("")
                    mc.postToChat("Continuing...")
                    break

                else:
                    mc.events.clearAll()
                    mc.postToChat("")
                    mc.postToChat("Process aborted.")
                    sys.exit(0)

# --------------------
# main
# --------------------

if __name__ == "__main__":
    
    mc.postToChat("")
    mc.postToChat("Music Lab v0.2.3 initiated!")
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
                configurationList = ss.setRedstoneSystem(path, mc, 1)
            
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
                if ve.args[0] == "Too many voices":
                    mc.postToChat("The midi file can be processed, however, you have to manually set the base line to properly activate the redstone system, as the program temporarily doesn't have a feasible algorithm for that.")
                    mc.postToChat("Input 1 to continue, or input anything besides 1 to abort the process.")
                    mc.postToChat("")
                    retry()
                    configurationList = ss.setRedstoneSystem(path, mc, 2)
                    mc.events.clearAll()
                    cs.constructRedstoneSystem(configurationList, mc, 2)
                    break

            else:
                mc.events.clearAll()
                cs.constructRedstoneSystem(configurationList, mc, 1)
                break
