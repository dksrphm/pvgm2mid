#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage


def noteOn(track, chnum, note, velocity, time):
    track.append(Message('note_on', channel=chnum, note=note, velocity=int(velocity), time=int(time)))


def noteOff(track, chnum, note, velocity, time):
    track.append(Message('note_off', channel=chnum, note=note, velocity=int(velocity), time=int(time)))


def sample2tick(sample, tempo, resolution):
    # VGM sample # -> midi time
    # VGM sample: 44100 = 1s
    # MIDI time: 1bpm = resolution(480)
    tick = mido.second2tick(second = sample / 44100, ticks_per_beat = resolution, tempo = mido.bpm2tempo(tempo))
    
    # add 4 beats time(Initial Measure)
    return(tick + 4 * resolution)


def main():
    pass


if __name__ == "__main__":
    main()
