# `asm`

# Assignment

    Mommy! I think I know how to make shellcodes

    ssh asm@pwnable.kr -p2222 (pw: guest)


Readme:

    once you connect to port 9026, the "asm" binary will be executed under asm_pwn privilege.
    make connection to challenge (nc 0 9026) then get the flag. (file name of the flag is same as the one in this directory)

`ls -al`:

    drwxr-x---  5 root asm   4096 Jan  2  2017 .
    drwxr-xr-x 93 root root  4096 Oct 10 22:56 ..
    d---------  2 root root  4096 Nov 19  2016 .bash_history
    dr-xr-xr-x  2 root root  4096 Nov 25  2016 .irssi
    drwxr-xr-x  2 root root  4096 Jan  2  2017 .pwntools-cache
    -rwxr-xr-x  1 root root 13704 Nov 29  2016 asm
    -rw-r--r--  1 root root  1793 Nov 29  2016 asm.c
    -rw-r--r--  1 root root   211 Nov 19  2016 readme
    -rw-r--r--  1 root root    67 Nov 19  2016 this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong

# Charters

## 1 ✓

Read `asm.c`

## ~1.1~

What is `seccomp_filter`

### Notes

- [ ] [seccomp_filter.txt](https://www.kernel.org/doc/Documentation/prctl/seccomp_filter.txt)
- [ ] [man 3 seccomp_init](http://man7.org/linux/man-pages/man3/seccomp_init.3.html)
- [ ] [man 3 seccomp_rule_add](http://man7.org/linux/man-pages/man3/seccomp_rule_add.3.html)

## 2

Learn to use `pwntools.asm`

### Notes

- [x] [pwnlib.asm](http://docs.pwntools.com/en/stable/asm.html)
- [x] [pwnlib.context](http://docs.pwntools.com/en/stable/context.html#module-pwnlib.context)
- [x] [pwnlib.constants](http://docs.pwntools.com/en/stable/constants.html#module-pwnlib.constants)

## 1.2

Disassemble `stub`

### Notes

```python
from pwn import *

stub = "\x48\x31\xc0\x48\x31\xdb\x48\x31\xc9\x48\x31\xd2\x48\x31\xf6\x48\x31\xff\x48\x31\xed\x4d\x31\xc0\x4d\x31\xc9\x4d\x31\xd2\x4d\x31\xdb\x4d\x31\xe4\x4d\x31\xed\x4d\x31\xf6\x4d\x31\xff"
context.update(bits=64, arch="amd64")
print disasm(stub)

```

Stub:

    0:   48 31 c0                xor    rax,rax
    3:   48 31 db                xor    rbx,rbx
    6:   48 31 c9                xor    rcx,rcx
    9:   48 31 d2                xor    rdx,rdx
    c:   48 31 f6                xor    rsi,rsi
    f:   48 31 ff                xor    rdi,rdi
    12:   48 31 ed                xor    rbp,rbp
    15:   4d 31 c0                xor    r8,r8
    18:   4d 31 c9                xor    r9,r9
    1b:   4d 31 d2                xor    r10,r10
    1e:   4d 31 db                xor    r11,r11
    21:   4d 31 e4                xor    r12,r12
    24:   4d 31 ed                xor    r13,r13
    27:   4d 31 f6                xor    r14,r14
    2a:   4d 31 ff                xor    r15,r15

## 3

Write shellcode

## 3.1 ✓

Write a code snippet in C - `shellcode.c`:

1. open file
1. read from it
1. write to stdout

### Notes

- [x] [man 2 open](http://man7.org/linux/man-pages/man2/open.2.html)
- [x] [man 2 read](http://man7.org/linux/man-pages/man2/read.2.html)
- [x] [man 2 write](http://man7.org/linux/man-pages/man2/write.2.html)
- [x] [X86 Assembly/Interfacing with Linux](https://en.wikibooks.org/wiki/X86_Assembly/Interfacing_with_Linux)
- [x] [Step out of current function with gdb](https://stackoverflow.com/questions/24712690/step-out-of-current-function-with-gdb)
- [x] [Linux Inside:Theory:Inline assembly](https://0xax.gitbooks.io/linux-insides/content/Theory/linux-theory-3.html)
- [x] [AT&T x86 Asm Syntax](https://cs.nyu.edu/courses/fall03/V22.0201-003/c_att_syntax.html)

## ~3.1.1~

Make calls to custom functions `inline`d.

### Notes

- [ ] [GCC Inline Functions](https://gcc.gnu.org/onlinedocs/gcc/Inline.html)

## 3.1.2 ✓

Write shellcode in `shellcode.s` for GNU `as`

### Notes

- [ ] [GNU Manuals: Using as](https://www.eecs.umich.edu/courses/eecs373/readings/Assembler.pdf)
- [ ] [X86 Assembly/GAS Syntax](https://en.wikibooks.org/wiki/X86_Assembly/GAS_Syntax)
- [ ] [NASM Assembly Language Tutorials](https://asmtutor.com/)

## 3.1.3 ✓

Write shellcode using Python's `keystone`

## 4

Sned `shellcode.bin` to `nc` process

### Notes

    HOME~$ scp -P 2222 ./shellcode.bin asm@pwnable.kr:/dev/shm
    REMOTE~$ nc 0 9026 < /dev/shm/shellcode.bin
