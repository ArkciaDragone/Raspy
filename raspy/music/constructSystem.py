# --------------------
# constructSystem.py
# Attach the configured redstone system in game
# --------------------

import sys
sys.path.append("..")

import mcpi.block as block
import mcpi.connection
import setSystem as ss

# --------------------
# placeNoteBlock
# --------------------

def placeNoteBlock(loc, hitNum, minDelay, columnRelativePlacingList, processedList, gameName):
    for j in range(0, hitNum):
        for k in range(0, len(processedList[j][1])):      # the number of notes in noteProcessedList[j]
            gameName.setNoteBlock(loc.x + columnRelativePlacingList[k], loc.y, loc.z + 7 + processedList[j][0] / minDelay * 5, processedList[j][1][k])

# --------------------
# placeRepeater
# --------------------

def placeRepeater(loc, hitNum, minDelay, columnRelativePlacingList, processedList, gameName):
    if minDelay <= 4:
        for i in range(0, len(columnRelativePlacingList)):
            for j in range(0, int(processedList[-1][0] / minDelay) + 1):
                gameName.setBlock(loc.x + columnRelativePlacingList[i], loc.y, loc.z + 6 + j * 5, block.UNPOWERED_REPEATER.id, 2 + 4 * (minDelay - 1))
                # 2 means facing south (z-axis positive)
    else:      # attach two repeaters if minDelay > 4
        for i in range(0, len(columnRelativePlacingList)):
            for j in range(0, int(processedList[-1][0] / minDelay) + 1):
                gameName.setBlock(loc.x + columnRelativePlacingList[i], loc.y, loc.z + 5 + j * 5, block.UNPOWERED_REPEATER.id, 2 + 12)
                gameName.setBlock(loc.x + columnRelativePlacingList[i], loc.y, loc.z + 6 + j * 5, block.UNPOWERED_REPEATER.id, 2 + 4 * (minDelay - 5))

# --------------------
# placeRedstoneWire
# --------------------

def placeRedstoneWire(loc, hitNum, voiceMax, minDelay, columnRelativePlacingList, processedList, gameName):
    
    if minDelay <= 4:
        for i in range(0, len(columnRelativePlacingList)):
            for j in range(0, int(processedList[-1][0] / minDelay) + 1):
                gameName.setBlock(loc.x + columnRelativePlacingList[i], loc.y, loc.z + 3 + j * 5, block.REDSTONE_WIRE.id)
                gameName.setBlock(loc.x + columnRelativePlacingList[i], loc.y, loc.z + 4 + j * 5, block.REDSTONE_WIRE.id)
                gameName.setBlock(loc.x + columnRelativePlacingList[i], loc.y, loc.z + 5 + j * 5, block.REDSTONE_WIRE.id)
    else:
        for i in range(0, len(columnRelativePlacingList)):
            for j in range(0, int(processedList[-1][0] / minDelay) + 1):
                gameName.setBlock(loc.x + columnRelativePlacingList[i], loc.y, loc.z + 3 + j * 5, block.REDSTONE_WIRE.id)
                gameName.setBlock(loc.x + columnRelativePlacingList[i], loc.y, loc.z + 4 + j * 5, block.REDSTONE_WIRE.id)
    
    # also place a redstone wire if "7 + processedList[j][0] / minDelay * 5" has no note block because of note lacking on this specific voice
    for k in range(0, hitNum):
        if len(processedList[k][1]) != voiceMax:      # means there's note block lacking
            for l in range(len(processedList[k][1]), voiceMax):
                gameName.setBlock(loc.x + columnRelativePlacingList[l], loc.y, loc.z + 7 + processedList[k][0] / minDelay * 5, block.REDSTONE_WIRE.id)

    for m in range(0, int(processedList[-1][0] / minDelay)):
        if m * minDelay not in [processedListMember[0] for processedListMember in processedList]:
            for n in range(0, len(columnRelativePlacingList)):
                gameName.setBlock(loc.x + columnRelativePlacingList[n], loc.y, loc.z + 7 + m * 5, block.REDSTONE_WIRE.id)

# --------------------
# placeBaseLine
# --------------------

def placeBaseLine(loc, columnRelativePlacingList, gameName):
    # needs revise because if voices are too many the initial redstone signal may not reach certain columns
    # if intended to revise, another configurationList member should be added, because the z coordinate of all other blocks may change
    for i in range(columnRelativePlacingList[0], columnRelativePlacingList[-1]+1):
        gameName.setBlock(loc.x + i, loc.y, loc.z + 2, block.REDSTONE_WIRE.id)
    gameName.setBlock(loc.x, loc.y, loc.z + 1, block.WOODEN_BUTTON.id, 5)

# --------------------
# constructRedstoneSystem
# --------------------

def constructRedstoneSystem(configurationList, gameName):

    gameName.postToChat("Please input (in-game) the name of the player beside whom the note block system is placed:")
    
    while True:
        posts = gameName.events.pollChatPosts()
        if len(posts) > 0:
            try:
                name = posts[0].message
                id = gameName.getPlayerEntityId(name)
            except mcpi.connection.RequestError:
                gameName.postToChat("Wrong name, please input again:")
                continue
            else:
                break
    
    loc = gameName.entity.getPos(id);

    gameName.postToChat("Attaching...")

    # configurationList[0] is preProcessResult, [1] is columnRelativePlacingList, [2] is processedList
    # configurationList[0][0] is hitNum, [0][1] is voiceMax, [0][2] is minDelay
    placeNoteBlock(loc, configurationList[0][0], configurationList[0][2], configurationList[1], configurationList[2], gameName)
    placeRepeater(loc, configurationList[0][0], configurationList[0][2], configurationList[1], configurationList[2], gameName)
    placeRedstoneWire(loc, configurationList[0][0], configurationList[0][1], configurationList[0][2], configurationList[1], configurationList[2], gameName)
    placeBaseLine(loc, configurationList[1], gameName)
    
    gameName.postToChat("Midi file successfully processed and attached in-game!")
    gameName.postToChat("If you wish to process another, reload the program.")