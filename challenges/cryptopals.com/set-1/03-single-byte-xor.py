#!/usr/bin/env python3

import pwn
from functools import reduce
import enchant
import string


def xor_1byte(enc):
    def _truth_ratio(a):
        b = map(lambda x: 1 if x else 0, a)
        return reduce(lambda x, y: x + y, b, 0) / len(a)

    e1 = bytes.fromhex(enc)
    spell_checker = enchant.Dict("en_US")

    v = []

    for bt in range(256):
        e2 = bytes([bt] * len(e1))
        p = pwn.xor(e1, e2)

        words = p.split(b" ")

        # Words are divided by spaces
        if len(words) < 2:
            continue

        # Plain text must contain only printable characters
        legit = True
        for i in words:
            for j in i:
                if j not in string.printable.encode("ascii"):
                    legit = False
        if not legit:
            continue

        # Spell check every word and take a True ratio
        v.append((_truth_ratio([(spell_checker.check(i.decode("ascii").lower()) if i else False) for i in words]), p))

    if v:
        vv = sorted(v, key=lambda x: x[0], reverse=True)[0]

        if vv[0] > 0.1:
            return vv[1].decode("ascii")

    return None


def main():
    encrypted = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    plain = xor_1byte(encrypted)

    print(plain)


if __name__ == '__main__':
    main()
