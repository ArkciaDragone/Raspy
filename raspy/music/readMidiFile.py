# --------------------
# Important Note:
# Packages "mido" and "python-rtmidi" should be pre-installed to run this application.
# Use "pip install <package-name>" in cmd to install.
# --------------------
from mido import MidiFile, Message, MetaMessage
from mido.midifiles.midifiles import DEFAULT_TEMPO
from mido.midifiles.tracks import merge_tracks, _to_abstime
import pprint
import fractions
from operator import attrgetter

"""
Mido Memo
note 60 = middle C

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


def second2duration(second: float, tempo: int):
    """Convert from real time (in seconds) to note duration (e.g. 1 / 8)"""
    return second * 1000 / tempo


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
            dt = 0.0
        elif msg.type == 'set_tempo':
            tempo = msg.tempo
    # Last note
    dt = (tick - last) / f.ticks_per_beat
    if dt % resolution == 0:
        yield int(dt / resolution), output


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


# def save_processed_file(path: str, out: str = None, resolution=1 / 16):
#     if out is None: out = path
#     f = MidiFile(ticks_per_beat=1)
#     # tempo = 100000


if __name__ == '__main__':
    files = [r'C:\Users\lenovo\Desktop\BWV 934 - cut.mid',
             r'E:\Downloads\最终鬼畜妹フランドール.S（慢拍） -Ab调.mid',
             r'E:\Downloads\最终鬼畜妹变态版.mid']
    for f in files:
        print(f"\n*** {f} ***\n")
        pprint.pprint([i for i in readAndProcessMidi(f)])
