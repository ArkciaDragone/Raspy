# --------------------
# askConfig.py
# Let the user define their own way of configuration
# --------------------

import sys
sys.path.append("..")

from readMidiFile import getFirstBpm, readAndProcessMidi

# --------------------
# askConfigWay
# --------------------

def askConfigWay(gameName):
    gameName.postToChat("")
    gameName.postToChat("There are currently two ways of configuring the redstone system.")
    gameName.postToChat("Way 1 is to make all note blocks mono-timbre, which also means the pitch range will be reduced. You can choose the timbre later.")
    gameName.postToChat("Way 2 is to remain all notes in the same pitches. The program will choose double bass as the timbre of low range, harp as of medium range, glockenspiel as of high range.")
    gameName.postToChat("Input 1 or 2 to decide which way to configure.")
    gameName.postToChat("")

    while True:
        decideConfigPost = gameName.events.pollChatPosts()
        if len(decideConfigPost) > 0:
            decideConfig = decideConfigPost[0].message
            try:
                a = int(decideConfig)
            except ValueError:      # decideConfig is not an integer
                gameName.events.clearAll()
                gameName.postToChat("")
                gameName.postToChat("You didn't input an integer, please input again.")
                gameName.postToChat("")
                continue
            else:
                if a == 1 or a == 2:
                    gameName.events.clearAll()
                    b = askTimbre(a, gameName)
                    return [a, b]
                else:
                    gameName.events.clearAll()
                    gameName.postToChat("")
                    gameName.postToChat("Your input doesn't fall between 1 and 2, please input again.")
                    gameName.postToChat("")
                    continue

# --------------------
# askTimbre
# --------------------

def askTimbre(a, gameName):

    if a == 1:

        gameName.postToChat("")
        gameName.postToChat("There are currently seven timbres:")
        gameName.postToChat("")
        gameName.postToChat("Harp/piano (1), double bass (2), glockenspiel (3), flute (4), chime (5), guitar (6), xylophone (7).")
        gameName.postToChat("")
        gameName.postToChat("Input an integer between 1 and 7 to choose your timbre.")
        gameName.postToChat("")

        while True:
            decideTimbrePost = gameName.events.pollChatPosts()
            if len(decideTimbrePost) > 0:
                decideTimbre = decideTimbrePost[0].message
                try:
                    b = int(decideTimbre)
                except ValueError:      # decideTimbre is not an integer
                    gameName.events.clearAll()
                    gameName.postToChat("")
                    gameName.postToChat("You didn't input an integer, please input again.")
                    gameName.postToChat("")
                    continue
                else:
                    if 1 <= b <= 7:
                        gameName.events.clearAll()
                        return b
                    else:
                        gameName.events.clearAll()
                        gameName.postToChat("")
                        gameName.postToChat("Your input doesn't fall between 1 and 7, please input again.")
                        gameName.postToChat("")
                        continue

    if a == 2:
        return 0

# --------------------
# askTempo
# --------------------

def askTempoAndProcess(path, gameName):

    tempo = int(getFirstBpm(path))

    # if the path is correct, then post the following
    gameName.postToChat("")
    gameName.postToChat("Configuring redstone system...")
    gameName.postToChat("")

    if tempo < 37.5:
        gameName.postToChat("The minimum tempo of a redstone music system is 37.5 bpm, but your file has a tempo lower than that.")
    elif 37.5 < tempo < 75:
        gameName.postToChat("The tempo of a redstone music system can either be 37.5 bpm or 75 bpm, but your file has a tempo in between, which is %s."%tempo)
    elif 75 < tempo < 150:
        gameName.postToChat("The tempo of a redstone music system can either be 75 bpm or 150 bpm, but your file has a tempo in between, which is %s."%tempo)
    elif tempo > 150:
        gameName.postToChat("The maximum tempo of a redstone music system is 150 bpm, but your file has a tempo higher than that.")
    elif tempo == 37.5 or tempo == 75 or tempo == 150:
        gameName.postToChat("Congratulations! You can construct the redstone music system in exactly %s bpm."%tempo)
    
    gameName.postToChat("")
    gameName.postToChat("Due to the in-game mechanics, the tempo of a redstone music system can only be one of 37.5 bpm, 75 bpm, or 150 bpm. Choose one and enter it, so that the system can be configured in that way.")
    gameName.postToChat("")

    while True:
            decideTempoPost = gameName.events.pollChatPosts()
            if len(decideTempoPost) > 0:
                decideTempo = decideTempoPost[0].message
                try:
                    a = float(decideTempo)
                except ValueError:      # decideTempo is not a float
                    gameName.events.clearAll()
                    gameName.postToChat("")
                    gameName.postToChat("You didn't input an integer, please input again.")
                    gameName.postToChat("")
                    continue
                else:
                    if a == 37.5:
                        hitList = list(readAndProcessMidi(path, 1 / 16))
                        return hitList
                    if a == 75:
                        hitList = list(readAndProcessMidi(path, 1 / 8))
                        return hitList
                    if a == 150:
                        hitList = list(readAndProcessMidi(path, 1 / 4))
                        return hitList
                    else:
                        gameName.events.clearAll()
                        gameName.postToChat("")
                        gameName.postToChat("Your input doesn't fall among 37.5, 75 or 150, please input again.")
                        gameName.postToChat("")
                        continue