#!/usr/bin/python

import time
import sys
import serial

def _write_to_port(port, dirL, dirR, engL, engR):
    header = 0b01010000
    header |= dirL
    header |= dirR << 1
    port.write(chr(header))

    dataR = 0b00000000 | engR
    port.write(chr(dataR))

    dataL = 0b11000000 | engL
    port.write(chr(dataL))

def set_engines(dirL, dirR, engL, engR):
    print dirL, dirR, engL, engR

    portname = "/dev/ttyS0"
    port = serial.Serial(portname, 9600)

    if (
        dirL not in (0, 1) or
        dirR not in (0, 1) or
        engL < 0 or engL > 63 or
        engR < 0 or engR > 63
    ):
        raise Exception('not in range')
        return

    # SAFEGUARD
    engL = int(engL / 2)
    engR = int(engR / 2)

    _write_to_port(port, dirL, dirR, engL, engR)
    port.close()

def main():
    if len(sys.argv) != 5:
        print ("Usage: ./engines.py dirL dirR powL powR \n"
        "Where: dir = (0, 1), pow = (0..100) inclusive \n\n"
        "Or: import module and call set_engines(dirL dirR powL powR) \n"
        "Where: dir = (0, 1), pow = (0..63) inclusive \n")
        return

    dirL, dirR, engL, engR = sys.argv[1:]
    dirL = int(dirL)
    dirR = int(dirR)
    engL = int(int(engL) / 100.0 * 63)
    engR = int(int(engR) / 100.0 * 63)

    set_engines(dirL, dirR, engL, engR)

if __name__ == "__main__":
    main()