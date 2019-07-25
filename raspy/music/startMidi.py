# --------------------
# (main) startMidi.py
# v0.1.2 - 2019/7/26
# Double-click this to launch the program!
# --------------------

import sys
sys.path.append("..")

import mcpi.minecraft as mmc
import tools
import setSystem as ss
import constructSystem as cs

mc = tools.start(0)

mc.postToChat("Please input (in-game) the path of the midi file you want to realize, \
beginning with an additional hyphen: (i.e. -C:\\Raspy\\test.mid or -/Users/<your-name>\
/Documents/test.mid)")

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
                mc.postToChat("Process aborted.")
                sys.exit(0)

            else:
                if int(userChoice) == 1:
                    mc.postToChat("Process restarted.")
                    mc.postToChat("Please input (in-game) the path of the midi file you want to realize, \
                    beginning with an additional hyphen: (i.e. -C:\\Raspy\\test.mid or -/Users/<your-name>\
                    /Documents/test.mid)")
                    mc.events.clearAll()
                    break
                else:
                    mc.postToChat("Process aborted.")
                    sys.exit(0)

# --------------------
# main
# --------------------

if __name__ == "__main__":

    while True:
        
        posts = mc.events.pollChatPosts()

        if len(posts) > 0:
            pathWithHyphen = posts[0].message
            path = pathWithHyphen.lstrip("-")

            try:
                configurationList = ss.setRedstoneSystem(path, mc)
            
            except FileNotFoundError:
                mc.postToChat("Cannot find a file at your path, maybe used a false grammar?")
                mc.postToChat("Input 1 to try again, or input anything besides 1 to abort the process.")
                retry()
                continue

            except PermissionError:
                mc.postToChat("Uh-oh, seems like the program doesn't have the permission to visit that path. Try putting the file in a different folder.")
                mc.postToChat("Input 1 to try again, or input anything besides 1 to abort the process.")
                retry()
                continue

            except IndexError:
                mc.postToChat("The file you requested isn't Midi file, or your Midi file cannot be processed at the moment. Sorry!")
                mc.postToChat("Input 1 to try again, or input anything besides 1 to abort the process.")
                retry()
                continue

            else:
                break

    mc.events.clearAll()

    cs.constructRedstoneSystem(configurationList, mc)