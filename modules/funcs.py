#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def isVGM(vgmdata):
    if (vgmdata[0:4].decode('utf-8') != "Vgm "):
        return False

    return True


def getVgmVer(vgmdata):
    vgmVer = hex(int.from_bytes(vgmdata[8:11], byteorder = "little"))
    return vgmVer


def usage(scrname):
    # Usage
    print("Usage:{} [-d] filename".format(scrname))


def dprint(state, msg):
    # for debug print
    if state.getDebug():
        print(msg)


def main():
    pass


if __name__ == "__main__":
    main()
