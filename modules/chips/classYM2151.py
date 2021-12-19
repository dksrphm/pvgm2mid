#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class YM2151:
    def __init__(self):
        self.chipname = 'YM2151'
        self.chs = 8    # max channels
        self.con = [0] * self.chs   # connection algorithm
        self.tls = [[0] * 4] * self.chs     # total levels [ch][op]
        self.keyon = [0] * self.chs
        self.note = [0] * self.chs
        self.octave = [0] * self.chs
        self.lch = [0] * self.chs   # left channel
        self.rch = [0] * self.chs   # right channel

    def update(self, addr, aa, dd):
        if (0x00 <= aa <= 0x07):
            pass

        elif (aa == 0x08):
            # bit 6-3:KeyOn/Off op4-op1
            # bit 2-0:channel num
            chnum = dd & 0x07
            keyon = dd & 0x78
            if (keyon != 0):
                print("addr:{} KeyOn aa:{} dd:{} chnum:{} keyon:{}".format(hex(addr), hex(aa), hex(dd), hex(chnum), hex(keyon)))
            else:
                print("addr:{} KeyOff aa:{} dd:{} chnum:{} keyon:{}".format(hex(addr), hex(aa), hex(dd), hex(chnum), hex(keyon)))
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
            print("addr:{} LRch/Con aa:{} dd:{} chnum:{} rch:{} lch:{} con:{}".format(hex(addr), hex(aa), hex(dd), hex(chnum), hex(self.rch), hex(self.lch), hex(self.con)))

        elif (0x28 <= aa <= 0x2f):
            # bit 6-4 octave
            # bit 3-0 note
            chnum = aa - 0x28
            octave = (dd & 0x70) >> 4
            note = dd & 0x0f
            print("addr:{} KeyCode aa:{} dd:{} chnum:{} octave:{} note:{}".format(hex(addr), hex(aa), hex(dd), hex(chnum), hex(octave), hex(note)))

        elif (0x30 <= aa <= 0x37):
            # bit 7-2 key fraction
            chnum = aa - 0x30
            keyfrac = (dd & 0xfc) >> 2
            print("addr:{} KeyFrac aa:{} dd:{} chnum:{} keyfrac:{}".format(hex(addr), hex(aa), hex(dd), hex(chnum), hex(keyfrac)))
        
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

            print("addr:{} TL aa:{} dd:{} chnum:{} opnum:{} tl:{}".format(hex(addr), hex(aa), hex(dd), hex(chnum), hex(opnum), hex(tl)))

        elif (0x80 <= aa <= 0xff):
            pass

        else:
            print("addr:{} NotImplemented aa:{} dd:{}".format(hex(addr), hex(aa), hex(dd)))


def main():
    pass

if __name__ == "__main__":
    main()
