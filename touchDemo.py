#!/usr/bin/env python3

import os

import board
# import digitalio
# import pyftdi
from pyftdi.ftdi import Ftdi


def main():
    # ftdi://[vendor][:[product][:serial|:bus:address|:index]]/interface
    # something = Ftdi().open_from_url("ftdi:///?")
    # print(dir(Ftdi()))
    # print(Ftdi().open_from_url("ftdi:///?").device_version())
    # print(os.environ["BLINKA_FT232H"])
    something = Ftdi()
    something.open_from_url("ftdi://0x0403:0x6014:MT0000/1")
    # something.open_from_url("ftdi://0x0403:0x6014/1")
    print(dir(something))
    something_else = Ftdi()
    something_else.open_from_url("ftdi://0x0403:0x6014:MB0000/1")
    print(something_else)

    # everything = Ftdi.find_all([(0x0403, 0x6014)])
    # for thing in everything:
    #     print(thing)
    #     thing = thing[0]
    #     print(dir(thing))
    #     print(thing.bitbang_enabled)

if __name__ == '__main__':
    main()
    # import fire
    # fire.Fire()
