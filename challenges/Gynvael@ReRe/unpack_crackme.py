#!/usr/bin/env python

import sys
from ctypes import c_byte
import types

# Look at https://github.com/mr6r4y/re-misc/blob/master/dispy.py
import relib.dispy as dispy

from rere import crackme


def get_size(obj):
    prev_line = None
    for line in filter(lambda a: a[1] != 'JUMP_FORWARD', dispy.dis(obj)):
        if line[1] == "STORE_FAST"\
                and line[5] is not None\
                and line[5][0] == "CO_VARNAMES"\
                and line[5][1] == "sz"\
                and prev_line is not None\
                and prev_line[1] == "LOAD_CONST"\
                and prev_line[5] is not None\
                and prev_line[5][0] == "CO_CONSTS":
            return prev_line[5][1]
        prev_line = line


def unpack_func(sz, obj):
    c = obj.func_code.co_code
    off = sys.getsizeof('') - 1
    ptr = (c_byte * len(c)).from_address(id(c) + off)
    key = map(ord, c[3:16])

    i = 0
    while i < sz:
        ptr[i + 16] ^= key[(i % 13)]
        i += 1


CRACKME_UNPACKED_FLG = False


class UnpackCrackme(object):
    def __init__(self):
        pass

    def unpack(self):
        # Use this cause we are changing imported object
        global CRACKME_UNPACKED_FLG

        sz = get_size(crackme)

        if not CRACKME_UNPACKED_FLG:
            unpack_func(sz, crackme)
            CRACKME_UNPACKED_FLG = True

        flg = False
        for line in filter(lambda a: a[1] != 'JUMP_FORWARD', dispy.dis(crackme, 16, sz + 16)):
            if line[1] == "CALL_FUNCTION" and line[2] == 1 and flg:
                flg = False
                continue
            if line[5] is not None and line[5][0] == "CO_NAMES" and line[5][1] == "_":
                flg = True
                continue
            if line[5] is not None\
                    and line[5][0] == "CO_CONSTS"\
                    and isinstance(line[5][1], str)\
                    and not line[5][1].startswith('q'):
                try:
                    yield tuple([((j[0], j[1][::-1].decode("zlib")) if isinstance(j, tuple) else j)
                                 for j in line])
                except Exception:
                    yield line
            else:
                yield line

    def obf_func_btc(self):
        def match_STORE_GLOBAL(l):
            return (l[1] == "STORE_GLOBAL" and
                    l[5] is not None and
                    l[5][0] == "CO_NAMES")

        def match_LOAD_GLOBAL_types(l):
            return (l[1] == "LOAD_GLOBAL" and
                    l[5] is not None and
                    l[5][0] == "CO_NAMES" and
                    l[5][1] == "types")

        record_func = False
        f = []
        f_name = None
        for i in self.unpack():
            if match_LOAD_GLOBAL_types(i):
                record_func = True
            if record_func:
                f.append(i)
            if match_STORE_GLOBAL(i):
                f_name = i[5][1]

                yield (f_name, f)

                record_func = False
                f = []
                f_name = None

    def build_func_data(self, func_btc):
        f_name, btc = func_btc
        s = SimplePythonInterp(btc)
        dt = s.stack()[-1]

        return {"name": f_name, "obj": dt}

    def funcs(self):
        for i in self.obf_func_btc():
            yield self.build_func_data(i)


class SimplePythonInterp(object):
    def __init__(self, btc):
        self.btc = btc
        self._stack = []
        self._consume_btc(btc)

    def match_LOAD_CONST(self, l):
        return (l[1] == "LOAD_CONST" and
                l[5] is not None and
                l[5][0] == "CO_CONSTS")

    def match_BUILD_TUPLE(self, l):
        return (l[1] == "BUILD_TUPLE")

    def match_LOAD_GLOBAL(self, l):
        return (l[1] == "LOAD_GLOBAL" and
                l[5] is not None and
                l[5][0] == "CO_NAMES")

    def match_LOAD_ATTR(self, l):
        return (l[1] == "LOAD_ATTR" and
                l[5] is not None and
                l[5][0] == "CO_NAMES")

    def match_CALL_FUNCTION(self, l):
        return (l[1] == "CALL_FUNCTION")

    def match_STORE_GLOBAL(self, l):
        return (l[1] == "STORE_GLOBAL" and
                l[5] is not None and
                l[5][0] == "CO_NAMES")

    def op_LOAD_CONST(self, value):
        self._stack.append(value)

    def op_BUILD_TUPLE(self, len):
        t = []
        for i in range(len):
            t.append(self._stack.pop())
        self._stack.append(tuple(reversed(t)))

    def op_LOAD_GLOBAL(self, name):
        self._stack.append(eval(name))

    def op_LOAD_ATTR(self, attr):
        a = self._stack.pop()
        self._stack.append(a.__dict__[attr])

    # Maintains only positional arguments
    def op_CALL_FUNCTION(self, argc):
        args = []
        for i in range(argc):
            args.append(self._stack.pop())
        f = self._stack.pop()
        self._stack.append(f(*reversed(args)))

    def op_STORE_GLOBAL(self, name):
        pass

    def _consume_btc(self, btc):
        for l in btc:
            if self.match_LOAD_CONST(l):
                self.op_LOAD_CONST(l[5][1])
            elif self.match_BUILD_TUPLE(l):
                self.op_BUILD_TUPLE(l[2])
            elif self.match_LOAD_GLOBAL(l):
                self.op_LOAD_GLOBAL(l[5][1])
            elif self.match_LOAD_ATTR(l):
                self.op_LOAD_ATTR(l[5][1])
            elif self.match_CALL_FUNCTION(l):
                self.op_CALL_FUNCTION(l[2])
            elif self.match_STORE_GLOBAL(l):
                self.op_STORE_GLOBAL(l[5][1])

    def stack(self):
        return self._stack


def main():
    u = UnpackCrackme()

    with open("rere_crackme.btc", "w") as f:
        for i in u.unpack():
            f.write(str(i) + "\n")

    for j in u.funcs():
        print j["name"]
        print "=" * 80
        sz = get_size(j["obj"])
        unpack_func(sz, j["obj"])
        for line in filter(lambda a: a[1] != 'JUMP_FORWARD', dispy.dis(j["obj"], 16, sz + 16)):
            if (line[1] == "LOAD_CONST" and
                    line[5] is not None and
                    line[5][0] == "CO_CONSTS" and
                    isinstance(line[5][1], types.CodeType)):
                print "-" * 60
                for ll in dispy.dis(line[5][1]):
                    print ll
                print "-" * 60
            print line
        print "=" * 80
        print "\n"


if __name__ == '__main__':
    main()
