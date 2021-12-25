#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage


def initMidiTrack(track, chnum):
    # initialize MIDI track

    track.append(mido.Message('control_change', channel=chnum, control=0, value=0, time=0))    # bank select MSB
    track.append(mido.Message('control_change', channel=chnum, control=32, value=0, time=0))    # bank select MLB
    track.append(mido.Message('program_change', channel=chnum, program=80, time=0))             # program_change(80: square wave)
    track.append(mido.Message('control_change', channel=chnum, control=1, value=0, time=0))     # modulation
    track.append(mido.Message('control_change', channel=chnum, control=7, value=100, time=0))   # channel volume
    track.append(mido.Message('control_change', channel=chnum, control=10, value=64, time=0))   # pan
    track.append(mido.Message('control_change', channel=chnum, control=11, value=127, time=0))  # expression
    track.append(mido.Message('control_change', channel=chnum, control=64, value=0, time=0))    # hold
    track.append(mido.Message('control_change', channel=chnum, control=91, value=40, time=0))   # reverb send
    track.append(mido.Message('control_change', channel=chnum, control=93, value=0, time=0))    # chorus send
    track.append(mido.Message('control_change', channel=chnum, control=94, value=0, time=0))    # delay send level


def setMidiTrackname(track, trackname):
    track.append(mido.MetaMessage('track_name', name=trackname, time=0))


def noteOn(track, chnum, note, velocity, time):
    track.append(Message('note_on', channel=chnum, note=note, velocity=int(velocity), time=int(time)))
    #pass


def noteOff(track, chnum, note, velocity, time):
    track.append(Message('note_off', channel=chnum, note=note, velocity=int(velocity), time=int(time)))
    #pass


def panSet(track, chnum, panpot):
    track.append(mido.Message('control_change', channel=chnum, control=10, value=panpot))


def sample2tick(sample, tempo, resolution):
    # VGM sample # -> midi time
    # VGM sample: 44100 = 1s
    # MIDI time: 1bpm = resolution(480)
    tick = mido.second2tick(second = sample / 44100, ticks_per_beat = resolution, tempo = mido.bpm2tempo(tempo))
    #pass
    
    # add 4 beats time(Initial Measure)
    return(tick + 4 * resolution)


def main():
    pass


if __name__ == "__main__":
    main()
