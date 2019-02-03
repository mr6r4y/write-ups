#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from __future__ import print_function
from pwn import *
import os

import random


SCRIPT_PATH = os.path.dirname(__file__)


def main():
    gdb_script = "\n".join([
        "break *(main+0x41b)",  # end of main
        "continue"
    ])

    s = gdb.debug(["./memcpy"], gdbscript=gdb_script)
    # s = process(["./memcpy"])

    s.sendline("{:d}\n".format(random.randint(8, 16)))
    s.sendline("{:d}\n".format(random.randint(16, 32)))
    s.sendline("{:d}\n".format(random.randint(32, 64)))
    s.sendline("{:d}\n".format(random.randint(64, 128)))
    s.sendline("{:d}\n".format(random.randint(128, 256)))
    s.sendline("{:d}\n".format(random.randint(256, 512)))
    s.sendline("{:d}\n".format(random.randint(512, 1024)))
    s.sendline("{:d}\n".format(random.randint(1024, 2048)))
    s.sendline("{:d}\n".format(random.randint(2048, 4096)))
    s.sendline("{:d}\n".format(random.randint(4096, 4096 * 2)))

    print(s.recvall())


if __name__ == '__main__':
    main()
