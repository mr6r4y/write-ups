#!/usr/bin/env python3


import os
from binascii import unhexlify, hexlify

from reh.crypto.basic import is_aes_ecb_128

SCRIPT_PATH = os.path.dirname(__file__)

def main():
    encrypted_file = os.path.join(SCRIPT_PATH, "data", "8.txt")
    with open(encrypted_file, "r") as ef:
        encrypted_list = [unhexlify(line.strip()) for line in ef]

    for n, enc in enumerate(encrypted_list, start=1):
        if is_aes_ecb_128(enc):
            print("Line: %i, content: %s" % (n, hexlify(enc).decode("ascii")))


if __name__ == "__main__":
    main()
