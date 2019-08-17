# --------------------
# set_system.py
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
from ask_config import ask_tempo_and_process, ask_config_way
from read_midi_file import read_and_process_midi

# --------------------
# set_middle_pitch
# --------------------

def set_middle_pitch(config_way):
    if config_way[0] == 1:
        if config_way[1] == 1:
            return [1, 66]      # 66 = F#4
        elif config_way[1] == 2:
            return [1, 42]      # 42 = F#2
        elif config_way[1] == 3 or config_way[1] == 5 or config_way[1] == 7:
            return [1, 90]      # 90 = F#6
        elif config_way[1] == 4:
            return [1, 78]      # 78 = F#5
        elif config_way[1] == 6:
            return [1, 54]      # 54 = F#3
    elif config_way[0] == 2:
        return [2, 66]

# --------------------
# average_pitch
# --------------------

def average_pitch(voice_max, hit_list):
    
    average_pitch_list = []
    note_num_list = []      # counts number of notes in each voice
    for i in range(0, voice_max):
        average_pitch_list.append(0)      # reserve voice_max spots
        note_num_list.append(0)      # reserve voice_max spots

    hit_num = len(hit_list)
    for j in range(0, hit_num):
        for k in range(0, len(hit_list[j][1])):
            average_pitch_list[k] += hit_list[j][1][k]
            note_num_list[k] += 1

    for l in range(0, voice_max):
        average_pitch_list[l] /= note_num_list[l]

    return average_pitch_list

# --------------------
# pre_process_1
# --------------------

def pre_process_1(hit_list):
    """The part where all errors are raised, if any"""

    hit_num = len(hit_list)
    if hit_num == 0:
        raise ValueError("Nothing")

    voice_max = max([len(hit[1]) for hit in hit_list])
    if voice_max > 28:
        raise ValueError("Too many voices")

    a, b = 1, 14
    base_line_row = 1
    while True:
        if a <= voice_max <= b:
            break
        else:
            a = b + 1
            b *= 2
            base_line_row += 1

    return [hit_num, voice_max, base_line_row]

# --------------------
# pre_process_2
# --------------------

def pre_process_2(hit_num, voice_max, hit_list, middle_pitch, base_line_row):
    """The rest of processing"""

    if hit_num == 1:
        min_delay = 1      # otherwise min_delay will calculate as 0, thus causing NaN in construct_system
    else:
        min_delay = gcd.reduce([hit[0] for hit in hit_list])

    repeater_num = ceil(min_delay / 4)
    
    if middle_pitch[0] == 1:
        average_pitch_list = average_pitch(voice_max, hit_list)
        minus_12_num_list = [floor((average_pitch - middle_pitch[1]) / 12) for average_pitch in average_pitch_list]      # 66 is the medium pitch (F#4) for harp sound
        for i in range(0, len(minus_12_num_list)):
            if minus_12_num_list[i] < 0:
                minus_12_num_list[i] += 1
        return [hit_num, voice_max, min_delay, repeater_num, average_pitch_list, minus_12_num_list, base_line_row]

    elif middle_pitch[0] == 2:
        return [hit_num, voice_max, min_delay, repeater_num, 0, 0, base_line_row]

# --------------------
# process_note_and_delay
# --------------------

def process_note_and_delay(minus_12_num_list, hit_list, middle_pitch):      # actually create a new list called processed_list

    new_hit_list = []
    
    for a in range(0, len(hit_list)):
        new_hit_list.append(list(hit_list[a]))      # turn tuples to lists so that we can modify them

    for i in range(0, len(new_hit_list)):

        # process notes
        if middle_pitch[0] == 1:
            voice_num = len(new_hit_list[i][1])
            for j in range(0, voice_num):
                new_hit_list[i][1][j] -= 12 * minus_12_num_list[j]      # using standard note pitch
                new_hit_list[i][1][j] -= (middle_pitch[1] - 12)      # convert to note block pitch
                while True:
                    if (0 <= new_hit_list[i][1][j] <= 24):
                        break
                    elif (new_hit_list[i][1][j] < 0):
                        new_hit_list[i][1][j] += 12
                        continue
                    elif (new_hit_list[i][1][j] > 24):
                        new_hit_list[i][1][j] -= 12
                        continue
        if middle_pitch[0] == 2:
            voice_num = len(new_hit_list[i][1])
            for j in range(0, voice_num):
                new_hit_list[i][1][j] -= 30      # let F#1 be 0
                while True:
                    if (0 <= new_hit_list[i][1][j] <= 72):      # 0-72 = F#1-F#7
                        break
                    elif (new_hit_list[i][1][j] < 0):
                        new_hit_list[i][1][j] += 12
                        continue
                    elif (new_hit_list[i][1][j] > 24):
                        new_hit_list[i][1][j] -= 12
                        continue

        # process delay
        if i == 0:
            continue
        else:
            for j in range(0, i):
                new_hit_list[i][0] += hit_list[j][0]      # sum-up total delay
    
    return new_hit_list

# --------------------
# set_redstone_system
# --------------------

def set_redstone_system(path, game_name):      # game_name is "mc" in startMidi
    
    # raise ValueError (if any) before asking tempo
    hit_list = list(read_and_process_midi(path))
    pre_process_1_result = pre_process_1(hit_list)

    hit_list = list(ask_tempo_and_process(path, game_name))      # hit_list looks like [(delay, [pitch, pitch]), ...]
    pre_process_1_result = pre_process_1(hit_list)

    # if no errors are raised, ask the user's custom choice(s)
    config_way = ask_config_way(game_name)
    middle_pitch = set_middle_pitch(config_way)
    
    pre_process_2_result = pre_process_2(pre_process_1_result[0], pre_process_1_result[1], hit_list, middle_pitch, pre_process_1_result[2])
    """Output to-be-used vital figures and lists"""
    processed_list = process_note_and_delay(pre_process_2_result[5], hit_list, middle_pitch)      # using minus_12_num_list
    """Let the notes fit in note block's playing range, and sum-up the total previous delay for each hit"""

    print(pre_process_2_result)
    print("\n")
    print(processed_list)

    game_name.postToChat("")
    game_name.postToChat("Configuration completed!")
    
    return [config_way, pre_process_2_result, processed_list]