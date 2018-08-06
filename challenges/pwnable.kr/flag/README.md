# `flag` Solution

From the first run I get the hint:

    I will malloc() and strcpy the flag there. take it.

So the flag will appear in memory on the heap at some time.
The executable is packed and is a mess. My laziest plan is to:
catch all `syscalls`:

    gdb ./flag

    pwndbg> info files     # does not work
    pwndbg> shell rabin2 -e ./flag
    Warning: Cannot initialize section headers
    Warning: Cannot initialize strings table
    Warning: Cannot initialize dynamic strings
    [Entrypoints]
    vaddr=0x0044a4f0 paddr=0x0004a4f0 baddr=0x00400000 laddr=0x00000000 haddr=0x00000018 type=program

    pwndbg> catch syscall     # catch them all

    pwndbg> continue
    ...
    pwndbg> continue
    ...

`continue` until `exit_group` found. Then dump the memory:

    pwndbg> vmmap
    LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
              0x400000           0x4c2000 r-xp    c2000 0
              0x4c2000           0x6c1000 ---p   1ff000 0
              0x6c1000           0x6ea000 rwxp    29000 0      [heap]
              0x800000           0x801000 rwxp     1000 0
        0x7ffff7ffa000     0x7ffff7ffb000 rwxp     1000 0
        0x7ffff7ffb000     0x7ffff7ffd000 r--p     2000 0      [vvar]
        0x7ffff7ffd000     0x7ffff7fff000 r-xp     2000 0      [vdso]
        0x7ffffffde000     0x7ffffffff000 rwxp    21000 0      [stack]
    0xffffffffff600000 0xffffffffff601000 r-xp     1000 0      [vsyscall]

    pwndbg> dump binary memory c.bin 0x6c1000 0x6ea000

    pwndbg> shell strings c.bin
    UPX...? sounds like a delivery service :)


# TO-DO

* automate recognition of packers (yara rules that work)
* manually unpack with gdb/r2
