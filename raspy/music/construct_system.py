# --------------------
# construct_system.py
# Attach the configured redstone system in game
# --------------------

import sys
sys.path.append("..")

from math import pow

import mcpi.block as block
import mcpi.connection

# --------------------
# x_boundary
# --------------------

def x_boundary(voice_max):
    """Define the horizontal boundary of glass cover"""
    return [- voice_max - 1, voice_max + 1]

# --------------------
# base_line_length
# --------------------

def base_line_length(base_line_row):
    return 3 + 2 * (base_line_row - 1)

# --------------------
# z_boundary
# --------------------

def z_boundary(hit_num, min_delay, repeater_num, processed_list, base_line_length):
    """Define the vertical boundary of glass cover"""
    if processed_list[-1][0] == 0:      # hit_num == 1
        num = 1
    else:
        num = int(processed_list[-1][0] / min_delay) + 1
    
    length = base_line_length + 1 + (num - 1) * (2 + repeater_num) + 4

    if hit_num == 1 and num == 1:
        return [-1, -1 + length - 1 + 3]
    else:
        return [-1, -1 + length - 1]

# --------------------
# place_stone
# --------------------

def place_stone(loc, x_boundary, z_boundary, game_name):
    # place stone in the bottom
    game_name.setBlocks(
        loc.x + x_boundary[0], loc.y - 1, loc.z + z_boundary[0],
        loc.x + x_boundary[1], loc.y - 1, loc.z + z_boundary[1],
        block.STONE.id)

# --------------------
# place_glass
# --------------------

def place_glass(loc, x_boundary, z_boundary, game_name):
    # place in the front and in the back
    game_name.setBlocks(
        loc.x + x_boundary[0], loc.y, loc.z + z_boundary[0],
        loc.x + x_boundary[1], loc.y + 6, loc.z + z_boundary[0],
        block.GLASS.id)
    game_name.setBlocks(
        loc.x + x_boundary[0], loc.y, loc.z + z_boundary[1],
        loc.x + x_boundary[1], loc.y + 6, loc.z + z_boundary[1],
        block.GLASS.id)
    # place in the left and in the right
    game_name.setBlocks(
        loc.x + x_boundary[0], loc.y, loc.z + z_boundary[0],
        loc.x + x_boundary[0], loc.y + 6, loc.z + z_boundary[1],
        block.GLASS.id)
    game_name.setBlocks(
        loc.x + x_boundary[1], loc.y, loc.z + z_boundary[0],
        loc.x + x_boundary[1], loc.y + 6, loc.z + z_boundary[1],
        block.GLASS.id)
    # place the top cover
    game_name.setBlocks(
        loc.x + x_boundary[0], loc.y + 7, loc.z + z_boundary[0],
        loc.x + x_boundary[1], loc.y + 7, loc.z + z_boundary[1],
        block.GLASS.id)

# --------------------
# place_air
# --------------------

def place_air(loc, x_boundary, z_boundary, game_name):
    # place inside glass cover
        game_name.setBlocks(
        loc.x + x_boundary[0] + 1, loc.y + 0, loc.z + z_boundary[0] + 1,
        loc.x + x_boundary[1] - 1, loc.y + 6, loc.z + z_boundary[1] - 1,
        block.AIR.id)

# --------------------
# place_door_and_terracotta
# --------------------

def place_door_and_terracotta(loc, z_boundary, game_name):

    # place front door and terracotta around
    game_name.setBlock(loc.x, loc.y, loc.z + z_boundary[0], block.DOOR_BIRCH.id, 0)      # lower door
    game_name.setBlock(loc.x, loc.y + 1, loc.z + z_boundary[0], block.DOOR_BIRCH.id, 8)      # upper door
    game_name.setBlock(loc.x, loc.y + 2, loc.z + z_boundary[0], block.LIGHT_BLUE_GLAZED_TERRACOTTA.id, 0)
    game_name.setBlocks(
        loc.x - 1, loc.y, loc.z + z_boundary[0],
        loc.x - 1, loc.y + 2, loc.z + z_boundary[0],
        block.LIGHT_BLUE_GLAZED_TERRACOTTA.id)
    game_name.setBlocks(
        loc.x + 1, loc.y, loc.z + z_boundary[0],
        loc.x + 1, loc.y + 2, loc.z + z_boundary[0],
        block.LIGHT_BLUE_GLAZED_TERRACOTTA.id)

    # place back door and terracotta around
    game_name.setBlock(loc.x, loc.y, loc.z + z_boundary[1], block.DOOR_BIRCH.id, 0)      # lower block
    game_name.setBlock(loc.x, loc.y + 1, loc.z + z_boundary[1], block.DOOR_BIRCH.id, 9)      # upper block
    game_name.setBlock(loc.x, loc.y + 2, loc.z + z_boundary[1], block.LIGHT_BLUE_GLAZED_TERRACOTTA.id, 0)
    game_name.setBlocks(
        loc.x - 1, loc.y, loc.z + z_boundary[1],
        loc.x - 1, loc.y + 2, loc.z + z_boundary[1],
        block.LIGHT_BLUE_GLAZED_TERRACOTTA.id)
    game_name.setBlocks(
        loc.x + 1, loc.y, loc.z + z_boundary[1],
        loc.x + 1, loc.y + 2, loc.z + z_boundary[1],
        block.LIGHT_BLUE_GLAZED_TERRACOTTA.id)

# --------------------
# place_note_block
# --------------------

def place_note_block(loc, config_way, hit_num, voice_max, min_delay, repeater_num, processed_list, the_base_line_length, game_name):

    if config_way[0] == 1:
        for j in range(0, hit_num):
            for k in range(0, len(processed_list[j][1])):      # the number of notes in processed_list[j]
                game_name.setNoteBlock(loc.x + (- voice_max + 1 + 2 * k), loc.y, loc.z + the_base_line_length + 1 + processed_list[j][0] / min_delay * (2 + repeater_num), processed_list[j][1][k])

        if config_way[1] == 1:      # harp/piano timbre
            for j in range(0, hit_num):
                for k in range(0, len(processed_list[j][1])):
                    game_name.setBlock(loc.x + (- voice_max + 1 + 2 * k), loc.y - 1, loc.z + the_base_line_length + 1 + processed_list[j][0] / min_delay * (2 + repeater_num), block.GRASS.id)
        elif config_way[1] == 2:      # double bass timbre
            for j in range(0, hit_num):
                for k in range(0, len(processed_list[j][1])):
                    game_name.setBlock(loc.x + (- voice_max + 1 + 2 * k), loc.y - 1, loc.z + the_base_line_length + 1 + processed_list[j][0] / min_delay * (2 + repeater_num), block.WOOD.id)
        elif config_way[1] == 3:      # glockenspiel timbre
            for j in range(0, hit_num):
                for k in range(0, len(processed_list[j][1])):
                    game_name.setBlock(loc.x + (- voice_max + 1 + 2 * k), loc.y - 1, loc.z + the_base_line_length + 1 + processed_list[j][0] / min_delay * (2 + repeater_num), block.GOLD_BLOCK.id)
        elif config_way[1] == 4:      # flute timbre
            for j in range(0, hit_num):
                for k in range(0, len(processed_list[j][1])):
                    game_name.setBlock(loc.x + (- voice_max + 1 + 2 * k), loc.y - 1, loc.z + the_base_line_length + 1 + processed_list[j][0] / min_delay * (2 + repeater_num), block.CLAY.id)
        elif config_way[1] == 5:      # chime timbre
            for j in range(0, hit_num):
                for k in range(0, len(processed_list[j][1])):
                    game_name.setBlock(loc.x + (- voice_max + 1 + 2 * k), loc.y - 1, loc.z + the_base_line_length + 1 + processed_list[j][0] / min_delay * (2 + repeater_num), block.PACKED_ICE.id)
        elif config_way[1] == 6:      # guitar timbre
            for j in range(0, hit_num):
                for k in range(0, len(processed_list[j][1])):
                    game_name.setBlock(loc.x + (- voice_max + 1 + 2 * k), loc.y - 1, loc.z + the_base_line_length + 1 + processed_list[j][0] / min_delay * (2 + repeater_num), block.WOOL.id)
        elif config_way[1] == 7:      # xylophone timbre
            for j in range(0, hit_num):
                for k in range(0, len(processed_list[j][1])):
                    game_name.setBlock(loc.x + (- voice_max + 1 + 2 * k), loc.y - 1, loc.z + the_base_line_length + 1 + processed_list[j][0] / min_delay * (2 + repeater_num), block.BONE_BLOCK.id)

    if config_way[0] == 2:

        for j in range(0, hit_num):
            for k in range(0, len(processed_list[j][1])):
                if 0 <= processed_list[j][1][k] < 24:      # low range, use double bass timbre
                    game_name.setNoteBlock(loc.x + (- voice_max + 1 + 2 * k), loc.y, loc.z + the_base_line_length + 1 + processed_list[j][0] / min_delay * (2 + repeater_num), processed_list[j][1][k])
                    game_name.setBlock(loc.x + (- voice_max + 1 + 2 * k), loc.y - 1, loc.z + the_base_line_length + 1 + processed_list[j][0] / min_delay * (2 + repeater_num), block.WOOD.id)
                if 24 <= processed_list[j][1][k] < 48:      # medium range, use harp/piano timbre
                    game_name.setNoteBlock(loc.x + (- voice_max + 1 + 2 * k), loc.y, loc.z + the_base_line_length + 1 + processed_list[j][0] / min_delay * (2 + repeater_num), processed_list[j][1][k] - 24)
                    game_name.setBlock(loc.x + (- voice_max + 1 + 2 * k), loc.y - 1, loc.z + the_base_line_length + 1 + processed_list[j][0] / min_delay * (2 + repeater_num), block.GRASS.id)
                if 48 <= processed_list[j][1][k] <= 72:      # high range, use glockenspiel timbre
                    game_name.setNoteBlock(loc.x + (- voice_max + 1 + 2 * k), loc.y, loc.z + the_base_line_length + 1 + processed_list[j][0] / min_delay * (2 + repeater_num), processed_list[j][1][k] - 48)
                    game_name.setBlock(loc.x + (- voice_max + 1 + 2 * k), loc.y - 1, loc.z + the_base_line_length + 1 + processed_list[j][0] / min_delay * (2 + repeater_num), block.GOLD_BLOCK.id)

# --------------------
# place_repeater
# --------------------

def place_repeater(loc, hit_num, voice_max, min_delay, repeater_num, processed_list, the_base_line_length, game_name):
    for i in range(- voice_max + 1, voice_max, 2):
        for j in range(0, int(processed_list[-1][0] / min_delay)):
            if int(min_delay % 4) == 0:
                game_name.setBlock(loc.x + i, loc.y, loc.z + the_base_line_length + 3 + repeater_num - 1 + j * (2 + repeater_num), block.UNPOWERED_REPEATER.id, 2 + 12)      # delay = 4
            else:
                game_name.setBlock(loc.x + i, loc.y, loc.z + the_base_line_length + 3 + repeater_num - 1 + j * (2 + repeater_num), block.UNPOWERED_REPEATER.id, 2 + 4 * (int(min_delay % 4) - 1))      # delay != 4
            for k in range(0, repeater_num - 1):      # range(0, 0) = []
                game_name.setBlock(loc.x + i, loc.y, loc.z + the_base_line_length + 3 + k + j * (2 + repeater_num), block.UNPOWERED_REPEATER.id, 2 + 12)      # delay = 4
                # 2 means facing south (z-axis positive)

# --------------------
# place_redstone_wire
# --------------------

def place_redstone_wire(loc, hit_num, voice_max, min_delay, repeater_num, processed_list, the_base_line_length, game_name):
    
    for i in range(- voice_max + 1, voice_max, 2):
        for j in range(0, int(processed_list[-1][0] / min_delay)):
            game_name.setBlock(loc.x + i, loc.y, loc.z + the_base_line_length + 2 + j * (2 + repeater_num), block.REDSTONE_WIRE.id)
    
    # also place a redstone wire if "3 + processed_list[j][0] / min_delay * (2 + repeater_num)" has no note block because of note lacking on this specific voice
    for k in range(0, hit_num):
        for l in range(len(processed_list[k][1]), voice_max):
            game_name.setBlock(loc.x + (- voice_max + 1 + 2 * l), loc.y, loc.z + the_base_line_length + 1 + processed_list[k][0] / min_delay * (2 + repeater_num), block.REDSTONE_WIRE.id)

    for m in range(0, int(processed_list[-1][0] / min_delay)):
        if m * min_delay not in [processed_listMember[0] for processed_listMember in processed_list]:
            for n in range(- voice_max + 1, voice_max, 2):
                game_name.setBlock(loc.x + n, loc.y, loc.z + the_base_line_length + 1 + m * (2 + repeater_num), block.REDSTONE_WIRE.id)

# --------------------
# place_torch
# --------------------

def place_torch(loc, z_boundary, hit_num, voice_max, repeater_num, the_base_line_length, game_name):
    if hit_num == 1:
        for i in range(- voice_max, voice_max + 1, 2):
            game_name.setBlock(loc.x + i, loc.y, loc.z + the_base_line_length, block.TORCH.id)
    else:
        # place torch every three rows of repeaters
        for i in range(- voice_max, voice_max + 1, 2):
            m = -3
            while True:
                m += 3
                if the_base_line_length + 3 + m * (2 + repeater_num) >= z_boundary[1]:
                    break
                game_name.setBlock(loc.x + i, loc.y, loc.z + the_base_line_length + 3 + m * (2 + repeater_num), block.TORCH.id)

# --------------------
# place_base_line
# --------------------

def place_base_line(loc, voice_max, the_base_line_row, the_base_line_length, game_name):

    x_list = [i for i in range(- voice_max + 1, voice_max, 2)]
    x_list_2 = []
    a = the_base_line_length      # loc.z + the_base_line_length is exactly the z coordinate for the frontmost row of repeaters
    row_num = 0
    
    while True:
        b, c = 0, -1
        row_num += 1
        while True:
            while True:
                c += 1
                if c == len(x_list) - 1:
                    break
                if x_list[c + 1] - x_list[b] > (29 - (pow(2, the_base_line_row - row_num) - 1) - 1):      # reachs maximum length
                    break
                else:
                    continue
            for x in range(b, c + 1):
                game_name.setBlock(loc.x + x_list[x], loc.y, loc.z + a, block.UNPOWERED_REPEATER.id, 2)
            for x in range(x_list[b], x_list[c] + 1):
                game_name.setBlock(loc.x + x, loc.y, loc.z + a - 1, block.REDSTONE_WIRE.id)
            middle_x = int((x_list[b] + x_list[c]) / 2)
            x_list_2.append(middle_x)
            if c == len(x_list) - 1:
                break
            else:
                b = c + 1
                c = b - 1
        a -= 2
        x_list = x_list_2
        x_list_2 = []
        if len(x_list) == 1:
            game_name.setBlock(loc.x + x_list[0], loc.y, loc.z + a, block.WOODEN_BUTTON.id, 5)
            break
        else:
            continue
            
# --------------------
# construct_redstone_system
# --------------------

def construct_redstone_system(cl, game_name):      # cl means configurationList

    game_name.postToChat("")
    game_name.postToChat("Please input (in-game) the name of the player beside whom the note block system is placed:")
    game_name.postToChat("")
    
    while True:
        posts = game_name.events.pollChatPosts()
        if len(posts) > 0:
            try:
                name = posts[0].message
                id = game_name.getPlayerEntityId(name)
            except mcpi.connection.RequestError:
                game_name.events.clearAll()
                game_name.postToChat("")
                game_name.postToChat("Wrong name, please input again:")
                game_name.postToChat("")
                continue
            else:
                game_name.events.clearAll()
                break
    
    loc = game_name.entity.getPos(id);

    game_name.postToChat("")
    game_name.postToChat("Attaching...")
    game_name.postToChat("This takes less than a minute for a medium-sized midi file.")
    game_name.postToChat("")

    # cl[0] is config_way, [1] is preProcess2Result, [2] is processed_list
    # cl[1][0] is hit_num, [1][1] is voice_max, [1][2] is min_delay, [1][3] is repeater_num, [1][6] is base_line_row
    
    the_x_boundary = x_boundary(cl[1][1])
    the_base_line_length = base_line_length(cl[1][6])
    the_z_boundary = z_boundary(cl[1][0], cl[1][2], cl[1][3], cl[2], the_base_line_length)

    place_stone(loc, the_x_boundary, the_z_boundary, game_name)
    place_glass(loc, the_x_boundary, the_z_boundary, game_name)
    place_air(loc, the_x_boundary, the_z_boundary, game_name)
    place_door_and_terracotta(loc, the_z_boundary, game_name)

    place_note_block(loc, cl[0], cl[1][0], cl[1][1], cl[1][2], cl[1][3], cl[2], the_base_line_length, game_name)
    place_repeater(loc, cl[1][0], cl[1][1], cl[1][2], cl[1][3], cl[2], the_base_line_length, game_name)
    place_redstone_wire(loc, cl[1][0], cl[1][1], cl[1][2], cl[1][3], cl[2], the_base_line_length, game_name)

    place_base_line(loc, cl[1][1], cl[1][6], the_base_line_length, game_name)
    place_torch(loc, the_z_boundary, cl[1][0], cl[1][1], cl[1][3], the_base_line_length, game_name)
    
    game_name.postToChat("Midi file successfully processed and attached in-game!")
    game_name.postToChat("If you wish to process another, reload the program.")