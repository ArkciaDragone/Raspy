# --------------------
# setSystem.py
# Use the results from readMidiFile to configure the redstone system
# 
# Important Note:
# Package "statistics" should be pre-installed to run this application.
# Use "pip install <package-name>" in cmd to install.
# --------------------

import sys
sys.path.append("..")

from math import floor, ceil
from statistics import mean
import readMidiFile as rmf

# --------------------
# gcd
# --------------------

def gcd(numList):

    if len(numList) == 1:      # there's only one chord in the midi file
        return 1

    else:
    
        while len(numList) > 1:
            a = numList[len(numList) - 2]
            b = numList[len(numList) - 1]
            numList = numList[:len(numList) - 2]
            
            while a:
                a, b = b % a, a
                
            numList.append(b)
        
            return b

# --------------------
# averagePitch
# --------------------

def averagePitch(voiceMax, hitList):
    
    averagePitchList = []
    noteNumList = []      # counts number of notes in each voice
    for i in range(0, voiceMax):
        averagePitchList.append(0)      # reserve voiceMax spots
        noteNumList.append(0)      # reserve voiceMax spots

    hitNum = len(hitList)
    for j in range(0, hitNum):
        for k in range(0, len(hitList[j][1])):
            averagePitchList[k] += hitList[j][1][k]
            noteNumList[k] += 1

    for l in range(0, voiceMax):
        averagePitchList[l] /= noteNumList[l]

    return averagePitchList

# --------------------
# preProcess
# --------------------

def preProcess(hitList):

    hitNum = len(hitList)
    if hitNum == 0:
        raise ValueError("Nothing")

    voiceMax = max([len(hit[1]) for hit in hitList])
    if voiceMax > 15:
        raise ValueError("Too many voices")      # the initial redstone signal cannot reach columns which are too far

    minDelay = gcd([hit[0] for hit in hitList])

    repeaterNum = ceil(minDelay / 4)

    averagePitchList = averagePitch(voiceMax, hitList)

    minus12NumList = [floor((averagePitch - 66) / 12) for averagePitch in averagePitchList]      # 66 is the medium pitch (F#4) for harp sound
    for i in range(0, len(minus12NumList)):
        if minus12NumList[i] < 0:
            minus12NumList[i] += 1

    return [hitNum, voiceMax, minDelay, repeaterNum, averagePitchList, minus12NumList]

# --------------------
# columnRelativePlacing
# --------------------

def columnRelativePlacing(voiceMax):
    return [(- voiceMax + 1 + i*2) for i in range(0, voiceMax)]      # odd and even are the same

# --------------------
# processNoteAndDelay
# --------------------

def processNoteAndDelay(minus12NumList, hitList):      # actually create a new list called processedList

    newHitList = []
    
    for a in range(0, len(hitList)):
        newHitList.append(list(hitList[a]))      # turn tuples to lists so that we can modify them

    for i in range(0, len(newHitList)):

        # process notes
        voiceNum = len(newHitList[i][1])
        for j in range(0, voiceNum):
            newHitList[i][1][j] -= 12 * minus12NumList[j]      # using standard note pitch
            newHitList[i][1][j] -= 54      # convert to note block pitch
            while True:
                if (0 <= newHitList[i][1][j] <= 24):
                    break
                elif (newHitList[i][1][j] < 0):
                    newHitList[i][1][j] += 12
                    continue
                elif (newHitList[i][1][j] > 24):
                    newHitList[i][1][j] -= 12
                    continue

        # process delay
        if i == 0:
            continue
        else:
            for j in range(0, i):
                newHitList[i][0] += hitList[j][0]      # sum-up total delay
    
    return newHitList

# --------------------
# setRedstoneSystem
# --------------------

def setRedstoneSystem(path, gameName):      # gameName is "mc" in startMidi

    hitList = list(rmf.readAndProcessMidi(path))      # hitList looks like [(delay, [pitch, pitch]), ...]
    """Read the result of readAndProcessMidi"""

    # if the path is correct, then post the following
    gameName.postToChat("")
    gameName.postToChat("Configuring redstone system...")
    
    preProcessResult = preProcess(hitList)
    """Output to-be-used vital figures and lists"""
    columnRelativePlacingList = columnRelativePlacing(preProcessResult[1])      # using voiceMax
    """Set the relative Z coordinate for each column"""
    processedList = processNoteAndDelay(preProcessResult[5], hitList)      # using minus12NumList
    """Let the notes fit in note block's playing range, and sum-up the total previous delay for each hit"""

    print(preProcessResult)
    print("\n")
    print(columnRelativePlacingList)
    print("\n")
    print(processedList)

    gameName.postToChat("")
    gameName.postToChat("Configuration completed!")
    
    return [preProcessResult, columnRelativePlacingList, processedList]