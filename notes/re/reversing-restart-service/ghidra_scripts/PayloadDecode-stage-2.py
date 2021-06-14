#Stage-2 patch and decode payload
#
#Decode routine:
#
#  MOV R11B,0x4a
#  MOV RCX,0x6c4d
#  LEA R8,[0x401968]
#LAB_00401968:
#  XOR byte ptr [R8 + RCX*0x1 + 0xb],R11B
#  ADD R11B,byte ptr [R8 + RCX*0x1 + 0xb]
#  LOOP LAB_00401968
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


def toByte(a):
    return BigInteger("%i" % a).byteValue()


def main():
    from_addr = toAddr(0x00401974)
    payload_len = 0x6c4d
    key = toByte(0x4a)

    m = currentProgram.getMemory()
    t = ProgramTransaction.open(currentProgram, "Patching payload code - stage-2")

    for i in reversed(range(payload_len)):
        current_addr = toAddr(from_addr.getOffset() + i)
        a = getByte(current_addr)
        c = toByte(a ^ key)
        m.setByte(current_addr, c)
        key = toByte(key + c)

    t.commit()
    t.close()


if __name__ == "__main__":
    main()