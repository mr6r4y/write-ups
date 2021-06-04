#!/usr/bin/env python3


import os
import sys
import click
import json
import fnv


@click.command()
@click.option("-f", "--json-file", required=True)
def main(json_file):
    hashes = [
        0x3944AA7E,
        0x7EA69E72,
        0xDBA7A248,
        0x57FF1EA4,
        0x71948CA4,
    ]

    names = json.load(open(json_file, "r"))
    for i in names:
        n = i["name"] if i["name"] != "None" else i["orig-name"]
        if n != "None" and n is not None:
            # s = fnv.hash(n[2:].encode("ascii") + b"\x00", algorithm=fnv.fnv_1a, bits=32)
            s1 = fnv.hash(n[2:].encode("ascii"), algorithm=fnv.fnv_1a, bits=32)
            if s1 in hashes:
                print("%s: 0x%X" % (n, s1))


if __name__ == "__main__":
    main()