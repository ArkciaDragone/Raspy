# --------------------
# ask_config.py
# Let the user define their own way of configuration
# --------------------

import sys
sys.path.append("..")

from read_midi_file import get_first_bpm, read_and_process_midi

# --------------------
# ask_config_way
# --------------------

def ask_config_way(game_name):
    game_name.postToChat("")
    game_name.postToChat("There are currently two ways of configuring the redstone system.")
    game_name.postToChat("Way 1 is to make all note blocks mono-timbre, which also means the pitch range will be reduced. You can choose the timbre later.")
    game_name.postToChat("Way 2 is to remain all notes in the same pitches. The program will choose double bass as the timbre of low range, harp as of medium range, glockenspiel as of high range.")
    game_name.postToChat("Input 1 or 2 to decide which way to configure.")
    game_name.postToChat("")

    while True:
        decide_config_post = game_name.events.pollChatPosts()
        if len(decide_config_post) > 0:
            decide_config = decide_config_post[0].message
            try:
                a = int(decide_config)
            except ValueError:      # decideConfig is not an integer
                game_name.events.clearAll()
                game_name.postToChat("")
                game_name.postToChat("You didn't input an integer, please input again.")
                game_name.postToChat("")
                continue
            else:
                game_name.events.clearAll()
                if a == 1 or a == 2:
                    b = ask_timbre(a, game_name)
                    return [a, b]
                else:
                    game_name.postToChat("")
                    game_name.postToChat("Your input doesn't fall between 1 and 2, please input again.")
                    game_name.postToChat("")
                    continue

# --------------------
# ask_timbre
# --------------------

def ask_timbre(a, game_name):

    if a == 1:

        game_name.postToChat("")
        game_name.postToChat("There are currently seven timbres:")
        game_name.postToChat("")
        game_name.postToChat("Harp/piano (1), double bass (2), glockenspiel (3), flute (4), chime (5), guitar (6), xylophone (7).")
        game_name.postToChat("")
        game_name.postToChat("Input an integer between 1 and 7 to choose your timbre.")
        game_name.postToChat("")

        while True:
            decide_timbre_post = game_name.events.pollChatPosts()
            if len(decide_timbre_post) > 0:
                decide_timbre = decide_timbre_post[0].message
                try:
                    b = int(decide_timbre)
                except ValueError:      # decideTimbre is not an integer
                    game_name.events.clearAll()
                    game_name.postToChat("")
                    game_name.postToChat("You didn't input an integer, please input again.")
                    game_name.postToChat("")
                    continue
                else:
                    game_name.events.clearAll()
                    if 1 <= b <= 7:
                        return b
                    else:
                        game_name.postToChat("")
                        game_name.postToChat("Your input doesn't fall between 1 and 7, please input again.")
                        game_name.postToChat("")
                        continue

    if a == 2:
        return 0

# --------------------
# ask_tempo
# --------------------

def ask_tempo_and_process(path, game_name):

    tempo = get_first_bpm(path)
    tempo_int = int(tempo)

    # if the path is correct, then post the following
    game_name.postToChat("")
    game_name.postToChat("Configuring redstone system...")
    game_name.postToChat("")

    if tempo < 37.5:
        game_name.postToChat("The minimum tempo of a redstone music system is 37.5 bpm, but your file has a tempo lower than that, which is %s."%tempo_int)
    elif 37.5 < tempo < 75:
        game_name.postToChat("The tempo of a redstone music system can either be 37.5 bpm or 75 bpm, but your file has a tempo in between, which is %s."%tempo_int)
    elif 75 < tempo < 150:
        game_name.postToChat("The tempo of a redstone music system can either be 75 bpm or 150 bpm, but your file has a tempo in between, which is %s."%tempo_int)
    elif tempo > 150:
        game_name.postToChat("The maximum tempo of a redstone music system is 150 bpm, but your file has a tempo higher than that, which is %s."%tempo_int)
    elif tempo == 37.5 or tempo == 75 or tempo == 150:
        game_name.postToChat("Congratulations! You can construct the redstone music system in exactly %s bpm."%tempo_int)
    
    game_name.postToChat("")
    game_name.postToChat("Due to the in-game mechanics, the tempo of a redstone music system can only be one of 37.5 bpm, 75 bpm, or 150 bpm. Choose one and enter it, so that the system can be configured in that way.")
    game_name.postToChat("")

    while True:
        decide_tempo_post = game_name.events.pollChatPosts()
        if len(decide_tempo_post) > 0:
            decide_tempo = decide_tempo_post[0].message
            try:
                a = float(decide_tempo)
            except ValueError:      # decideTempo is not a float
                game_name.events.clearAll()
                game_name.postToChat("")
                game_name.postToChat("You didn't input a valid number, please input again.")
                game_name.postToChat("")
                continue
            else:
                game_name.events.clearAll()
                if a == 37.5:
                    hit_list = list(read_and_process_midi(path, 1 / 16))
                    return hit_list
                if a == 75:
                    hit_list = list(read_and_process_midi(path, 1 / 8))
                    return hit_list
                if a == 150:
                    hit_list = list(read_and_process_midi(path, 1 / 4))
                    return hit_list
                else:
                    game_name.postToChat("")
                    game_name.postToChat("Your input doesn't fall among 37.5, 75 or 150, please input again.")
                    game_name.postToChat("")
                    continue