#Print addresses of complicated references in a challenge executable
#
#The code:
#
#     v1 = (ulong)*(uint *)(ntdll_DllBase + 0x88 + (long)*(int *)(ntdll_DllBase + 0x3c));
#
#     v2 = (ulong)*(uint *)(ntdll_DllBase + 0x18 + v1);
#
#     v3 = (char *)((ulong)*(uint *)(*(uint *)(ntdll_DllBase + 0x20 + v1) + ntdll_DllBase + v2 * 4) + ntdll_DllBase + 2);
#
#      *pdVar2 = *(dword *)(ntdll_DllBase + 4 +
#                     (ulong)*(uint *)(*(uint *)(ntdll_DllBase + 0x1c + v1) +
#                                      ntdll_DllBase + (ulong)*(ushort *) (*(uint *)(ntdll_DllBase + 0x24 + v1) + ntdll_DllBase + v2 * 2) * 4));
#
#@author mr6r4y
#@category -Restart-Service-
#@keybinding
#@menupath
#@toolbar


import struct
from binascii import unhexlify
from homies.fnvhash import fnv1_32, fnv1a_32
from ghidra.util.exception import CancelledException
from ghidra.program.model.mem import MemoryAccessException
from ghidra.program.flatapi import FlatProgramAPI


class AddressExplorer(object):
    def __init__(self, currentProgram):
        self.p = currentProgram
        self.a = FlatProgramAPI(self.p)
        self.image_base_offset = self.p.getAddressMap().imageBase.getOffset()

    def image_directory_entry_export_addr(self):
        offs1 = self.a.getInt(self.a.toAddr(self.image_base_offset + 0x3c))
        return self.a.toAddr(self.image_base_offset + 0x88 + offs1)

    def image_directory_entry_export(self):
        return self.a.getInt(self.image_directory_entry_export_addr())

    def export_number_of_names_addr(self):
        return self.a.toAddr(self.image_base_offset + 0x18 + self.image_directory_entry_export())

    def export_number_of_names(self):
        return self.a.getInt(self.export_number_of_names_addr())

    def address_of_names(self):
        return self.a.toAddr(self.image_base_offset + 0x20 + self.image_directory_entry_export())

    def address_of_names_offset(self):
        return self.a.getInt(self.address_of_names())

    def v3_addr(self):
        offs1_addr = self.address_of_names()
        print("v3_addr:offs1_addr = AddressOfNames Offset Address = %s" % offs1_addr)
        offs1 = self.address_of_names_offset()
        print("v3_addr:offs1 = AddressOfNames Offset = 0x%x" % offs1)
        print("v3_addr:offs1 = AddressOfNames Address = %s" % self.a.toAddr(self.image_base_offset + offs1))
        offs2_addr = self.a.toAddr(self.image_base_offset + (self.export_number_of_names() - 1) * 4 + offs1)
        print("v3_addr:offs2_addr = %s" % offs2_addr)
        offs2 = self.a.getInt(offs2_addr)
        print("v3_addr:offs2 = 0x%x" % offs2)
        return self.a.toAddr(self.image_base_offset + 2 + offs2)

    def get_dll_name(self):
        return self.a.getDataAt(self.a.toAddr(self.a.getInt(self.a.toAddr(self.image_base_offset + 0x0c + self.image_directory_entry_export())) + self.image_base_offset))

    def name_iter(self):
        number_of_names = self.export_number_of_names()
        address_of_names_offset = self.address_of_names_offset()
        while number_of_names >= 0:
            number_of_names -= 1
            next_name_addr_offset = self.a.getInt(self.a.toAddr(self.image_base_offset + number_of_names * 4 + address_of_names_offset))
            yield self.a.getDataAt(self.a.toAddr(self.image_base_offset + next_name_addr_offset))

    def address_of_name_ordinals_offset(self):
        return self.a.getInt(self.a.toAddr(self.image_base_offset + 0x24 + self.image_directory_entry_export()))

    def address_of_functions_offset(self):
        return self.a.getInt(self.a.toAddr(self.image_base_offset + 0x1c + self.image_directory_entry_export()))

    def func_addr_iter(self):
        number_of_names = self.export_number_of_names()
        address_of_name_ordinals_offset = self.address_of_name_ordinals_offset()
        address_of_functions_offset = self.address_of_functions_offset()
        while number_of_names >= 0:
            number_of_names -= 1
            next_ordinal_addr_offset = self.a.getShort(self.a.toAddr(self.image_base_offset + number_of_names * 2 + address_of_name_ordinals_offset))
            next_func_offset = self.a.getInt(self.a.toAddr(self.image_base_offset + address_of_functions_offset + next_ordinal_addr_offset * 4))
            yield self.a.toAddr(self.image_base_offset + next_func_offset)


def main():
    a = AddressExplorer(currentProgram)
    print("v1_addr = IMAGE_DIRECTORY_ENTRY_EXPORT Offset Address = %s" % a.image_directory_entry_export_addr())
    print("v1 = IMAGE_DIRECTORY_ENTRY_EXPORT Offset = 0x%x" % a.image_directory_entry_export())
    print("v2_addr = IMAGE_DIRECTORY_ENTRY_EXPORT.NumberOfNames Address = %s" % a.export_number_of_names_addr())
    print("v2 = IMAGE_DIRECTORY_ENTRY_EXPORT.NumberOfNames = 0x%x" % a.export_number_of_names())
    print("v3_addr = Name = %s" % a.v3_addr())

    print("address_of_name_ordinals_offset = 0x%x" % a.address_of_name_ordinals_offset())
    print("address_of_functions_offset = 0x%x" % a.address_of_functions_offset())

    print("dll_name = %s" % a.get_dll_name())


if __name__ == "__main__":
    main()