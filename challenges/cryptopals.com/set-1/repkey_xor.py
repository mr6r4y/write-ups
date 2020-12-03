#!/usr/bin/env python3

import click
from base64 import b64decode
from reh.crypto.basic import repkey_xor


@click.command()
@click.argument("encrypted-file", type=click.Path())
@click.argument("key")
def main(encrypted_file, key):
    with open(encrypted_file, "r") as ef:
        encrypted = b64decode("".join([line.strip() for line in ef]))

    plain = repkey_xor(encrypted, key.encode("ascii"))

    print(plain.decode("ascii"))


if __name__ == "__main__":
    main()