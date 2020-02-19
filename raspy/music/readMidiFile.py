# --------------------
# readMidiFile.py
# Process the requested midi file (and other relative functions)
#
# Important Note:
# Package "mido" should be pre-installed to run this application.
# Use "pip install <package-name>" in cmd to install.
# --------------------

from typing import Set
from mido import MidiFile, Message, MetaMessage, tempo2bpm, bpm2tempo
from mido.midifiles.midifiles import DEFAULT_TEMPO
from mido.midifiles.tracks import merge_tracks, _to_abstime
# import pprint
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
  - The default tempo: 500000 μs/beat = BPM 120.
    The meta message ‘set_tempo’ can be used to change tempo
    bpm2tempo() & tempo2bpm()
  - f.ticks_per_beat: CONST, also called PPQ
    tick2second() & second2tick()
  - f.type: 0 single track, 1 synchronous, 2 asynchronous
  - f.length: total playback time in seconds
  - for i, track in enumerate(f.tracks)

Instrument:
    Midi files assign different instruments for each "channel" instead of
    tracks, and each track is not associated with a certain channel.
    Notes in a track can be sent to a certain channel to be played, and
    therefore by the corresponding instrument of that channel.
    To assign an instrument to a channel, use a message of type
    "program_change" with the target instrument as its "program" attribute.
    The "program" attribute is specified in General Midi Instrument List.
    However, this list starts from 1 instead of 0, which differs from midi
    files. In the function belowAn offset parameter is provided to determine
    whether this offset should be adjusted.
"""


def second2duration(second: float, tempo: int):
    """Convert from real time (in seconds) to note duration (e.g. 1 / 8)"""
    return second * 1000 / tempo


def readAndProcessMidi(path: str, resolution=1 / 8):
    """Path is supposed to lead to a valid midi file"""
    f = MidiFile(path)
    assert f.type != 2, "asynchronous midi files are not supported yet"
    messages = []
    for track in f.tracks:
        messages.extend(_to_abstime(track))
    assert messages, "failed to find messages. Erroneous file?"
    messages = [m for m in messages if m.type == 'note_on' and m.velocity > 0]
    messages.sort(key=attrgetter('time'))
    output = set()
    TOLERANCE = resolution / 4
    i = skipped = 0
    last = beat = messages[i].time / f.ticks_per_beat
    while i < len(messages):
        if messages[i].time / f.ticks_per_beat < beat - TOLERANCE:
            # Falls behind, then discard
            skipped += 1
            i += 1
        elif messages[i].time / f.ticks_per_beat <= beat + TOLERANCE:
            # Collected
            output.add(messages[i].note)
            i += 1
        else:  # Exceeded, then advance
            if output:
                yield int((beat - last) / resolution), list(output)
                output.clear()
                last = beat
            beat += resolution
    if output:  # Last notes
        yield int((beat - last) / resolution), list(output)
    print(f"  {path} - Total={i}; Skipped={skipped}; Loss={skipped / i * 100:.2f}%")


def musical_extract_midi(path: str):
    """Generates (BPM: float, duration since last: float, [pitch: int])"""
    f = MidiFile(path)
    assert f.type != 2, "asynchronous midi files are not supported yet"
    messages = []
    for track in f.tracks:
        messages.extend(_to_abstime(track))
    assert messages, "failed to find messages. Erroneous file?"
    messages.sort(key=attrgetter('time'))
    tempo = DEFAULT_TEMPO
    last = tick = 0
    output = set()
    for msg in messages:
        if msg.type == 'note_on' and msg.velocity > 0:
            if msg.time == tick:  # Current hit
                output.add(msg.note)
            elif output:  # New hit
                yield tempo2bpm(tempo), (tick - last) / f.ticks_per_beat, list(output)
                output = {msg.note}
                last, tick = tick, msg.time
            else:  # Non-0 Beginning
                last = tick = msg.time
                output.add(msg.note)
        elif msg.type == 'set_tempo':
            tempo = msg.tempo
    # Last hit
    if output:
        yield tempo2bpm(tempo), (tick - last) / f.ticks_per_beat, list(output)


def getBpmSet(path: str) -> Set[float]:
    bpm = set()
    f = MidiFile(path)
    for track in f.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                bpm.add(tempo2bpm(msg.tempo))
    return bpm


def getFirstBpm(path: str) -> float:
    for track in MidiFile(path).tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                return tempo2bpm(msg.tempo)


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


def save_processed_file(path: str, out: str = None, resolution=1 / 16):
    if out is None:
        out = path
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
    print(f"{i} hits wrote to {out}")


def save_musical_file(path: str, out: str = None):
    if out is None:
        out = path
    f = MidiFile()
    ap = f.add_track('Main').append
    last_bpm = tempo2bpm(DEFAULT_TEMPO)
    ap(MetaMessage("set_tempo", tempo=DEFAULT_TEMPO))
    notes_on = []
    i = 0
    for bpm, duration, notes in musical_extract_midi(path):
        i += 1
        if notes_on:
            ap(Message(type='note_off', note=notes_on[0],
                       time=int(duration * f.ticks_per_beat * 0.95)))
            for n in notes_on[1:]:
                ap(Message(type='note_off', note=n, time=0))
        notes_on = notes
        ap(Message(type='note_on', note=notes_on[0],
                   time=int(duration * f.ticks_per_beat * 0.05)))
        for n in notes_on:
            ap(Message(type='note_on', note=n, time=0))
        if bpm != last_bpm:
            last_bpm = bpm
            ap(MetaMessage("set_tempo", tempo=bpm2tempo(bpm)))
    if notes_on:  # Last note; just make it 1 beat long
        ap(Message(type='note_off', note=notes_on[0], time=f.ticks_per_beat))
        for n in notes_on[1:]:
            ap(Message(type='note_off', note=n, time=0))
    f.save(out)
    print(f"{i} hits wrote to {out}")


def musical_extract_midi_with_inst(path: str, offset=True):
    """Generates (BPM: float, duration since last: float,
    [(pitch: int, instrument_index: int)])"""
    if offset:
        offset = 1
    else:
        offset = 0
    f = MidiFile(path)
    assert f.type != 2, "asynchronous midi files are not supported yet"
    messages = []
    for track in f.tracks:
        messages.extend(_to_abstime(track))
    assert messages, "failed to find messages. Erroneous file?"
    messages.sort(key=attrgetter('time'))
    tempo = DEFAULT_TEMPO
    last = tick = 0
    output = set()
    insts = dict()
    for msg in messages:
        if msg.type == 'note_on' and msg.velocity > 0:
            if msg.time == tick:  # Current hit
                output.add((msg.note, insts.get(msg.channel, offset)))
            elif output:  # New hit
                yield (tempo2bpm(tempo),
                       (tick - last) / f.ticks_per_beat, list(output))
                output = {(msg.note, insts.get(msg.channel, offset))}
                last, tick = tick, msg.time
            else:  # Non-0 Beginning
                last = tick = msg.time
                output.add((msg.note, insts.get(msg.channel, offset)))
        elif msg.type == 'set_tempo':
            tempo = msg.tempo
        elif msg.type == 'program_change':
            insts[msg.channel] = msg.program + offset
    # Last hit
    if output:
        yield tempo2bpm(tempo), (tick - last) / f.ticks_per_beat, list(output)


# if __name__ == '__main__':
#     files = [r"E:\Downloads\Phoenix_Wright_Ace_Attorney_-_Pressing_Pursuit_Cornered.mid",
#              r"E:\Downloads\Deltarune_-_THE_WORLD_REVOLVING.mid",
#              r"E:\Downloads\Undertale_OST_-_068_-_Death_By_Glamour.mid"]
#     pprint.pprint(list(musical_extract_midi_with_inst(files[2])))
