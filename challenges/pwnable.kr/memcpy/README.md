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


# References

## Compilation

- https://stackoverflow.com/questions/12824134/undefined-reference-to-pow-in-c-despite-including-math-h
- https://stackoverflow.com/questions/49101265/how-to-configure-gcc-to-use-no-pie-by-default

## GDB

- https://stackoverflow.com/questions/10680670/ask-gdb-to-list-all-functions-in-a-program
- https://sourceware.org/gdb/onlinedocs/gdb/Symbols.html

## Inline Assembly in GCC

- https://www.ibiblio.org/gferg/ldp/GCC-Inline-Assembly-HOWTO.html
- http://www.delorie.com/djgpp/doc/brennan/brennan_att_inline_djgpp.html
- https://stackoverflow.com/questions/26456510/what-does-asm-volatile-do-in-c
- https://0xax.gitbooks.io/linux-insides/content/Theory/linux-theory-3.html

## x86 Instructions

- https://c9x.me/x86/html/file_module_x86_id_278.html