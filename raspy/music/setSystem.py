# --------------------
# setSystem.py
# Use the results from readMidiFile to configure the redstone system
# 
# Important Note:
# Packages "statistics" and "numpy" should be pre-installed to run this application.
# Use "pip install <package-name>" in cmd to install.
# --------------------

import sys
sys.path.append("..")

from math import floor, ceil
from statistics import mean
from numpy import gcd
from askConfig import askTempoAndProcess, askConfigWay
from readMidiFile import readAndProcessMidi

# --------------------
# setMiddlePitch
# --------------------

def setMiddlePitch(configWay):
    if configWay[0] == 1:
        if configWay[1] == 1:
            return [1, 66]      # 66 = F#4
        elif configWay[1] == 2:
            return [1, 42]      # 42 = F#2
        elif configWay[1] == 3 or configWay[1] == 5 or configWay[1] == 7:
            return [1, 90]      # 90 = F#6
        elif configWay[1] == 4:
            return [1, 78]      # 78 = F#5
        elif configWay[1] == 6:
            return [1, 54]      # 54 = F#3
    elif configWay[0] == 2:
        return [2, 66]

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
# preProcess1
# --------------------

def preProcess1(hitList, checkForError: bool):
    """The part where all errors are raised, if any"""

    hitNum = len(hitList)
    if hitNum == 0:
        raise ValueError("Nothing")

    voiceMax = max([len(hit[1]) for hit in hitList])
    if voiceMax > 28:
        raise ValueError("Too many voices")

    # preProcess 1 will run twice
    # on the first time it is to check whether the file is able to be processed
    # if not, then the error is raised as above
    # but if so, there's no need to complete processing
    if checkForError:
        return

    a, b = 1, 14
    baseLineRow = 1
    while True:
        if a <= voiceMax <= b:
            break
        else:
            a = b + 1
            b *= 2
            baseLineRow += 1
    
    result = {
        "hitNum": hitNum,
        "voiceMax": voiceMax,
        "baseLineRow": baseLineRow
    }

    return result

# --------------------
# preProcess2
# --------------------

def preProcess2(hitList, middlePitch, pp1Result: dict):
    """The rest of processing"""

    hitNum = pp1Result.get("hitNum")
    voiceMax = pp1Result.get("voiceMax")
    baseLineRow = pp1Result.get("baseLineRow")

    if hitNum == 1:
        minDelay = 1      # otherwise minDelay will calculate as 0, thus causing NaN in constructSystem
    else:
        minDelay = gcd.reduce([hit[0] for hit in hitList])

    repeaterNum = ceil(minDelay / 4)
    
    if middlePitch[0] == 1:
        averagePitchList = averagePitch(voiceMax, hitList)
        minus12NumList = [floor((averagePitch - middlePitch[1]) / 12) for averagePitch in averagePitchList]      # 66 is the medium pitch (F#4) for harp sound
        for i in range(0, len(minus12NumList)):
            if minus12NumList[i] < 0:
                minus12NumList[i] += 1

    elif middlePitch[0] == 2:
        averagePitchList = 0
        minus12NumList = 0
    
    result = {
        "hitNum": hitNum,
        "voiceMax": voiceMax,
        "minDelay": minDelay,
        "repeaterNum": repeaterNum,
        "averagePitchList": averagePitchList,
        "minus12NumList": minus12NumList,
        "baseLineRow": baseLineRow
    }

    return result

# --------------------
# processNoteAndDelay
# --------------------

def processNoteAndDelay(minus12NumList, hitList, middlePitch):      # actually create a new list called processedList

    newHitList = []
    
    for a in range(0, len(hitList)):
        newHitList.append(list(hitList[a]))      # turn tuples to lists so that we can modify them

    for i in range(0, len(newHitList)):

        # process notes
        if middlePitch[0] == 1:
            voiceNum = len(newHitList[i][1])
            for j in range(0, voiceNum):
                newHitList[i][1][j] -= 12 * minus12NumList[j]      # using standard note pitch
                newHitList[i][1][j] -= (middlePitch[1] - 12)      # convert to note block pitch
                while True:
                    if (0 <= newHitList[i][1][j] <= 24):
                        break
                    elif (newHitList[i][1][j] < 0):
                        newHitList[i][1][j] += 12
                        continue
                    elif (newHitList[i][1][j] > 24):
                        newHitList[i][1][j] -= 12
                        continue
        if middlePitch[0] == 2:
            voiceNum = len(newHitList[i][1])
            for j in range(0, voiceNum):
                newHitList[i][1][j] -= 30      # let F#1 be 0
                while True:
                    if (0 <= newHitList[i][1][j] <= 72):      # 0-72 = F#1-F#7
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
    
    gameName.postToChat("")
    gameName.postToChat("Checking if the file can be handled by the program...")
    # raise ValueError (if any) before asking tempo
    hitList = list(readAndProcessMidi(path))
    preProcess1(hitList, True)

    hitList = list(askTempoAndProcess(path, gameName))      # hitList looks like [(delay, [pitch, pitch]), ...]
    pp1Result = preProcess1(hitList, False)

    # if no errors are raised, ask the user's custom choice(s)
    configWay = askConfigWay(gameName)
    middlePitch = setMiddlePitch(configWay)
    
    pp2Result = preProcess2(hitList, middlePitch, pp1Result)
    """Output to-be-used vital figures and lists"""
    processedList = processNoteAndDelay(pp2Result.get("minus12NumList"), hitList, middlePitch)      # using minus12NumList
    """Let the notes fit in note block's playing range, and sum-up the total previous delay for each hit"""

    print(pp2Result)
    print("\n")
    print(processedList)

    gameName.postToChat("")
    gameName.postToChat("Configuration completed!")
    
    configResult = {
        "configWay": configWay,
        "processedList": processedList,
        "hitNum": pp2Result.get("hitNum"),
        "voiceMax": pp2Result.get("voiceMax"),
        "minDelay": pp2Result.get("minDelay"),
        "repeaterNum": pp2Result.get("repeaterNum"),
        "averagePitchList": pp2Result.get("averagePitchList"),
        "minus12NumList": pp2Result.get("minus12NumList"),
        "baseLineRow": pp2Result.get("baseLineRow")
    }

    return configResult
