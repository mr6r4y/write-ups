#!/usr/bin/env python3


import os
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

SCRIPT_PATH = os.path.dirname(__file__)

def main():
    encrypted_file = os.path.join(SCRIPT_PATH, "data", "7.txt")
    with open(encrypted_file, "r") as ef:
        encrypted = b64decode("".join([line.strip() for line in ef]))

    cipher = Cipher(algorithm=algorithms.AES(key=b"YELLOW SUBMARINE"), mode=modes.ECB())
    decryptor = cipher.decryptor()
    plain = decryptor.update(encrypted)

    print(plain.decode("ascii"))


if __name__ == "__main__":
    main()
