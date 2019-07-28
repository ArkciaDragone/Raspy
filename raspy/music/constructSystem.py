# --------------------
# constructSystem.py
# Attach the configured redstone system in game
# --------------------

import sys
sys.path.append("..")

import mcpi.block as block
import mcpi.connection
import setSystem as ss

# cRPL: columnRelativePlacingList
# rN: repeaterNum

# --------------------
# xBoundary
# --------------------

def xBoundary(cRPL):
    """Define the horizontal boundary of glass cover"""
    return [cRPL[0] - 2, cRPL[-1] + 2]

# --------------------
# zBoundary
# --------------------

def zBoundary(minDelay, rN, processedList):
    """Define the vertical boundary of glass cover"""
    totalNoteBlockNum = int(processedList[-1][0] / minDelay) + 1
    totalLength = 4 + (totalNoteBlockNum - 1) * (2 + rN) + 4
    return [-1, -1 + totalLength - 1]

# --------------------
# placeStone
# --------------------

def placeStone(loc, xBoundary, zBoundary, gameName):
    # place stone in the bottom
    for i in range(xBoundary[0], xBoundary[1] + 1):
        for j in range(zBoundary[0], zBoundary[1] + 1):
            gameName.setBlock(loc.x + i, loc.y - 1, loc.z + j, block.STONE.id)    

# --------------------
# placeGlass
# --------------------

def placeGlass(loc, xBoundary, zBoundary, gameName):
    # place in the front and in the back
    for i in range(xBoundary[0], xBoundary[1] + 1):
        for a in range(0, 7):
            gameName.setBlock(loc.x + i, loc.y + a, loc.z + zBoundary[0], block.GLASS.id)
            gameName.setBlock(loc.x + i, loc.y + a, loc.z + zBoundary[1], block.GLASS.id)
    # place in the left and in the right
    for j in range(zBoundary[0], zBoundary[1] + 1):
        for b in range(0, 7):
            gameName.setBlock(loc.x + xBoundary[0], loc.y + b, loc.z + j, block.GLASS.id)
            gameName.setBlock(loc.x + xBoundary[1], loc.y + b, loc.z + j, block.GLASS.id)
    # place the top cover
    for k in range(xBoundary[0], xBoundary[1] + 1):
        for l in range(zBoundary[0], zBoundary[1] + 1):
            gameName.setBlock(loc.x + k, loc.y + 7, loc.z + l, block.GLASS.id)

# --------------------
# placeAir
# --------------------

def placeAir(loc, xBoundary, zBoundary, gameName):
    # place inside glass cover
    for i in range(xBoundary[0] + 1, xBoundary[1]):
        for j in range(zBoundary[0] + 1, zBoundary[1]):
            for k in range(0, 7):
                gameName.setBlock(loc.x + i, loc.y + k, loc.z + j, block.AIR.id)

# --------------------
# placeDoor
# --------------------

def placeDoor(loc, zBoundary, gameName):
    # place front door
    gameName.setBlock(loc.x, loc.y, loc.z + zBoundary[0], block.DOOR_BIRCH.id, 0)
    gameName.setBlock(loc.x, loc.y + 1, loc.z + zBoundary[0], block.DOOR_BIRCH.id, 8)

    # place back door
    gameName.setBlock(loc.x, loc.y, loc.z + zBoundary[1], block.DOOR_BIRCH.id, 0)
    gameName.setBlock(loc.x, loc.y + 1, loc.z + zBoundary[1], block.DOOR_BIRCH.id, 9)

# --------------------
# placeNoteBlock
# --------------------

def placeNoteBlock(loc, hitNum, minDelay, rN, cRPL, processedList, gameName):
    for j in range(0, hitNum):
        for k in range(0, len(processedList[j][1])):      # the number of notes in noteProcessedList[j]
            gameName.setNoteBlock(loc.x + cRPL[k], loc.y, loc.z + 4 + processedList[j][0] / minDelay * (2 + rN), processedList[j][1][k])
            gameName.setBlock(loc.x + cRPL[k], loc.y - 1, loc.z + 4 + processedList[j][0] / minDelay * (2 + rN), block.GRASS.id)      # the timbre of harp/piano

# --------------------
# placeRepeater
# --------------------

def placeRepeater(loc, hitNum, minDelay, rN, cRPL, processedList, gameName):
    for i in range(0, len(cRPL)):
        for j in range(0, int(processedList[-1][0] / minDelay)):
            if int(minDelay % 4) == 0:
                gameName.setBlock(loc.x + cRPL[i], loc.y, loc.z + 6 + rN - 1 + j * (2 + rN), block.UNPOWERED_REPEATER.id, 2 + 12)      # delay = 4
            else:
                gameName.setBlock(loc.x + cRPL[i], loc.y, loc.z + 6 + rN - 1 + j * (2 + rN), block.UNPOWERED_REPEATER.id, 2 + 4 * (int(minDelay % 4) - 1))      # delay != 4
            for k in range(0, rN - 1):      # range(0, 0) = []
                gameName.setBlock(loc.x + cRPL[i], loc.y, loc.z + 6 + k + j * (2 + rN), block.UNPOWERED_REPEATER.id, 2 + 12)      # delay = 4
                # 2 means facing south (z-axis positive)

# --------------------
# placeRedstoneWire
# --------------------

def placeRedstoneWire(loc, hitNum, voiceMax, minDelay, rN, cRPL, processedList, gameName):
    
    for i in range(0, len(cRPL)):
        for j in range(0, int(processedList[-1][0] / minDelay)):
            gameName.setBlock(loc.x + cRPL[i], loc.y, loc.z + 5 + j * (2 + rN), block.REDSTONE_WIRE.id)
    
    # also place a redstone wire if "3 + processedList[j][0] / minDelay * (2 + rN)" has no note block because of note lacking on this specific voice
    for k in range(0, hitNum):
        if len(processedList[k][1]) != voiceMax:      # means there's note block lacking
            for l in range(len(processedList[k][1]), voiceMax):
                gameName.setBlock(loc.x + cRPL[l], loc.y, loc.z + 4 + processedList[k][0] / minDelay * (2 + rN), block.REDSTONE_WIRE.id)

    for m in range(0, int(processedList[-1][0] / minDelay)):
        if m * minDelay not in [processedListMember[0] for processedListMember in processedList]:
            for n in range(0, len(cRPL)):
                gameName.setBlock(loc.x + cRPL[n], loc.y, loc.z + 4 + m * (2 + rN), block.REDSTONE_WIRE.id)

# --------------------
# placeBaseLine
# --------------------

def placeBaseLine(loc, cRPL, gameName):
    # the base line can only spread redstone signal to 15 columns at most
    for i in range(cRPL[0], cRPL[-1]+1):
        gameName.setBlock(loc.x + i, loc.y, loc.z + 2, block.REDSTONE_WIRE.id)
    for j in range(0, len(cRPL)):
        gameName.setBlock(loc.x + cRPL[j], loc.y, loc.z + 3, block.UNPOWERED_REPEATER.id, 2)
    gameName.setBlock(loc.x, loc.y, loc.z + 1, block.WOODEN_BUTTON.id, 5)

# --------------------
# constructRedstoneSystem
# --------------------

def constructRedstoneSystem(cL, gameName):      # cL means configurationList

    gameName.postToChat("")
    gameName.postToChat("Please input (in-game) the name of the player beside whom the note block system is placed:")
    gameName.postToChat("")
    
    while True:
        posts = gameName.events.pollChatPosts()
        if len(posts) > 0:
            try:
                name = posts[0].message
                id = gameName.getPlayerEntityId(name)
            except mcpi.connection.RequestError:
                gameName.postToChat("")
                gameName.postToChat("Wrong name, please input again:")
                gameName.postToChat("")
                continue
            else:
                break
    
    loc = gameName.entity.getPos(id);

    gameName.postToChat("")
    gameName.postToChat("Attaching...")
    gameName.postToChat("")

    # cL[0] is preProcessResult, [1] is columnRelativePlacingList, [2] is processedList
    # cL[0][0] is hitNum, [0][1] is voiceMax, [0][2] is minDelay, [0][3] is repeaterNum
    theXBoundary = xBoundary(cL[1])
    theZBoundary = zBoundary(cL[0][2], cL[0][3], cL[2])

    placeStone(loc, theXBoundary, theZBoundary, gameName)
    placeGlass(loc, theXBoundary, theZBoundary, gameName)
    placeAir(loc, theXBoundary, theZBoundary, gameName)
    placeDoor(loc, theZBoundary, gameName)

    placeNoteBlock(loc, cL[0][0], cL[0][2], cL[0][3], cL[1], cL[2], gameName)
    placeRepeater(loc, cL[0][0], cL[0][2], cL[0][3], cL[1], cL[2], gameName)
    placeRedstoneWire(loc, cL[0][0], cL[0][1], cL[0][2], cL[0][3], cL[1], cL[2], gameName)
    placeBaseLine(loc, cL[1], gameName)

    gameName.postToChat("Midi file successfully processed and attached in-game!")
    gameName.postToChat("If you wish to process another, reload the program.")
