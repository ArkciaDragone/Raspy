import sys
sys.path.append("..")

from numpy import gcd

import mcpi.minecraft as mmc
import tools
from read_midi_file import read_and_process_midi, get_bpm_set, get_first_bpm

mc = tools.start(0)

mc.postToChat("Test mode, please input a path.")

while True:
    posts = mc.events.pollChatPosts()
    if len(posts) > 0:
        path_with_hyphen = posts[0].message
        path = path_with_hyphen.lstrip("-")
        a = list(read_and_process_midi(path))
        b = get_bpm_set(path)
        c = get_first_bpm(path)
        print("This is the gcd:\n")
        print(gcd.reduce([hit[0] for hit in a]))
        print("\nThis is the hitlist:\n")
        print([hit for hit in a])
        print("\nThis is the set of BPM:\n")
        print(b)
        print("\nThis is the first BPM:\n")
        print(c)
        break