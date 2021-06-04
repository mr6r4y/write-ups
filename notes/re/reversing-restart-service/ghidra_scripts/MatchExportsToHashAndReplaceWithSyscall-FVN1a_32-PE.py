#Match export function name FVN1a_32 hash in a shared library (Windows PE) against a list of hashes and replace them with appropriate syscall at memory
#@author mr6r4y
#@category -Restart-Service-
#@keybinding
#@menupath
#@toolbar


import struct
from binascii import unhexlify
from homies.fnvhash import fnv1_32, fnv1a_32
from ShowNtdllAddresses import AddressExplorer
from ghidra.program.flatapi import FlatProgramAPI
from ghidra.util.exception import CancelledException
from ghidra.program.model.mem import MemoryAccessException
from ghidra.program.database.util import ProgramTransaction


def main():
    try:
        rs_program = askProgram("Choose the restart-service.exe executable")
        ntdll_program = askProgram("Choose the ntdll.dll shared library")
    except CancelledException:
        return

    hashes = [
        0x3944AA7E,
        0x7EA69E72,
        0xDBA7A248,
        0x57FF1EA4,
        0x71948CA4,
    ]

    rs_api = FlatProgramAPI(rs_program)

    addresses = {
        0x3944AA7E: rs_api.toAddr(0x004ab004),
        0x7EA69E72: rs_api.toAddr(0x004ab008),
        0xDBA7A248: rs_api.toAddr(0x004ab00c),
        0x57FF1EA4: rs_api.toAddr(0x004ab010),
        0x71948CA4: rs_api.toAddr(0x004ab014),
    }

    a = AddressExplorer(ntdll_program)
    m = rs_program.getMemory()
    t = ProgramTransaction.open(rs_program, "Writing matched syscall IDs")

    for func_name, func_addr in zip(a.name_iter(), a.func_addr_iter()):
        func = getFunctionAt(func_addr)
        func_name_orig = func.getName() if func else None
        try:
            syscall_dword = getInt(toAddr(func_addr.getOffset() + 4))
        except MemoryAccessException:
            syscall_dword = None
        s = fnv1a_32(func_name.getBytes()[2:-1]) if func_name else 0x0
        s_orig = fnv1a_32([ord(i) for i in func_name_orig[2:]]) if func_name_orig else 0x0



        if (s in hashes) and func_name and func_name.getValue().startswith("Nt") and syscall_dword is not None:
            print("name: %s, name_orig: %s, func_addr: %s, syscall: %s, s: 0x%X, s_orig: 0x%X" % (func_name, func_name_orig, func_addr, syscall_dword, s, s_orig))
            print("Writing %s to 0x%X" % (addresses[s], syscall_dword))
            m.setInt(addresses[s], syscall_dword)

    t.commit()
    t.close()


if __name__ == "__main__":
    main()