# Seek for __guard in .dynsym section
s 0x6e0
w0 24
# Seek for __stack_smash_handler in .dynsym section
s 0x710
w0 24
# Patch ptrace check / debugger check
s 0xd33
wa jmp 0xd51