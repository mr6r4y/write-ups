# `memcpy` Solution

# Assignment

    Are you tired of hacking?, take some rest here.
    Just help me out with my small experiment regarding memcpy performance. 
    after that, flag is yours.

    http://pwnable.kr/bin/memcpy.c

    ssh memcpy@pwnable.kr -p2222 (pw:guest)

    the compiled binary of "memcpy.c" source code (with real flag) will be executed under memcpy_pwn privilege if you connect to port 9022.
    execute the binary by connecting to daemon(nc 0 9022).

# Charters

## 1

Semantics of `__asm__` and `__volatile__` in GCC

## 2 ✓

Read about symbol table and how to find functions defined locally in the executable via GDB.

### Notes

`(gdb) maint info sections` - Gives info about exe's ELF sections

`(gdb) info address symbol`

`(gdb) info symbol addr`:

    (gdb) info symbol 0x54320
    _initialize_vx + 396 in section .text

`(gdb) info scope location`

`$ rabin2 -s ./memcpy` - List symbols in the executable only

## 3 ✓

Could not understand conditions of `printf` buffering so I tried to write a script that makes random suggestions. Could not reproduce cut-the-stdout behaviour locally.

## ~3.1~

Reproduce the program behaviour locally.

### Notes

- [x] ~Try automated interaction to look more like real one - use `s.recv` and `s.sendline`~
- [x] Read [pwntools docs][17]

At the end I could not reproduce this locally. Probably due to newer version of GCC.

## ~3.1.1~

Make pwntools' `process` behave and receive every line during program communication. Currently lines like:

    specify the memcpy amount between 8 ~ 16 :

are printed on `recvall` and I want to take them before every `sendline`.

## 3.2 ✓

Research problems in Linux concerning buffering of `stdout`.

### Notes

- [x] Artiicle for [stdout buffering][1]

## 4 ✓

Seek tips from Google

### Notes

- [x] [memcpy hints][20]
- [x] [MOVNTPS][21]
- [ ] [Alignment in C][22]

## 5 ✓

Try to debug the app and break on `fast_memcpy`'s fist instruction from `__asm__` block.

### Notes

Show heap chunks after completing the 10 experiments:

    gef➤  heap chunks
    Chunk(addr=0x2443010, size=0x250, flags=PREV_INUSE)
        [0x0000000002443010     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
    Chunk(addr=0x2443260, size=0x410, flags=PREV_INUSE)
        [0x0000000002443260     65 6c 6c 61 70 73 65 64 20 43 50 55 20 63 79 63    ellapsed CPU cyc]
    Chunk(addr=0x2443670, size=0x1010, flags=PREV_INUSE)
        [0x0000000002443670     38 0a 31 36 0a 33 32 0a 36 34 0a 31 34 34 0a 32    8.16.32.64.144.2]
    Chunk(addr=0x2444680, size=0x20, flags=PREV_INUSE)
        [0x0000000002444680     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
    Chunk(addr=0x24446a0, size=0x20, flags=PREV_INUSE)
        [0x00000000024446a0     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
    Chunk(addr=0x24446c0, size=0x30, flags=PREV_INUSE)
        [0x00000000024446c0     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
    Chunk(addr=0x24446f0, size=0x50, flags=PREV_INUSE)
        [0x00000000024446f0     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
    Chunk(addr=0x2444740, size=0xa0, flags=PREV_INUSE)
        [0x0000000002444740     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
    Chunk(addr=0x24447e0, size=0x120, flags=PREV_INUSE)
        [0x00000000024447e0     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
    Chunk(addr=0x2444900, size=0x220, flags=PREV_INUSE)
        [0x0000000002444900     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
    Chunk(addr=0x2444b20, size=0x420, flags=PREV_INUSE)
        [0x0000000002444b20     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
    Chunk(addr=0x2444f40, size=0x820, flags=PREV_INUSE)
        [0x0000000002444f40     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
    Chunk(addr=0x2445760, size=0x1020, flags=PREV_INUSE)
        [0x0000000002445760     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................]
    Chunk(addr=0x2446780, size=0x1d890, flags=PREV_INUSE)  ←  top chunk

## 5.1 ✓

Try to compile the app as 32 bit ELF

### Notes

Still cannot reproduce program halt but in a comment in `memcpy.c` I see:

    // compiled with : gcc -o memcpy memcpy.c -m32 -lm

The needed package for Ubuntu to be able to compile 32bit:

    sudo apt-get install gcc-multilib


## 5.1.1

Fix the Gef's `heap chunks` when working with 32bit ELF.

## 5.1.2

Gef's `capstone-disassemble` does not work for the `fast_memcpy` for 32bit ELF:

    gef➤  cs fast_memcpy
           0x8048747 <fast_memcpy+0>  push   ebp
           0x8048748 <fast_memcpy+1>  mov    ebp, esp
           0x804874a <fast_memcpy+3>  sub    esp, 0x10
     →     0x804874d <fast_memcpy+6>  call   0x8048bdc
    [!] Command 'capstone-disassemble' failed to execute properly, reason: unsupported operand type(s) for +: 'bool' and 'str'

## 5.2

Make such `malloc` allocation that every `address % 16 == 0`. Mind the `0x10` (x86-64) additional storage for chunk pointers.

## 5.2.1

Make GDB script to print at `fast_memcpy` `dest` address.

### Notes

It seems every address is aligned at `0x10`, even on 32 bit ELF:

    0xfff1ffe0│+0x0000: 0x09a9b170  →  0x00000000

    Breakpoint 2, 0x0804874d in fast_memcpy ()
    0xfff1ffe0│+0x0000: 0x09a9b180  →  0x00000000

    Breakpoint 2, 0x0804874d in fast_memcpy ()
    0xfff1ffe0│+0x0000: 0x09a9b1a0  →  0x00000000

    Breakpoint 2, 0x0804874d in fast_memcpy ()
    0xfff1ffe0│+0x0000: 0x09a9b1d0  →  0x00000000

    Breakpoint 2, 0x0804874d in fast_memcpy ()
    0xfff1ffe0│+0x0000: 0x09a9b220  →  0x00000000

    Breakpoint 2, 0x0804874d in fast_memcpy ()
    0xfff1ffe0│+0x0000: 0x09a9b2c0  →  0x00000000

    Breakpoint 2, 0x0804874d in fast_memcpy ()
    0xfff1ffe0│+0x0000: 0x09a9b3e0  →  0x00000000

    Breakpoint 2, 0x0804874d in fast_memcpy ()
    0xfff1ffe0│+0x0000: 0x09a9b600  →  0x00000000

    Breakpoint 2, 0x0804874d in fast_memcpy ()
    0xfff1ffe0│+0x0000: 0x09a9ba20  →  0x00000000

    Breakpoint 2, 0x0804874d in fast_memcpy ()
    0xfff1ffe0│+0x0000: 0x09a9c240  →  0x00000000

For 64 bit ELF:

    0x0000000002103270│+0x0000: 0x0000000000000000   ← $rax, $rdi

    Breakpoint 2, 0x0000000000400961 in fast_memcpy ()
    0x0000000002103290│+0x0000: 0x0000000000000000   ← $rax, $rdi

    Breakpoint 2, 0x0000000000400961 in fast_memcpy ()
    0x00000000021032b0│+0x0000: 0x0000000000000000   ← $rax, $rdi

    Breakpoint 2, 0x0000000000400961 in fast_memcpy ()
    0x00000000021032e0│+0x0000: 0x0000000000000000   ← $rax, $rdi

    Breakpoint 2, 0x0000000000400961 in fast_memcpy ()
    0x0000000002103330│+0x0000: 0x0000000000000000   ← $rax, $rdi

    Breakpoint 2, 0x0000000000400961 in fast_memcpy ()
    0x00000000021033d0│+0x0000: 0x0000000000000000   ← $rax, $rdi

    Breakpoint 2, 0x0000000000400961 in fast_memcpy ()
    0x00000000021034f0│+0x0000: 0x0000000000000000   ← $rax, $rdi

    Breakpoint 2, 0x0000000000400961 in fast_memcpy ()
    0x0000000002103710│+0x0000: 0x0000000000000000   ← $rax, $rdi

    Breakpoint 2, 0x0000000000400961 in fast_memcpy ()
    0x0000000002103b30│+0x0000: 0x0000000000000000   ← $rax, $rdi

    Breakpoint 2, 0x0000000000400961 in fast_memcpy ()
    0x0000000002104350│+0x0000: 0x0000000000000000   ← $rax, $rdi


# References

## Compilation

- [x] [Undefined Reference to pow()][1]
- [x] [Make GCC not to compile with PIE][2]
- [x] [Compile 32bit apps on 64bit Ubuntu][23]

## GDB

- [x] [GDB List all functions][3]
- [x] [GDB - Symbols][4]
- [ ] [GDB - Files][5]
- [ ] [GDB - Variables][6]

## Pwntools

- [x] [Tubes][17]

## C

- [x] [setvbuf][7]
- [ ] [mmap][8]
- [x] [C Programming: setvbuf][9]
- [x] [Stdout Buffering][10]
- [ ] [SOF: Why does printf not flush after the call unless a newline is in the format string?][16]
- [ ] [Unix Buffering][18]
- [x] [dup2][19]

## Inline Assembly in GCC

- [ ] [GCC Inline Assembly HOWTO][11]
- [ ] [Brennan's Guide to Inline Assembly][12]
- [ ] [`__asm__` and `__volatile__`][13]
- [ ] [Inside Linux: Inline Assembly][14]

## x86 Instructions

- [x] [RDTSC][15]

## Hints

- [ ] [memcpy hints][20]
- [x] [MOVNTPS][21]
- [ ] [Alignment in C][22]


[1]: https://stackoverflow.com/questions/12824134/undefined-reference-to-pow-in-c-despite-including-math-h
[2]: https://stackoverflow.com/questions/49101265/how-to-configure-gcc-to-use-no-pie-by-default
[3]: https://stackoverflow.com/questions/10680670/ask-gdb-to-list-all-functions-in-a-program
[4]: https://sourceware.org/gdb/onlinedocs/gdb/Symbols.html
[5]: https://sourceware.org/gdb/onlinedocs/gdb/Files.html
[6]: https://sourceware.org/gdb/onlinedocs/gdb/Variables.html
[7]: https://linux.die.net/man/3/setvbuf
[8]: https://linux.die.net/man/3/mmap
[9]: https://en.wikibooks.org/wiki/C_Programming/stdio.h/setvbuf
[10]: https://eklitzke.org/stdout-buffering
[11]: https://www.ibiblio.org/gferg/ldp/GCC-Inline-Assembly-HOWTO.html
[12]: http://www.delorie.com/djgpp/doc/brennan/brennan_att_inline_djgpp.html "Brennan's Guide to Inline Assembly"
[13]: https://stackoverflow.com/questions/26456510/what-does-asm-volatile-do-in-c
[14]: https://0xax.gitbooks.io/linux-insides/content/Theory/linux-theory-3.html "Inside Linux: Inline Assembly"
[15]: https://c9x.me/x86/html/file_module_x86_id_278.html "RDTSC"
[16]: https://stackoverflow.com/questions/1716296/why-does-printf-not-flush-after-the-call-unless-a-newline-is-in-the-format-strin/1716621
[17]: http://docs.pwntools.com/en/stable/tubes.html
[18]: https://www.turnkeylinux.org/blog/unix-buffering
[19]: http://man7.org/linux/man-pages/man2/dup.2.html
[20]: https://github.com/Macmod/pwnable-writeups
[21]: https://www.felixcloutier.com/x86/movntps
[22]: https://wr.informatik.uni-hamburg.de/_media/teaching/wintersemester_2013_2014/epc-14-haase-svenhendrik-alignmentinc-paper.pdf
[23]: https://stackoverflow.com/questions/22355436/how-to-compile-32-bit-apps-on-64-bit-ubuntu