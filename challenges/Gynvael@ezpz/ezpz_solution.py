#!/usr/bin/env python

import argparse

import string
import r2pipe as r2p
import hashlib


__all__ = []


HASHES_V_ADDR = 0x004030e0


def get_dyn_hashes_loc(r2ob):
    CHECK_V_ADDR = 0x00402ca5  # In VerifyPassword function: check letter hashes
    je_patch_v_addr = 0x00402cb7
    je_patch_slot = 0x402cc2

    cm = "db 0x%x" % CHECK_V_ADDR
    print "Command: %s" % cm
    r2ob.cmd(cm)

    cm = "s 0x%x; wa jmp 0x%x" % (je_patch_v_addr, je_patch_slot)
    print "Command: %s" % cm
    r2ob.cmd(cm)

    cm = "dc"
    print "Command: %s" % cm
    r2ob.cmd(cm)

    for i in range(0x14):
        cm = "drj"
        print "Command: %s" % cm
        regs = r2ob.cmdj(cm)

        yield regs["rcx"]

        cm = "dc"
        print "Command: %s" % cm
        r2ob.cmd(cm)

    cm = "drj"
    print "Command: %s" % cm
    regs = r2ob.cmdj(cm)

    yield regs["rcx"]


def get_hashes(r2ob, hash_loc):
    for j in range(0x15):
        cm = "p8j 0x10 @ 0x%x + 0x%x" % (hash_loc, j * 0x10)
        print "Command: %s" % cm
        h = "".join([("%02x" % i) for i in r2ob.cmdj(cm)])
        yield h


def get_hash(r2ob, hash_loc):
    cm = "p8j 0x10 @ 0x%x" % (hash_loc)
    print "Command: %s" % cm
    h = "".join([("%02x" % i) for i in r2ob.cmdj(cm)])
    return h


def md5(a):
    h = hashlib.md5()
    h.update(a)
    return h.hexdigest()


def bf_hash(h, prep):
    l = string.printable[:95]
    for i in l:
        if md5(prep + i) == h:
            return i

    return "?"


def get_args():
    parser = argparse.ArgumentParser(description=("Solve 'ezpz' challenge by Gynvael "
                                                  "- https://www.youtube.com/watch?v=JExnV1-GNxk ."
                                                  "Use in 'r2 -d' with '#!pipe ezpz_solution.py' "
                                                  "to solve it dynamically"))
    parser.add_argument("-f", "--file",
                        help="Path to file for analysis (static solving)")

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    if args.file:
        e = r2p.open(args.file)
        hashes_loc = HASHES_V_ADDR

        hs = [i for i in get_hashes(e, hashes_loc)]

        flag = []

        print ""
        print "Hashes:"
        print "--------------"
        for i in hs:
            print i
            s = bf_hash(i, "".join(flag))
            flag.append(s)
        print "--------------"

        print ""
        print "Flag:"
        print "--------------"
        print "".join(flag)
        print "--------------"
    else:
        e = r2p.open()
        hashes_loc = get_dyn_hashes_loc(e)

        hs = []
        for hash_loc in hashes_loc:
            hs.append(get_hash(e, hash_loc))

            print ""
            print "Hashes location: 0x%x" % hash_loc

        flag = []

        print ""
        print "Hashes:"
        print "--------------"
        for i in hs:
            print i
            s = bf_hash(i, "".join(flag))
            flag.append(s)
        print "--------------"

        print ""
        print "Flag:"
        print "--------------"
        print "".join(flag)
        print "--------------"


if __name__ == "__main__":
    main()
