#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from __future__ import print_function
from pwn import *
import os


SCRIPT_PATH = os.path.dirname(__file__)


def main():
    initial = ["{:d}\n".format(random.randint(8, 16)),
               "{:d}\n".format(random.randint(16, 32)),
               "{:d}\n".format(random.randint(32, 64)),
               "{:d}\n".format(random.randint(64, 128)),
               "{:d}\n".format(random.randint(128, 256)),
               "{:d}\n".format(random.randint(256, 512)),
               "{:d}\n".format(random.randint(512, 1024)),
               "{:d}\n".format(random.randint(1024, 2048)),
               "{:d}\n".format(random.randint(2048, 4096)),
               "{:d}\n".format(random.randint(4096, 4096 * 2))]

    second = ["{:d}\n".format(10),
              "{:d}\n".format(18),
              "{:d}\n".format(62),
              "{:d}\n".format(88),
              "{:d}\n".format(189)]
    i = len(second)

    old_out = None
    while i < 10:
        s = process(["nc", "0", "9022"])

        for j in range(10):
            if j < len(second):
                s.sendline(second[j])
            else:
                s.sendline(initial[j])

        out = s.recvall()

        if old_out is None:
            old_out = out

        print(out)

        if len(out) > len(old_out) + 38:
            old_out = out
            second.append(initial[i])
            i += 1

        initial = ["{:d}\n".format(random.randint(8, 16)),
                   "{:d}\n".format(random.randint(16, 32)),
                   "{:d}\n".format(random.randint(32, 64)),
                   "{:d}\n".format(random.randint(64, 128)),
                   "{:d}\n".format(random.randint(128, 256)),
                   "{:d}\n".format(random.randint(256, 512)),
                   "{:d}\n".format(random.randint(512, 1024)),
                   "{:d}\n".format(random.randint(1024, 2048)),
                   "{:d}\n".format(random.randint(2048, 4096)),
                   "{:d}\n".format(random.randint(4096, 4096 * 2))]

    print(out)

if __name__ == '__main__':
    main()
