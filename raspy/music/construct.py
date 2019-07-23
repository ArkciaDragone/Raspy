# --------------------
# construct.py
# Use the results from readMidiFile to construct the redstone system in-game
# --------------------

import sys
sys.path.append("..")

from . import readMidiFile as rmf

# --------------------
# constructRedstoneSystem
# --------------------

def constructRedstoneSystem(path):
    hitList = rmf.readandProcessMidi(path)