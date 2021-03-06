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
        self.midiFileName = ''
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
        self.expression = [0] * self.chs    # expression

        self.mid = MidiFile()
        self.mid.type = 1
        # track 0: conductor track
        # track 1-: data track
        self.track = [0] * (self.chs + 1)

        # conductor track
        self.track[0] = MidiTrack()
        self.mid.tracks.append(self.track[0])
        self.track[0].append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(state.getMidiTempo()), time = 0))

        # data track
        for i in range(self.chs):
            self.track[i + 1] = MidiTrack()
            self.mid.tracks.append(self.track[i + 1])
            m.initMidiTrack(self.track[i + 1], i)
            trackname = self.chipname + ' CH' + str(i + 1)
            m.setMidiTrackname(self.track[i + 1], trackname)

        #self.mid.save('new_song.mid')

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
                        m.noteOn(self.track[chnum + 1], chnum, self.midinote[chnum], self.expression[chnum], tick - self.lastmiditick[chnum])
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
                        m.noteOff(self.track[chnum + 1], chnum, self.lastmidinote[chnum], self.expression[chnum], tick - self.lastmiditick[chnum])
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
            self.rch[chnum] = dd & 0x80
            self.lch[chnum] = dd & 0x40
            self.con[chnum] = dd & 0x07
            funcs.dprint(state, "addr:{} LRch/Con aa:{} dd:{} chnum:{} rch:{} lch:{} con:{}".format(hex(addr), hex(aa), hex(dd), hex(chnum), hex(self.rch[chnum]), hex(self.lch[chnum]), hex(self.con[chnum])))

            # midi panpot:(L)0-64-127(R)
            # YM2151: lch rch    midi panpot
            #          1   0       0
            #          1   1      64
            #          0   1     127
            if (self.rch[chnum]):
                panpot = 127
            else:
                panpot = 64
            
            if (self.lch[chnum]):
                panpot -= 63
            else:
                panpot -= 0

            if (state.getSamples() < 1):
                # sample # < 1 ... initial process. ignore
                pass
            else:
                m.panSet(self.track[chnum + 1], chnum, panpot)

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
            self.tls[chnum][opnum] = dd & 0x7f
            self.expression[chnum] = funcs.ymtl2exp(self.con[chnum], self.tls[chnum][0], self.tls[chnum][1], self.tls[chnum][2], self.tls[chnum][3])
            funcs.dprint(state, "addr:{} TL aa:{} dd:{} chnum:{} opnum:{}".format(hex(addr), hex(aa), hex(dd), hex(chnum), hex(opnum)))

        elif (0x80 <= aa <= 0xff):
            pass

        else:
            print("addr:{} NotImplemented aa:{} dd:{}".format(hex(addr), hex(aa), hex(dd)))


    def getMidiFileName(self):
        return self.midifilebase + '_' + self.chipname + '.mid'


    def setMidiFileName(self, midifilebase):
        self.midifilebase = midifilebase


    def exportMidi(self):
        self.mid.save(self.getMidiFileName())


def note2midinote(octave, note):
    # YM2151 440Hz: Oct=4 Note=10
    # YM2151 note: C#, D, D#, x, E, F, F#, x, G, G#, A, x, A#, B, C, x
    # MIDI 440Hz: A4(GM), noteno #69
    n1 = note // 4
    n2 = note % 4
    midinote = (octave + 1) * 12 + (n + 1)
    #print("octave:{} note:{} midinote:{}".format(hex(octave), hex(note), midinote))
    return(midinote)


def main():
    pass

if __name__ == "__main__":
    main()
