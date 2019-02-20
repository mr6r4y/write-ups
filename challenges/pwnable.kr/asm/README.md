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

# Solution

The `asm.c` is a simple sandbox that allows only 5 syscalls to be executed from the sent shellcode. The `open`, `read`, `write` syscalls are sufficient to read a file and write its contents to `STDOUT_FILENO`. The `stub` just `xor`s the registers:

```python
from pwn import *

stub = "\x48\x31\xc0\x48\x31\xdb\x48\x31\xc9\x48\x31\xd2\x48\x31\xf6\x48\x31\xff\x48\x31\xed\x4d\x31\xc0\x4d\x31\xc9\x4d\x31\xd2\x4d\x31\xdb\x4d\x31\xe4\x4d\x31\xed\x4d\x31\xf6\x4d\x31\xff"
context.update(bits=64, arch="amd64")
print disasm(stub)

```

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

You can find my shellcode in [shellcode.c](shellcode.c) and the compilation rules are in [Makefile](Makefile).