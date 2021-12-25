#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import gzip

from modules import convState, funcs
from modules import vgmMain as v
from modules import convState


def main(argv):
    # status data(debug flag, etc...)
    state = convState.convState()

    scrname = os.path.basename(argv[0])
    if (len(argv) == 2):
        filename = argv[1]
    elif (len(argv) == 3):
        if (argv[1] == '-d'):
            state.setDebug(True)
            filename = argv[2]
        else:
            funcs.usage(scrname)
            return(1)
    else:
        funcs.usage(scrname)
        return(1)

    if (not os.path.isfile(filename)):
        print("File not found: {}".format(filename))
        return(1)
    
    midifilebase = os.path.splitext(filename)[0]

    # read vgm data from file
    try:
        # try open file as gzipped file(.vgz)
        with gzip.open(filename, mode="rb") as g:
            vgmdata = g.read()
            #print(vgmdata)
    except gzip.BadGzipFile as e:
        # open file as .vgm file
        with open(filename, mode="rb") as f:
            vgmdata = f.read()
            #print(vgmdata)

    if (not funcs.isVGM(vgmdata)):
        print("File format error: {}".format(filename))
        return(1)

    v.convert(state, vgmdata, midifilebase)

    return (0)


if (__name__ == '__main__'):
    sys.exit(main(sys.argv))
