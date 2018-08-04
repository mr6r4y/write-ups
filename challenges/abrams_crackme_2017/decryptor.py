#!/usr/bin/env python2

from pwn import *
import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Custom unpacker for abrams_crackme_2017")
    parser.add_argument("-i", "--in-file", help="File to unpack")
    parser.add_argument("-o", "--out-file", help="Output file")

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    PAYLOAD_VA = 0x400570
    PAYLOAD_LEN = 0x2d2
    KEY = 0xc
    XOR_INSTR_VA = 0x4009e7

    open(args.in_file)

    e = ELF(args.in_file)

    log.info("Read payload: 0x%x bytes at 0x%x" % (PAYLOAD_LEN, PAYLOAD_VA))
    payload = e.read(PAYLOAD_VA, PAYLOAD_LEN)

    log.info("XORing with 0x%x" % KEY)
    payload_decr = xor(payload, KEY)

    log.info("Write back the decrypted payload")
    e.write(PAYLOAD_VA, payload_decr)

    log.info("NOPing the XOR at 0x%x" % XOR_INSTR_VA)
    e.write(XOR_INSTR_VA, "\x90" * 5)

    e.save(args.out_file)


if __name__ == '__main__':
    main()
