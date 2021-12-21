#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage, second2tick

from . import funcs
from . import convState
from . import midiFuncs as m

class YM2151:
    def __init__(self, state):
        self.chipname = 'YM2151'
        self.chs = 8    # max channels
        self.con = [0] * self.chs   # connection algorithm
        self.tls = [[0] * 4] * self.chs     # total levels [ch][op]
        self.keyon = [0] * self.chs
        self.note = [0] * self.chs
        self.octave = [0] * self.chs
        self.midinote = [0] * self.chs  # midi note no now
        self.lastmidinote = [0] * self.chs  # midi note # of last key on
        self.lastmiditick = [0] * self.chs  # midi tick # of last key on/off
        self.lch = [0] * self.chs   # left channel
        self.rch = [0] * self.chs   # right channel

        self.mid = MidiFile()
        # track 0: conductor track
        # track 1-: data track
        self.track = [0] * (self.chs + 1)
        for i in range(self.chs + 1):
            self.track[i] = MidiTrack()
            self.mid.tracks.append(self.track[i])

        self.track[0].append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(state.getMidiTempo()), time = 10))
        self.mid.save('new_song.mid')

    def update(self, state, addr, aa, dd):
        #state.setDebug(False)
        if (0x00 <= aa <= 0x07):
            pass

        elif (aa == 0x08):
            # bit 6-3:KeyOn/Off op4-op1
            # bit 2-0:channel num
            chnum = dd & 0x07
            keyon = dd & 0x78
            if (keyon != 0):
                if (self.keyon[chnum] != 0):
                    # on -> on: do nothing
                    pass
                else:
                    # off -> on: keyOn
                    if (state.getSamples() < 1):
                        # sample # < 1 ... initial process. ignore
                        pass
                    else:
                        funcs.dprint(state, "addr:{} KeyOn aa:{} dd:{} chnum:{} keyon:{}".format(hex(addr), hex(aa), hex(dd), hex(chnum), hex(keyon)))
                        tick = m.sample2tick(state.getSamples(), state.getMidiTempo(), state.getMidiResolution())
                        m.noteOn(self.track[chnum + 1], self.midinote[chnum], 100, tick - self.lastmiditick[chnum])
                        self.lastmidinote[chnum] = self.midinote[chnum]
                        self.lastmiditick[chnum] = tick
                        self.keyon[chnum] = keyon
            else:
                if (self.keyon[chnum] != 0):
                    # on -> off: keyoff
                    if (state.getSamples() < 1):
                        pass
                    else:
                        funcs.dprint(state, "addr:{} KeyOff aa:{} dd:{} chnum:{} keyon:{}".format(hex(addr), hex(aa), hex(dd), hex(chnum), hex(keyon)))
                        tick = m.sample2tick(state.getSamples(), state.getMidiTempo(), state.getMidiResolution())
                        m.noteOff(self.track[chnum + 1], self.lastmidinote[chnum], 100, tick - self.lastmiditick[chnum])
                        self.lastmiditick[chnum] = tick
                        self.keyon[chnum] = keyon
                else:
                    # off -> off: do nothing
                    pass
            self.keyon[chnum] = keyon

        elif (0x09 <= aa <= 0x1f):
            pass

        elif (0x20 <= aa <= 0x27):
            # bit 7 R-ch enable
            # bit 6 L-ch enable
            # bit 2-0 connection
            chnum = aa - 0x20
            self.rch = dd & 0x80
            self.lch = dd & 0x40
            self.con = dd & 0x07
            funcs.dprint(state, "addr:{} LRch/Con aa:{} dd:{} chnum:{} rch:{} lch:{} con:{}".format(hex(addr), hex(aa), hex(dd), hex(chnum), hex(self.rch), hex(self.lch), hex(self.con)))

        elif (0x28 <= aa <= 0x2f):
            # bit 6-4 octave
            # bit 3-0 note (C#, D, D#, x, E, F, F#, x, G, G#, A, x, A#, B, C, x)
            chnum = aa - 0x28
            octave = (dd & 0x70) >> 4
            note = dd & 0x0f
            funcs.dprint(state, "addr:{} KeyCode aa:{} dd:{} chnum:{} octave:{} note:{}".format(hex(addr), hex(aa), hex(dd), hex(chnum), hex(octave), hex(note)))
            midinote = note2midinote(octave, note)
            self.midinote[chnum] = midinote

        elif (0x30 <= aa <= 0x37):
            # bit 7-2 key fraction
            chnum = aa - 0x30
            keyfrac = (dd & 0xfc) >> 2
            funcs.dprint(state, "addr:{} KeyFrac aa:{} dd:{} chnum:{} keyfrac:{}".format(hex(addr), hex(aa), hex(dd), hex(chnum), hex(keyfrac)))
        
        elif (0x38 <= aa <= 0x5f):
            pass

        elif (0x60 <= aa <= 0x7f):
            # total level
            chnum = (aa - 0x60) % 8
            opnum = (aa - 0x60) // 8
            # opnum: 0 -> 2 -> 1 -> 3
            if (opnum == 2):
                opnum = 1
            elif (opnum == 1):
                opnum = 2
            tl = dd & 0x7f

            funcs.dprint(state, "addr:{} TL aa:{} dd:{} chnum:{} opnum:{} tl:{}".format(hex(addr), hex(aa), hex(dd), hex(chnum), hex(opnum), hex(tl)))

        elif (0x80 <= aa <= 0xff):
            pass

        else:
            print("addr:{} NotImplemented aa:{} dd:{}".format(hex(addr), hex(aa), hex(dd)))

    def exportMidi(self):
        self.mid.save('new_song.mid')


def note2midinote(octave, note):
    # YM2151 440Hz: Oct=4 Note=10
    # YM2151 note: C#, D, D#, x, E, F, F#, x, G, G#, A, x, A#, B, C, x
    # MIDI 440Hz: A4(GM), noteno #69
    n1 = note // 4
    n2 = note % 4
    n = n1 * 3 + n2
    if (n > 0x0b):
        octave += 1
    midinote = (octave + 1) * 12 + (n + 1)
    #print("octave:{} note:{} midinote:{}".format(hex(octave), hex(note), midinote))
    return(midinote)


def main():
    pass

if __name__ == "__main__":
    main()
