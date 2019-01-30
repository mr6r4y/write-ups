#!/usr/bin/env python3

import importlib
sbxor = importlib.import_module('03-single-byte-xor')


def main():
    with open("4.txt", "r") as txt:
        for n, line in enumerate(txt):
            a = sbxor.xor_1byte(line.strip())
            if a:
                print("{:d} : {:s} -> {:s}".format(n + 1, line.strip(), a.strip()))


if __name__ == '__main__':
    main()
