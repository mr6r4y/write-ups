#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from __future__ import print_function
from pwn import *
import os
from time import sleep

import random


SCRIPT_PATH = os.path.dirname(__file__)


def main():
    gdb_break_script = "\n".join([
        "commands",
            "dereference $rdi l1",  # 64bit
            # "dereference $ebp+0x8 l1",  # 32bit
            "continue",
        "end",
    ])

    gdb_script = "\n".join([
       "gef config context.enable False",
        "break *(main+0x41b)",  # end of main 64bit
        # "break *0x08048bdb",  # end of main 32bit
        "break fast_memcpy",
        gdb_break_script,
        "continue"
    ])

    s = gdb.debug(["./memcpy"], gdbscript=gdb_script)
    # s = process(["strace", "./memcpy"])
    # s = process(["./memcpy"])

    print(s.clean())

    # s.write("{:d}\n".format(random.randint(2**3, 2**4)))
    # s.write("{:d}\n".format(random.randint(2**4, 2**5)))
    # s.write("{:d}\n".format(random.randint(2**5, 2**6)))
    # s.write("{:d}\n".format(random.randint(2**6, 2**7)))
    # s.write("{:d}\n".format(random.randint(2**7, 2**8)))
    # s.write("{:d}\n".format(random.randint(2**8, 2**9)))
    # s.write("{:d}\n".format(random.randint(2**9, 2**10)))
    # s.write("{:d}\n".format(random.randint(2**10, 2**11)))
    # s.write("{:d}\n".format(random.randint(2**11, 2**12)))
    # s.write("{:d}\n".format(random.randint(2**12, 2**13)))

    s.write("{:d}\n".format(8))
    s.write("{:d}\n".format(16))
    s.write("{:d}\n".format(32))
    s.write("{:d}\n".format(64))
    s.write("{:d}\n".format(128 + 0x10))
    s.write("{:d}\n".format(256 + 0x10))
    s.write("{:d}\n".format(512 + 0x10))
    s.write("{:d}\n".format(1024 + 0x10))
    s.write("{:d}\n".format(2048 + 0x10))
    s.write("{:d}\n".format(4096 + 0x10))

    s.interactive()
    # print(s.recvall())


if __name__ == '__main__':
    main()
