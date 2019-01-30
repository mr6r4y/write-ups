#!/usr/bin/env python3

import pwn


def xor(s1, s2):
    b1, b2 = bytes.fromhex(s1), bytes.fromhex(s2)
    l = min((len(b1), len(b2)))
    return bytes.hex(pwn.xor(b1[:l], b2[:l]))


def main():
    inputs = ("1c0111001f010100061a024b53535009181c",
              "686974207468652062756c6c277320657965")
    output = "746865206b696420646f6e277420706c6179"

    my_out = xor(inputs[0], inputs[1])

    print("{:s} == {:s}".format(my_out, output))
    assert my_out == output

if __name__ == '__main__':
    main()
