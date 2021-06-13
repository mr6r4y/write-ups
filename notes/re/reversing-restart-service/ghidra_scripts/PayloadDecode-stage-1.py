#Stage-1 patch and decode payload
#
#Decode routine:
#
#     POP R14
#     CMC
#     JMP LAB_004085c6
#     LAB_004085c6:
#     NOT dword ptr [R14]
#     JMP LAB_004085cb
#   LAB_004085cb:
#     SUB dword ptr [R14 + 0x4],0xd7e3a9db
#     ROR dword ptr [R14 + 0x8],0x2b
#     JMP LAB_004085da
#   LAB_004085da:
#     ADD dword ptr [R14 + 0xc],0xfaf545c1
#     JMP R14
#
#@author mr6r4y
#@category -Restart-Service-
#@keybinding
#@menupath
#@toolbar


import struct
from binascii import unhexlify
from ShowNtdllAddresses import AddressExplorer
from ghidra.program.flatapi import FlatProgramAPI
from ghidra.util.exception import CancelledException
from ghidra.program.model.mem import MemoryAccessException
from ghidra.program.database.util import ProgramTransaction
from java.math import BigInteger


def toInt(a):
    return BigInteger("%i" % a).intValue()


def NOT(a):
    return (~a) & (2**32-1)


def ROR(a, b):
    width = 32
    b = b % width
    return (a >> (b) | a << (width - (b))) & (2**32-1)


def SUB(a, b):
    return (a - b) & (2**32-1)


def ADD(a, b):
    return (a + b) & (2**32-1)


def main():
    return_addr = toAddr(0x00401957)

    m = currentProgram.getMemory()
    t = ProgramTransaction.open(currentProgram, "Patching payload code - stage-2")

    dw1 = long(getInt(return_addr)) & (2**32 - 1)
    dw2 = long(getInt(toAddr(return_addr.getOffset() + 4))) & (2**32 - 1)
    dw3 = long(getInt(toAddr(return_addr.getOffset() + 8))) & (2**32 - 1)
    dw4 = long(getInt(toAddr(return_addr.getOffset() + 12))) & (2**32 - 1)

    dwr1 = toInt(NOT(dw1))
    print("NOT(0x%x) = 0x%x" % (dw1, dwr1))
    dwr2 = toInt(SUB(dw2, 0xd7e3a9db))
    print("SUB(0x%x, 0xd7e3a9db) = 0x%x" % (dw2, dwr2))
    dwr3 = toInt(ROR(dw3, 0x2b))
    print("ROR(0x%x, 0x2b) = 0x%x" % (dw3, dwr3))
    dwr4 = toInt(ADD(dw4, 0xfaf545c1))
    print("ADD(0x%x, 0xfaf545c1) = 0x%x" % (dw4, dwr4))

    m.setInt(return_addr, dwr1)
    m.setInt(toAddr(return_addr.getOffset() + 4), dwr2)
    m.setInt(toAddr(return_addr.getOffset() + 8), dwr3)
    m.setInt(toAddr(return_addr.getOffset() + 12), dwr4)

    t.commit()
    t.close()


if __name__ == "__main__":
    main()