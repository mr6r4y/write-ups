#!/usr/bin/env python

import json
import re
import struct
import binascii
from z3 import *


TABLE = [
    BitVecVal(0x56, 64),
    BitVecVal(0x6f, 64),
    BitVecVal(0x6c, 64),
    BitVecVal(0x67, 64),
    BitVecVal(0x61, 64),
    BitVecVal(0x43, 64),
    BitVecVal(0x54, 64),
    BitVecVal(0x46, 64),
    BitVecVal(0x7b, 64),
]

TABLE = TABLE + [BitVec("x_%i" % i, 64) for i in range(9, 44)] + [BitVecVal(0x7d, 64)]

# TABLE = [BitVec("x_%i" % i, 64) for i in range(45)]

rax = None
rbx = None
rcx = None
rdx = None
rsi = None
rdi = None
r8 = None
r9 = None
r10 = None
r11 = None
r12 = None
r13 = None
r14 = TABLE


def reset():
    global rax, rbx, rcx, rdx, rsi, rdi, r8, r9, r10, r11, r12, r13, r14
    rax = None
    rbx = None
    rcx = None
    rdx = None
    rsi = None
    rdi = None
    r8 = None
    r9 = None
    r10 = None
    r11 = None
    r12 = None
    r13 = None
    r14 = TABLE


def asm_mov(a1, a2):
    return "%s = %s" % (a1, a2)


def asm_lea(a1, a2):
    return "%s = %s" % (a1, a2)


def asm_shl(a1, a2):
    return "%s = %s << %s" % (a1, a1, a2)


def asm_add(a1, a2):
    if a2.startswith("0x"):
        a2 = "BitVecVal(%s, 64)" % a2
    return "%s = %s + %s" % (a1, a1, a2)


def asm_sub(a1, a2):
    if a2.startswith("0x"):
        a2 = "BitVecVal(%s, 64)" % a2
    return "%s = %s - %s" % (a1, a1, a2)


def asm_imul(a1, a2, a3=None):
    if a3 is None:
        if a2.startswith("0x"):
            a2 = "BitVecVal(%s, 64)" % a2
        return "%s = %s * %s" % (a1, a1, a2)
    else:
        if a3.startswith("0xffff"):
            a3 = str(struct.unpack(">q", binascii.unhexlify(a3[2:]))[0])
            a3 = "BitVecVal(%s, 64)" % a3
        return "%s = %s * %s" % (a1, a2, a3)


def asm_neg(a1):
    return "%s = -%s" % (a1, a1)


def asm_cmp(a1, a2):
    if a2.startswith("0xffff"):
        a2 = str(struct.unpack(">q", binascii.unhexlify(a2[2:]))[0])
    return "%s == BitVecVal(%s, 64)" % (a1, a2)


def parse_assembly(s):
    def _get_instr(s):
        ins = re.search("^[a-z]+", s).group()
        return ins

    def _get_args(s):
        raw_args = re.search("^[a-z]+ (.*)", s).group(1)
        raw_args = [i.strip() for i in raw_args.split(",")]

        args_expr = []
        for a in raw_args:
            if a in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi",
                     "r8", "r9", "r10", "r11", "r12", "r13", "r14"]:
                args_expr.append(a)
            else:
                r = re.search("^qword \\[(.+)\\]$", a)
                if r:
                    r = r.group(1)
                    r = [i.strip() for i in r.split("+")]
                    if len(r) == 1:
                        if r[0] == "r14":
                            args_expr.append("%s" % r[0])
                        else:
                            args_expr.append("%s[0]" % r[0])
                    else:
                        r1, r2 = r
                        try:
                            e = int(r2) / 8
                        except ValueError:
                            e = int(r2, 16) / 8
                        args_expr.append("%s[%i]" % (r1, e))
                else:
                    args_expr.append(a)

        return args_expr

    ins = _get_instr(s)
    args = _get_args(s)

    instructions = {
        "mov": asm_mov,
        "lea": asm_lea,
        "shl": asm_shl,
        "add": asm_add,
        "sub": asm_sub,
        "imul": asm_imul,
        "neg": asm_neg,
        "cmp": asm_cmp
    }

    c = instructions[ins](*args)
    return ins, c


def eval_block(b):
    global rax, rbx, rcx, rdx, rsi, rdi, r8, r9, r10, r11, r12, r13, r14
    for i in b:
        ins, c = parse_assembly(i)
        if ins == "cmp":
            print c
            return eval(c)
        else:
            print c
            exec c


def main():
    allasm = json.load(open("all-asm.json", "r"))

    constraints = []
    for n, b in enumerate(allasm):
        print "Block No: %i" % n
        print "="*40
        c = eval_block(b)
        constraints.append(c)
        reset()
        print "-"*40

    print solve(*constraints)


if __name__ == '__main__':
    main()
