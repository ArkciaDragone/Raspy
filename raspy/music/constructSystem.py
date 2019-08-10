# --------------------
# constructSystem.py
# Attach the configured redstone system in game
# --------------------

import sys
sys.path.append("..")

import mcpi.block as block
import mcpi.connection

# --------------------
# xBoundary
# --------------------

def xBoundary(voiceMax):
    """Define the horizontal boundary of glass cover"""
    return [- voiceMax - 1, voiceMax + 1]

# --------------------
# baseLineLength
# --------------------

def baseLineLength(baseLineRow):
    return 3 + 2 * (baseLineRow - 1)

# --------------------
# zBoundary
# --------------------

def zBoundary(hitNum, minDelay, repeaterNum, processedList, baseLineLength):
    """Define the vertical boundary of glass cover"""
    if processedList[-1][0] == 0:      # hitNum == 1
        num = 1
    else:
        num = int(processedList[-1][0] / minDelay) + 1
    
    length = baseLineLength + 1 + (num - 1) * (2 + repeaterNum) + 4

    if hitNum == 1:
        return [-1, -1 + length - 1 + 3]
    else:
        return [-1, -1 + length - 1]

# --------------------
# placeStone
# --------------------

def placeStone(loc, xBoundary, zBoundary, gameName):
    # place stone in the bottom
    gameName.setBlocks(
        loc.x + xBoundary[0], loc.y - 1, loc.z + zBoundary[0],
        loc.x + xBoundary[1], loc.y - 1, loc.z + zBoundary[1],
        block.STONE.id)

# --------------------
# placeGlass
# --------------------

def placeGlass(loc, xBoundary, zBoundary, gameName):
    # place in the front and in the back
    gameName.setBlocks(
        loc.x + xBoundary[0], loc.y, loc.z + zBoundary[0],
        loc.x + xBoundary[1], loc.y + 6, loc.z + zBoundary[0],
        block.GLASS.id)
    gameName.setBlocks(
        loc.x + xBoundary[0], loc.y, loc.z + zBoundary[1],
        loc.x + xBoundary[1], loc.y + 6, loc.z + zBoundary[1],
        block.GLASS.id)
    # place in the left and in the right
    gameName.setBlocks(
        loc.x + xBoundary[0], loc.y, loc.z + zBoundary[0],
        loc.x + xBoundary[0], loc.y + 6, loc.z + zBoundary[1],
        block.GLASS.id)
    gameName.setBlocks(
        loc.x + xBoundary[1], loc.y, loc.z + zBoundary[0],
        loc.x + xBoundary[1], loc.y + 6, loc.z + zBoundary[1],
        block.GLASS.id)
    # place the top cover
    gameName.setBlocks(
        loc.x + xBoundary[0], loc.y + 7, loc.z + zBoundary[0],
        loc.x + xBoundary[1], loc.y + 7, loc.z + zBoundary[1],
        block.GLASS.id)

# --------------------
# placeAir
# --------------------

def placeAir(loc, xBoundary, zBoundary, gameName):
    # place inside glass cover
        gameName.setBlocks(
        loc.x + xBoundary[0] + 1, loc.y + 0, loc.z + zBoundary[0] + 1,
        loc.x + xBoundary[1] - 1, loc.y + 6, loc.z + zBoundary[1] - 1,
        block.AIR.id)

# --------------------
# placeDoorAndTerracotta
# --------------------

def placeDoorAndTerracotta(loc, zBoundary, gameName):

    # place front door and terracotta around
    gameName.setBlock(loc.x, loc.y, loc.z + zBoundary[0], block.DOOR_BIRCH.id, 0)      # lower door
    gameName.setBlock(loc.x, loc.y + 1, loc.z + zBoundary[0], block.DOOR_BIRCH.id, 8)      # upper door
    gameName.setBlock(loc.x, loc.y + 2, loc.z + zBoundary[0], block.LIGHT_BLUE_GLAZED_TERRACOTTA.id, 0)
    gameName.setBlocks(
        loc.x - 1, loc.y, loc.z + zBoundary[0],
        loc.x - 1, loc.y + 2, loc.z + zBoundary[0],
        block.LIGHT_BLUE_GLAZED_TERRACOTTA.id)
    gameName.setBlocks(
        loc.x + 1, loc.y, loc.z + zBoundary[0],
        loc.x + 1, loc.y + 2, loc.z + zBoundary[0],
        block.LIGHT_BLUE_GLAZED_TERRACOTTA.id)

    # place back door and terracotta around
    gameName.setBlock(loc.x, loc.y, loc.z + zBoundary[1], block.DOOR_BIRCH.id, 0)      # lower block
    gameName.setBlock(loc.x, loc.y + 1, loc.z + zBoundary[1], block.DOOR_BIRCH.id, 9)      # upper block
    gameName.setBlock(loc.x, loc.y + 2, loc.z + zBoundary[1], block.LIGHT_BLUE_GLAZED_TERRACOTTA.id, 0)
    gameName.setBlocks(
        loc.x - 1, loc.y, loc.z + zBoundary[1],
        loc.x - 1, loc.y + 2, loc.z + zBoundary[1],
        block.LIGHT_BLUE_GLAZED_TERRACOTTA.id)
    gameName.setBlocks(
        loc.x + 1, loc.y, loc.z + zBoundary[1],
        loc.x + 1, loc.y + 2, loc.z + zBoundary[1],
        block.LIGHT_BLUE_GLAZED_TERRACOTTA.id)

# --------------------
# placeNoteBlock
# --------------------

def placeNoteBlock(loc, configWay, hitNum, voiceMax, minDelay, repeaterNum, processedList, theBaseLineLength, gameName):

    if configWay[0] == 1:
        for j in range(0, hitNum):
            for k in range(0, len(processedList[j][1])):      # the number of notes in noteProcessedList[j]
                gameName.setNoteBlock(loc.x + (- voiceMax + 1 + 2 * k), loc.y, loc.z + theBaseLineLength + 1 + processedList[j][0] / minDelay * (2 + repeaterNum), processedList[j][1][k])

        if configWay[1] == 1:      # harp/piano timbre
            for j in range(0, hitNum):
                for k in range(0, len(processedList[j][1])):
                    gameName.setBlock(loc.x + (- voiceMax + 1 + 2 * k), loc.y - 1, loc.z + theBaseLineLength + 1 + processedList[j][0] / minDelay * (2 + repeaterNum), block.GRASS.id)
        elif configWay[1] == 2:      # double bass timbre
            for j in range(0, hitNum):
                for k in range(0, len(processedList[j][1])):
                    gameName.setBlock(loc.x + (- voiceMax + 1 + 2 * k), loc.y - 1, loc.z + theBaseLineLength + 1 + processedList[j][0] / minDelay * (2 + repeaterNum), block.WOOD.id)
        elif configWay[1] == 3:      # glockenspiel timbre
            for j in range(0, hitNum):
                for k in range(0, len(processedList[j][1])):
                    gameName.setBlock(loc.x + (- voiceMax + 1 + 2 * k), loc.y - 1, loc.z + theBaseLineLength + 1 + processedList[j][0] / minDelay * (2 + repeaterNum), block.GOLD_BLOCK.id)
        elif configWay[1] == 4:      # flute timbre
            for j in range(0, hitNum):
                for k in range(0, len(processedList[j][1])):
                    gameName.setBlock(loc.x + (- voiceMax + 1 + 2 * k), loc.y - 1, loc.z + theBaseLineLength + 1 + processedList[j][0] / minDelay * (2 + repeaterNum), block.CLAY.id)
        elif configWay[1] == 5:      # chime timbre
            for j in range(0, hitNum):
                for k in range(0, len(processedList[j][1])):
                    gameName.setBlock(loc.x + (- voiceMax + 1 + 2 * k), loc.y - 1, loc.z + theBaseLineLength + 1 + processedList[j][0] / minDelay * (2 + repeaterNum), block.PACKED_ICE.id)
        elif configWay[1] == 6:      # guitar timbre
            for j in range(0, hitNum):
                for k in range(0, len(processedList[j][1])):
                    gameName.setBlock(loc.x + (- voiceMax + 1 + 2 * k), loc.y - 1, loc.z + theBaseLineLength + 1 + processedList[j][0] / minDelay * (2 + repeaterNum), block.WOOL.id)
        elif configWay[1] == 7:      # xylophone timbre
            for j in range(0, hitNum):
                for k in range(0, len(processedList[j][1])):
                    gameName.setBlock(loc.x + (- voiceMax + 1 + 2 * k), loc.y - 1, loc.z + theBaseLineLength + 1 + processedList[j][0] / minDelay * (2 + repeaterNum), block.BONE_BLOCK.id)

    if configWay[0] == 2:

        for j in range(0, hitNum):
            for k in range(0, len(processedList[j][1])):
                if 0 <= processedList[j][1][k] < 24:      # low range, use double bass timbre
                    gameName.setNoteBlock(loc.x + (- voiceMax + 1 + 2 * k), loc.y, loc.z + theBaseLineLength + 1 + processedList[j][0] / minDelay * (2 + repeaterNum), processedList[j][1][k])
                    gameName.setBlock(loc.x + (- voiceMax + 1 + 2 * k), loc.y - 1, loc.z + theBaseLineLength + 1 + processedList[j][0] / minDelay * (2 + repeaterNum), block.WOOD.id)
                if 24 <= processedList[j][1][k] < 48:      # medium range, use harp/piano timbre
                    gameName.setNoteBlock(loc.x + (- voiceMax + 1 + 2 * k), loc.y, loc.z + theBaseLineLength + 1 + processedList[j][0] / minDelay * (2 + repeaterNum), processedList[j][1][k] - 24)
                    gameName.setBlock(loc.x + (- voiceMax + 1 + 2 * k), loc.y - 1, loc.z + theBaseLineLength + 1 + processedList[j][0] / minDelay * (2 + repeaterNum), block.GRASS.id)
                if 48 <= processedList[j][1][k] <= 72:      # high range, use glockenspiel timbre
                    gameName.setNoteBlock(loc.x + (- voiceMax + 1 + 2 * k), loc.y, loc.z + theBaseLineLength + 1 + processedList[j][0] / minDelay * (2 + repeaterNum), processedList[j][1][k] - 48)
                    gameName.setBlock(loc.x + (- voiceMax + 1 + 2 * k), loc.y - 1, loc.z + theBaseLineLength + 1 + processedList[j][0] / minDelay * (2 + repeaterNum), block.GOLD_BLOCK.id)

# --------------------
# placeRepeater
# --------------------

def placeRepeater(loc, hitNum, voiceMax, minDelay, repeaterNum, processedList, theBaseLineLength, gameName):
    for i in range(- voiceMax + 1, voiceMax, 2):
        for j in range(0, int(processedList[-1][0] / minDelay)):
            if int(minDelay % 4) == 0:
                gameName.setBlock(loc.x + i, loc.y, loc.z + theBaseLineLength + 3 + repeaterNum - 1 + j * (2 + repeaterNum), block.UNPOWERED_REPEATER.id, 2 + 12)      # delay = 4
            else:
                gameName.setBlock(loc.x + i, loc.y, loc.z + theBaseLineLength + 3 + repeaterNum - 1 + j * (2 + repeaterNum), block.UNPOWERED_REPEATER.id, 2 + 4 * (int(minDelay % 4) - 1))      # delay != 4
            for k in range(0, repeaterNum - 1):      # range(0, 0) = []
                gameName.setBlock(loc.x + i, loc.y, loc.z + theBaseLineLength + 3 + k + j * (2 + repeaterNum), block.UNPOWERED_REPEATER.id, 2 + 12)      # delay = 4
                # 2 means facing south (z-axis positive)

# --------------------
# placeRedstoneWire
# --------------------

def placeRedstoneWire(loc, hitNum, voiceMax, minDelay, repeaterNum, processedList, theBaseLineLength, gameName):
    
    for i in range(- voiceMax + 1, voiceMax, 2):
        for j in range(0, int(processedList[-1][0] / minDelay)):
            gameName.setBlock(loc.x + i, loc.y, loc.z + theBaseLineLength + 2 + j * (2 + repeaterNum), block.REDSTONE_WIRE.id)
    
    # also place a redstone wire if "3 + processedList[j][0] / minDelay * (2 + repeaterNum)" has no note block because of note lacking on this specific voice
    for k in range(0, hitNum):
        for l in range(len(processedList[k][1]), voiceMax):
            gameName.setBlock(loc.x + (- voiceMax + 1 + 2 * l), loc.y, loc.z + theBaseLineLength + 1 + processedList[k][0] / minDelay * (2 + repeaterNum), block.REDSTONE_WIRE.id)

    for m in range(0, int(processedList[-1][0] / minDelay)):
        if m * minDelay not in [processedListMember[0] for processedListMember in processedList]:
            for n in range(- voiceMax + 1, voiceMax, 2):
                gameName.setBlock(loc.x + n, loc.y, loc.z + theBaseLineLength + 1 + m * (2 + repeaterNum), block.REDSTONE_WIRE.id)

# --------------------
# placeTorch
# --------------------

def placeTorch(loc, zBoundary, hitNum, voiceMax, repeaterNum, theBaseLineLength, gameName):
    if hitNum == 1:
        for i in range(- voiceMax, voiceMax + 1, 2):
            gameName.setBlock(loc.x + i, loc.y, loc.z + theBaseLineLength, block.TORCH.id)
    else:
        # place torch every three rows of repeaters
        for i in range(- voiceMax, voiceMax + 1, 2):
            m = -3
            while True:
                m += 3
                if theBaseLineLength + 3 + m * (2 + repeaterNum) >= zBoundary[1]:
                    break
                gameName.setBlock(loc.x + i, loc.y, loc.z + theBaseLineLength + 3 + m * (2 + repeaterNum), block.TORCH.id)

# --------------------
# placeBaseLine
# --------------------

def placeBaseLine(loc, voiceMax, theBaseLineLength, gameName):

    xList = [i for i in range(- voiceMax + 1, voiceMax, 2)]
    xList2 = []
    a = theBaseLineLength      # loc.z + theBaseLineLength is exactly the z coordinate for the frontmost row of repeaters

    while True:
        b, c = 0, -1
        while True:
            while True:
                c += 1
                if c == len(xList) - 1:
                    break
                if xList[c + 1] - xList[b] > 29:      # reachs maximum length
                    break
                else:
                    continue
            for x in range(b, c + 1):
                gameName.setBlock(loc.x + xList[x], loc.y, loc.z + a, block.UNPOWERED_REPEATER.id, 2)
            for x in range(xList[b], xList[c] + 1):
                gameName.setBlock(loc.x + x, loc.y, loc.z + a - 1, block.REDSTONE_WIRE.id)
            middleX = int((xList[b] + xList[c]) / 2)
            xList2.append(middleX)
            if c == len(xList) - 1:
                break
            else:
                b = c + 1
                c = b - 1
        a -= 2
        xList = xList2
        xList2 = []
        if len(xList) == 1:
            gameName.setBlock(loc.x + xList[0], loc.y, loc.z + a, block.WOODEN_BUTTON.id, 5)
            break
        else:
            continue
            
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
    gameName.postToChat("This takes less than a minute for a medium-sized midi file.")
    gameName.postToChat("")

    # cL[0] is configWay, [1] is preProcess2Result, [2] is processedList
    # cL[1][0] is hitNum, [1][1] is voiceMax, [1][2] is minDelay, [1][3] is repeaterNum, [1][6] is baseLineRow
    
    theXBoundary = xBoundary(cL[1][1])
    theBaseLineLength = baseLineLength(cL[1][6])
    theZBoundary = zBoundary(cL[1][0], cL[1][2], cL[1][3], cL[2], theBaseLineLength)

    placeStone(loc, theXBoundary, theZBoundary, gameName)
    placeGlass(loc, theXBoundary, theZBoundary, gameName)
    placeAir(loc, theXBoundary, theZBoundary, gameName)
    placeDoorAndTerracotta(loc, theZBoundary, gameName)

    placeNoteBlock(loc, cL[0], cL[1][0], cL[1][1], cL[1][2], cL[1][3], cL[2], theBaseLineLength, gameName)
    placeRepeater(loc, cL[1][0], cL[1][1], cL[1][2], cL[1][3], cL[2], theBaseLineLength, gameName)
    placeRedstoneWire(loc, cL[1][0], cL[1][1], cL[1][2], cL[1][3], cL[2], theBaseLineLength, gameName)

    placeBaseLine(loc, cL[1][1], theBaseLineLength, gameName)
    placeTorch(loc, theZBoundary, cL[1][0], cL[1][1], cL[1][3], theBaseLineLength, gameName)
    
    gameName.postToChat("Midi file successfully processed and attached in-game!")
    gameName.postToChat("If you wish to process another, reload the program.")