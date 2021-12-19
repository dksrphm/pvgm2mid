#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
    pass


def read(vgmdata):
    vgmheader = {}

    vgmheader['Eof offset']     = _readHeadData(vgmdata, 0x04, 4)
    #vgmheader['Version'] = hex(int.from_bytes(vgmdata[8:11], byteorder = "little"))
    vgmheader['Version']        = _readHeadData(vgmdata, 0x08, 4)
    vgmheader['SN76489 clock']  = _readHeadData(vgmdata, 0x0c, 4)
    vgmheader['YM2413 clock']   = _readHeadData(vgmdata, 0x10, 4)
    vgmheader['GD3 offset']     = _readHeadData(vgmdata, 0x14, 4)
    vgmheader['Total # samples']= _readHeadData(vgmdata, 0x18, 4)
    vgmheader['Loop offset']    = _readHeadData(vgmdata, 0x1c, 4)
    vgmheader['Loop # samples'] = _readHeadData(vgmdata, 0x20, 4)
    vgmheader['Rate']           = _readHeadData(vgmdata, 0x24, 4)
    vgmheader['SN FB']          = _readHeadData(vgmdata, 0x28, 2)
    vgmheader['SNW']            = _readHeadData(vgmdata, 0x2a, 1)
    vgmheader['SF']             = _readHeadData(vgmdata, 0x2b, 1)
    vgmheader['YM2612 clock']   = _readHeadData(vgmdata, 0x2c, 4)
    vgmheader['YM2151 clock']   = _readHeadData(vgmdata, 0x30, 4)
    vgmheader['VGM data offset']= _readHeadData(vgmdata, 0x34, 4)

    if (vgmheader['Version'] > 0x151):
        vgmheader['Sega PCM clock'] = _readHeadData(vgmdata, 0x38, 4)
        vgmheader['SPCM Interface'] = _readHeadData(vgmdata, 0x3c, 4)
    
    return(vgmheader)


def _readHeadData(vgmdata, start, bytes):
    return int.from_bytes(vgmdata[start:(start + bytes)], byteorder = "little")


if __name__ == "__main__":
    main()
