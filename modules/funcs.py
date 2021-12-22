#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def isVGM(vgmdata):
    if (vgmdata[0:4].decode('utf-8') != "Vgm "):
        return False

    return True


def getVgmVer(vgmdata):
    vgmVer = hex(int.from_bytes(vgmdata[8:11], byteorder = "little"))
    return vgmVer


def ymtl2exp(conn, tl1, tl2, tl3, tl4):
    if (0 <= conn <= 3):
        exp = 127 - tl4
    elif ( conn == 4):
        exp = 127 - ((tl2 + tl3) / 2)
    elif (5 <= conn <= 6):
        exp = 127 - ((tl2 + tl3 + tl4) / 3)
    elif (conn == 7):
        exp = 127 - ((tl1 + tl2 + tl3 + tl4) / 4)
    else:
        exp = 100
    return(exp)


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
