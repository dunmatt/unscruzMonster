#!/usr/bin/env python3

import os
import time

# import board
# import digitalio
# import pyftdi
# from pyftdi.ftdi import Ftdi
from pyftdi.i2c import I2cController, I2cIOError

BASE_ADDRESS = 0x5A

ACCR_ADDR = 0x7B  # (and 0x7C)
ECR_ADDR = 0x5E
OOR_ADDR = 0x02  # (and 0x03)
SRR_ADDR = 0x80
TSR_ADDR = 0x00  # (and 0x01)

USL_ADDR = 0x7D
USL_VALUE = 240
LSL_VALUE = int(USL_VALUE * 0.25)
TL_VALUE = int(USL_VALUE * 0.7)

ECR_ALL_SYSTEMS_STOP = 0x00
ECR_ALL_SYSTEMS_GO = 0xFF


def get_i2c_controller(id):
    i2c = I2cController()
    i2c.configure(f"ftdi://0x0403:0x6014:MT{id:04}/1")
    # TODO: consider fixing https://github.com/eblot/pyftdi/blob/master/pyftdi/i2c.py:459 and then
    #       using the below line instead of the above one... if we find it's too slow as is, that is
    # i2c.configure(f"ftdi://0x0403:0x6014:MT{id:04}/1", frequency=400_000)
    return i2c


def populate_auto_config_registers(port):
    # See https://cdn-shop.adafruit.com/datasheets/MPR121.pdf for an explanation of these magic bytes.
    port.write_to(ACCR_ADDR, b'\xB3\x00')


def populate_level_registers(port):
    bts = bytearray()
    bts.append(USL_VALUE)
    bts.append(LSL_VALUE)
    bts.append(TL_VALUE)
    port.write_to(USL_ADDR, bts)


def get_touch_sensor(i2c, addr):
    try:
        port = i2c.get_port(addr)
        port.write_to(SRR_ADDR, b'\x63')  # Soft resets the sensor chip, and verifies comm.
        time.sleep(0.1)  # gives it time to reset itself
        populate_level_registers(port)
        populate_auto_config_registers(port)
        time.sleep(0.1)  # gives it time to reconfigure itself (probably not required)
        port.write_to(ECR_ADDR, b'\xCF')  # Turns sensing on for all real channels.
        return port
    except I2cIOError as e:
        print(f"Error {e} while configuring {hex(addr)}@{i2c}")
        return None


def get_touch_sensors(i2c):
    # TODO: does the := below need parens?
    return (sensor for i in range(4) if (sensor := get_touch_sensor(i2c, BASE_ADDRESS + i)))


def read_sensor(sensor):
    return sensor.read_from(TSR_ADDR, 2)  # magic 2 is the number of bytes to read


def main():
    # # something = Ftdi.create_from_url("ftdi://0x0403:0x6014:MT0000/1")
    # something = Ftdi()
    # something.open_mpsse(0x0403, 0x6014, serial="MT0000", frequency=400_000)
    # # TODO: enable MPSSE mode before uncommenting this line
    # # something.set_frequency(400_000)
    # something.enable_3phase_clock(True)
    # print(something)
    # # print(something.get_identifiers())
    # print(dir(something.usb_dev))
    # print((something.usb_dev.serial_number))
    # print((something.usb_dev.product))
    # print((something.usb_dev.manufacturer))


    # everything = Ftdi.find_all([(0x0403, 0x6014)])
    # for thing in everything:
    #     thing = thing[0]
    #     print(thing)
    #     print(dir(thing))
    #     print(thing.sn)
    # #     print(thing.bitbang_enabled)

    i2c_controller = get_i2c_controller(0)
    sensors = list(get_touch_sensors(i2c_controller))
    while True:
        for sensor in sensors:
            reading = read_sensor(sensor)
            chan0 = sensor.read_from(0x04, 2)
            chan0 = int(chan0[1]) << 8 | chan0[0]
            b = sensor.read_from(0x1E, 1)[0]
            print(f"{reading[0] & 1}  {reading[0] & 2}    {chan0}    {b}")


if __name__ == '__main__':
    main()
    # import fire
    # fire.Fire()
