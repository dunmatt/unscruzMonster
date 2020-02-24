#!/usr/bin/env python3

import os

# import board
# import digitalio
# import pyftdi
from pyftdi.ftdi import Ftdi


def main():
    # something = Ftdi.create_from_url("ftdi://0x0403:0x6014:MT0000/1")
    something = Ftdi()
    something.open_mpsse(0x0403, 0x6014, serial="MT0000", frequency=400_000)
    # TODO: enable MPSSE mode before uncommenting this line
    # something.set_frequency(400_000)
    something.enable_3phase_clock(True)
    print(something)
    # print(something.get_identifiers())
    print(dir(something.usb_dev))
    print((something.usb_dev.serial_number))
    print((something.usb_dev.product))
    print((something.usb_dev.manufacturer))


    # everything = Ftdi.find_all([(0x0403, 0x6014)])
    # for thing in everything:
    #     thing = thing[0]
    #     print(thing)
    #     print(dir(thing))
    #     print(thing.sn)
    # #     print(thing.bitbang_enabled)

if __name__ == '__main__':
    main()
    # import fire
    # fire.Fire()
