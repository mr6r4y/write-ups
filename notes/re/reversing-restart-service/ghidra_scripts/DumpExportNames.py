#Dump exporrt names to a file
#@author mr6r4y
#@category -Restart-Service-
#@keybinding
#@menupath
#@toolbar


import struct
from binascii import unhexlify
from homies.fnvhash import fnv1_32, fnv1a_32
from ShowNtdllAddresses import AddressExplorer
from ghidra.util.exception import CancelledException
from ghidra.program.model.mem import MemoryAccessException


def main():
    try:
        json_fl = askFile("File to save results in", "Save")
    except CancelledException:
        return

    a = AddressExplorer(currentProgram)

    names = []
    dll_name = a.get_dll_name()
    dll_name = dll_name.getValue() if dll_name is not None else ""

    for func_name, func_addr in zip(a.name_iter(), a.func_addr_iter()):
        func = getFunctionAt(func_addr)
        func_name_orig = func.getName() if func else None
        # names.append({"name": "%s" % func_name.getValue() if func_name else None, "orig-name": "%s" % func_name_orig})
        fn = func_name.getValue() if func_name else (func_name_orig if func_name_orig is not None else "")
        names.append(dll_name + ":" + fn)

    with open(str(json_fl), "a") as fl:
        fl.write("\n".join(names))


if __name__ == "__main__":
    main()