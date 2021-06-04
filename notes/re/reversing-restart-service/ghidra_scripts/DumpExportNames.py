#Dump exporrt names to a file
#@author mr6r4y
#@category -Restart-Service-
#@keybinding
#@menupath
#@toolbar


import struct
from binascii import unhexlify
import json
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

    for func_name, func_addr in zip(a.name_iter(), a.func_addr_iter()):
        func = getFunctionAt(func_addr)
        func_name_orig = func.getName() if func else None
        names.append({"name": "%s" % func_name.getValue() if func_name else None, "orig-name": "%s" % func_name_orig})

    json.dump(names, open(str(json_fl), "w"), sort_keys=True, indent=2)


if __name__ == "__main__":
    main()