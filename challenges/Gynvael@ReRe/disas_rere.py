#!/usr/bin/env python

import sys
from ctypes import c_byte

# Look at https://github.com/mr6r4y/re-misc/blob/master/dispy.py
import relib.dispy as dispy

from rere import _, crackme


print "Function: _"
print "=" * 80
for line in filter(lambda a: a[1] != 'JUMP_FORWARD', dispy.dis(_)):
    print line
print "=" * 80

print "Function: crackme"
print "=" * 80
for line in filter(lambda a: a[1] != 'JUMP_FORWARD', dispy.dis(crackme)):
    print line
print "=" * 80

c = _.func_code.co_code
off = sys.getsizeof('') - 1
ptr = (c_byte * len(c)).from_address(id(c) + off)
key = map(ord, c[3:16])

sz = 250
i = 0
while i < sz:
    ptr[i + 16] ^= key[(i % 13)]
    i += 1
print "Function: _(payload)"
print "=" * 80
for line in filter(lambda a: a[1] != 'JUMP_FORWARD', dispy.dis(_, 16, 250+16)):
    print line


c = crackme.func_code.co_code
off = sys.getsizeof('') - 1
ptr = (c_byte * len(c)).from_address(id(c) + off)
key = map(ord, c[3:16])

sz = 44633
i = 0
while i < sz:
    ptr[i + 16] ^= key[(i % 13)]
    i += 1
print "Function: crackme (payload)"
print "=" * 80
flg = False
for line in filter(lambda a: a[1] != 'JUMP_FORWARD', dispy.dis(crackme, 16, 44633 + 16)):
    if line[1] == "CALL_FUNCTION" and line[2] == 1 and flg:
        flg = False
        continue
    if line[5] is not None and line[5][0] == "CO_NAMES" and line[5][1] == "_":
        flg = True
        continue
    if line[5] is not None and line[5][0] == "CO_CONSTS" and isinstance(line[5][1], str) and not line[5][1].startswith('q'):
        try:
            print [((i[0], i[1][::-1].decode("zlib")) if isinstance(i, tuple) else i) for i in line]
        except Exception:
            print line
    else:
        print line
