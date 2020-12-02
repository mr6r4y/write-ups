#!/usr/bin/env python3

import os
import base64
from pprint import pprint
from reh.crypto.basic import XORKeyBreak


SCRIPT_PATH = os.path.dirname(__file__)


def main():
    ciphered = base64.b64decode(open(os.path.join(SCRIPT_PATH, "data", "6.txt"), "r").read().replace("\n", ""))
    xb = XORKeyBreak(ciphered)
    pprint(xb.run())


if __name__ == "__main__":
    main()
