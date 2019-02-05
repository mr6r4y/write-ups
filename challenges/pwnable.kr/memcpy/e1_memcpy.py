#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from __future__ import print_function
from pwn import *
import os


SCRIPT_PATH = os.path.dirname(__file__)


def make_inititial_set():
    return [
        "{:d}\n".format(random.randint(2**3, 2**4)),
        "{:d}\n".format(random.randint(2**4, 2**5)),
        "{:d}\n".format(random.randint(2**5, 2**6)),
        "{:d}\n".format(random.randint(2**6, 2**7)),
        "{:d}\n".format(random.randint(2**7, 2**8)),
        "{:d}\n".format(random.randint(2**8, 2**9)),
        "{:d}\n".format(random.randint(2**9, 2**10)),
        "{:d}\n".format(random.randint(2**10, 2**11)),
        "{:d}\n".format(random.randint(2**11, 2**12)),
        "{:d}\n".format(random.randint(2**12, 2**13))
    ]


def main():
    initial_set = make_inititial_set()

    # Found that this finishes the 5th test and stops at 6th
    better_set = ["{:d}\n".format(10),
                  "{:d}\n".format(18),
                  "{:d}\n".format(62),
                  "{:d}\n".format(88),
                  "{:d}\n".format(189)]

    i = len(better_set)

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

        initial_set = make_inititial_set()

    print(out)

if __name__ == '__main__':
    main()
