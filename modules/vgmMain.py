#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import vgmHeader as h
#from . import convState
from . import classYM2151

def main():
    pass


def convert(state, vgmdata, midifilebase):
    objYM2151 = None

    # read VGM header
    vgmheader = {}
    vgmheader = h.read(vgmdata)
    #print(vgmheader)

    # read VGM data
    addr = vgmheader.get('VGM data offset') + 0x34
    while True:
        vgmcmd = vgmdata[addr]

        if (vgmcmd == 0x61):
            # Wait n samples
            nn1 = vgmdata[addr + 1]
            nn2 = vgmdata[addr + 2]
            addr += 3
            state.addSamples(nn2 * 256 + nn1)
        elif (vgmcmd == 0x62):
            # wait 735 samples
            addr += 1
            state.addSamples(735)
        elif (vgmcmd == 0x63):
            # wait 882 samples
            addr += 1
            state.addSamples(882)
        elif (vgmcmd == 0x66):
            # end of sound data
            addr += 1
            break
            #print("vgmcmd:{} aa:{} dd:{}".format(hex(vgmcmd), hex(aa), hex(dd)))
        elif (0x70 <= vgmcmd <= 0x7F):
            # wait n+1 samples, n can range from 0 to 15.
            addr += 1
            state.addSamples(vgmcmd - 0x70 + 1)
        elif (vgmcmd == 0x54):
            if (objYM2151 is None):
                objYM2151 = classYM2151.YM2151(state)
                objYM2151.setMidiFileName(midifilebase)
            # YM2151, write value dd to register aa
            aa = vgmdata[addr + 1]
            dd = vgmdata[addr + 2]
            addr += 3
            objYM2151.update(state, addr, aa, dd)
            #print("vgmcmd:{} aa:{} dd:{}".format(hex(vgmcmd), hex(aa), hex(dd)))
        else:
            print("Not implemented: addr:{} vgmcmd:{}".format(hex(addr), hex(vgmcmd)))
            addr += 1
        
        if addr > vgmheader.get('Eof offset'):
            break

        if (addr > 20000):
            #break
            pass

        objYM2151.exportMidi()
    return True


if __name__ == "__main__":
    main()
