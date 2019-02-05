#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from __future__ import print_function
from pwn import *
import os


SCRIPT_PATH = os.path.dirname(__file__)


def make_inititial_set(offset):
    return [
        "{:d}\n".format(2**3 + offset),
        "{:d}\n".format(2**4 + offset),
        "{:d}\n".format(2**5 + offset),
        "{:d}\n".format(2**6 + offset),
        "{:d}\n".format(2**7 + offset),
        "{:d}\n".format(2**8 + offset),
        "{:d}\n".format(2**9 + offset),
        "{:d}\n".format(2**10 + offset),
        "{:d}\n".format(2**11 + offset),
        "{:d}\n".format(2**12 + offset)
    ]


def main():
    initial_set = make_inititial_set(0)

    # Found that this finishes the 5th test and stops at 6th
    better_set = ["{:d}\n".format(8),
                  "{:d}\n".format(16),
                  "{:d}\n".format(32),
                  "{:d}\n".format(88),
                  "{:d}\n".format(128 + 0x8),
                  "{:d}\n".format(256 + 0x8),
                  "{:d}\n".format(512 + 0x8)]

    i = len(better_set)

    offset = 4

    old_out = None
    while i < 10:
        s = process(["nc", "0", "9022"])

        for j in range(10):
            if j < len(better_set):
                s.sendline(better_set[j])
            else:
                s.sendline(initial_set[j])

        out = s.recvall()

        if old_out is None:
            old_out = out

        print(out)

        if len(out) > len(old_out) + 38:
            old_out = out
            better_set.append(initial_set[i])
            i += 1

        initial_set = make_inititial_set(offset)
        offset += 4

    print(out)

if __name__ == '__main__':
    main()
