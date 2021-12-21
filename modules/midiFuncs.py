#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage


def noteOn(track, wnote, wvelocity, wtime):
    track.append(Message('note_on', note=wnote, velocity=wvelocity, time=int(wtime)))


def noteOff(track, wnote, wvelocity, wtime):
    track.append(Message('note_off', note=wnote, velocity=wvelocity, time=int(wtime)))


def sample2tick(sample, wtempo, resolution):
    # VGM sample # -> midi time
    # VGM sample: 44100 = 1s
    # MIDI time: 1bpm = resolution(480)
    tick = mido.second2tick(second = sample / 44100, ticks_per_beat = resolution, tempo = mido.bpm2tempo(wtempo))
    
    # add 4 beats time(Initial Measure)
    return(tick + 4 * resolution)


def main():
    pass


if __name__ == "__main__":
    main()
