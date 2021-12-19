#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
    pass


def isVGM(vgmdata):
    if (vgmdata[0:4].decode('utf-8') != "Vgm "):
        return False

    return True


def getVgmVer(vgmdata):
    vgmVer = hex(int.from_bytes(vgmdata[8:11], byteorder = "little"))
    return vgmVer


if __name__ == "__main__":
    main()
