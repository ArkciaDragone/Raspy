# --------------------
# readMidiFile.py
# Process the requested midi file
# 
# Important Note:
# Packages "mido" and "pprint" should be pre-installed to run this application.
# Use "pip install <package-name>" in cmd to install.
# --------------------
from typing import Set
from mido import MidiFile, Message, MetaMessage, tempo2bpm
from mido.midifiles.midifiles import DEFAULT_TEMPO
from mido.midifiles.tracks import merge_tracks, _to_abstime
import pprint
import fractions
from operator import attrgetter

"""
Mido Memo
note 60 = C4 (note 66 = F#4)

Message:
 - Important message types:
   note_on: channel, note, velocity
   note_off: channel, note, velocity
 - msg.is_meta
 - Important meta message types:
   end_of_track
   set_tempo: tempo (int)
   time_signature: numerator (int), denominator (int), ...
 - msg.type == 'note_on'
 - msg.time: Inside a track, it is delta time in ticks. (int)
             In messages yielded from play(), it is delta time in seconds
             (time elapsed since the last yielded message)

File f:
 - The default tempo: 500000 ms/beat = BPM 120.
   The meta message ‘set_tempo’ can be used to change tempo
   bpm2tempo() & tempo2bpm()
 - f.ticks_per_beat: CONST, also called PPQ
   tick2second() & second2tick()
 - f.type: 0 single track, 1 synchronous, 2 asynchronous
 - f.length: total playback time in seconds
 - for i, track in enumerate(f.tracks)
"""


# --------------------
# second2duration
# --------------------

def second2duration(second: float, tempo: int):
    """Convert from real time (in seconds) to note duration (e.g. 1 / 8)"""
    return second * 1000 / tempo


# --------------------
# readAndProcessMidi
# --------------------

def readAndProcessMidi(path: str, resolution=1 / 16):
    """Path is supposed to lead to a valid midi file"""
    f = MidiFile(path)
    assert f.type != 2, "asynchronous midi files are not supported yet"
    messages = []
    for track in f.tracks:
        messages.extend(_to_abstime(track))
    assert messages, "failed to find messages. Erroneous file?"
    messages.sort(key=attrgetter('time'))
    tempo = DEFAULT_TEMPO
    tick, last = messages[0].time, 0
    output = []
    for msg in messages:
        if msg.type == 'note_on':
            if output:  # Current tick
                if msg.time == tick:
                    output.append(msg.note)
                else:
                    dt = (tick - last) / f.ticks_per_beat
                    if dt % resolution == 0:
                        last = tick
                        yield int(dt / resolution), output
                    output = [msg.note]
                    tick = msg.time
            else:  # New tick
                output.append(msg.note)
                tick = msg.time
        elif msg.type == 'set_tempo':
            tempo = msg.tempo
    # Last note
    dt = (tick - last) / f.ticks_per_beat
    if dt % resolution == 0:
        yield int(dt / resolution), output


def getBpmSet(path: str) -> Set[float]:
    bpm = set()
    f = MidiFile(path)
    for track in f.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                bpm.add(tempo2bpm(msg.tempo))
    return bpm


# --------------------
# _test
# --------------------

def _test(path):
    f = MidiFile(path)
    dt, min_dt = 0.0, 99999
    freqs = {}
    for msg in f:
        dt += msg.time
        if msg.type == 'set_tempo':
            freq = freqs[msg.tempo] = {}
        if msg.type == 'note_on':
            # print("Note:", msg.note, "dt:", dt)
            if dt:
                try:
                    freq[dt] += 1
                except KeyError:
                    freq[dt] = 1
                min_dt = min(min_dt, dt)
            dt = 0.0
    pprint.pprint(freqs)
    print("Min dt:", min_dt)


# --------------------
# tempo_consistency_test
# --------------------

def tempo_consistency_test(path):
    dt = 0
    tempo_dict = {}
    f = MidiFile(path)
    for track in f.tracks:
        tempos = tempo_dict[track.name] = []
        for msg in track:
            dt += msg.time
            if msg.type == 'set_tempo':
                tempos.append(dt)
                dt = 0
    pprint.pprint(tempo_dict)


# --------------------
# print_time
# --------------------

def print_time(path):
    f = MidiFile(path)
    print(f.filename)
    dt = 0
    for msg in f:
        dt += msg.tick
        if msg.type == 'note_on' and dt:
            duration = fractions.Fraction(dt, f.ticks_per_beat)
            if float(duration) >= 1 / 16:
                print(f"{duration} beat = {float(duration)}")
            dt = 0


# --------------------
# print_tick
# --------------------

def print_tick(path):
    f = MidiFile(path)
    print(f.filename)
    dtick = 0
    for msg in merge_tracks(f.tracks):
        dtick += msg.time
        if msg.type == 'note_on' and dtick:
            duration = fractions.Fraction(dtick, f.ticks_per_beat)
            if float(duration) >= 1 / 16:
                print(f"{duration} beat = {float(duration)}")
            dtick = 0


# --------------------
# save_processed_file
# --------------------

def save_processed_file(path: str, out: str = None, resolution=1 / 16):
    if out is None: out = path
    f = MidiFile(ticks_per_beat=1)
    ap = f.add_track('Main').append
    ap(MetaMessage("set_tempo", tempo=100000))

    def on(note: int, time: int):
        ap(Message(type='note_on', note=note, time=time))

    def off(note: int, time: int):
        ap(Message(type='note_off', note=note, time=time))

    def note(time: int, *notes):
        if notes:
            for n in notes:
                on(n, 0)
            off(notes[0], time)
            for n in notes[1:]:
                off(n, 0)

    i = 0
    for fwd, notes in readAndProcessMidi(path, resolution):
        note(fwd, *notes)
        i += 1
    f.save(out)
    print(i)


# --------------------
# main
# --------------------

# if __name__ == '__main__':
    # files = [r'C:\Users\lenovo\Desktop\BWV 934 - cut.mid',
    #          r'E:\Downloads\最终鬼畜妹フランドール.S（慢拍） -Ab调.mid',
    #          r'E:\Downloads\最终鬼畜妹变态版.mid']
    # for f in files:
    #     print(getTempoSet(f))
    #     print(f"\n*** {f} ***\n")
    #     pprint.pprint([i for i in readAndProcessMidi(f)])
    # for i in range(len(files)):
        # save_processed_file(files[i], f'D:/out{i}.mid', 1 / 4)
        # pprint.pprint([i for i in readAndProcessMidi(files[i])])
