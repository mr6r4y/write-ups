#!/usr/bin/env python3

import importlib
fxor = importlib.import_module('02-fixed-xor')


def main():
    inputs = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    inputs_hex = bytes.hex("Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal".encode("ascii"))
    output_hex = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    key = "ICE"
    long_key = (key * (len(inputs) // len(key) + 1))[:len(inputs)]

    my_cypher = fxor.xor(inputs_hex, bytes.hex(long_key.encode("ascii")))

    print("my_cypher = {:s}".format(my_cypher))
    print("output    = {:s}".format(output_hex))
    assert my_cypher == output_hex


if __name__ == '__main__':
    main()
