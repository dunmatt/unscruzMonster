#!/usr/bin/env python3
import sys

def checksum(all_bytes):
    # Why any of this?  Shut up, that's why.
    checksum = 0xAAAA
    for i in range(0x7F):
        value = all_bytes[i * 2]
        value += all_bytes[i * 2 + 1] << 8
        checksum = value ^ checksum
        checksum = ((checksum << 1) & 0xFFFF) | (checksum >> 15)
        # print(hex(value), hex(checksum))
    return checksum


def main(filename):
    with open(filename, mode="rb+") as f:
        contents = bytearray(f.read1())
        contents[0x1C] = 0x67
        chksm = checksum(contents)
        contents[-2] = chksm & 0xFF
        contents[-1] = chksm >> 8
        f.seek(0)
        f.write(contents)


if __name__ == '__main__':
    main(sys.argv[-1])
