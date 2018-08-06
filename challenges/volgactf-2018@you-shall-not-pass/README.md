# `you-shall-not-pass` at VolgaCTF-2018

## Intro

    You Shall Not Pass

    This rather strange binary needs a particular string as its input. Yet we have no idea what this string is. Do you?

[ysnp](ysnp.tar.gz)

This is one of the `reverse` challenges in VolgaCTF 2018.
The challenge is 200 points. What is interesting about it is:
* has 40 threads that check the input
* it is written in C++
* every thread does a mathematical calculation that is checked against a constant

You can't find more suitable challenge for using a SMT solver on.
My choice is `z3` with its Python binding. But before the solving lets do the 
application analysis.

## Analysis

The app is a 64 bit ELF binary:

    $ file ysnp 
    ysnp: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=efd7438ad3cc4c32c0ce7838e6f72d005b0ad18e, stripped

Using `radare2` there are two interesting functions to analyse:
* `main`
* `sub.__cxa_guard_acquire_4e0`

For the sake of convenience I usually dump all the interesting stuff in separate `.asm` files. It is easier to inspect the
assembly in `Sublime Text 3` for me. It let me search/highlight more freely:

    r2> aaa
    r2> pdf @ main > asm/main.asm
    r2> pdf @ sub.__cxa_guard_acquire_4e0 > sub.__cxa_guard_acquire_4e0.asm

I spent some time there to grasp the whole scheme. I immediately noticed the launch of the 40 threads in `sub.__cxa_guard_acquire_4e0`. This code is repeated 40 times and it is easy to spot the start address of 
the thread functions in `esi`:

```nasm
|     ::|   0x00406509      be60204000     mov esi, 0x402060           ; "AVAUATUSH\x83\xec H\x8b\x1dmq "
|     ::|   0x0040650e      bf90926000     mov edi, 0x609290
|     ::|   0x00406513      48c705c22c20.  mov qword [0x006091e0], 0x609200 ; [0x6091e0:8]=0
|     ::|   0x0040651e      48c744241010.  mov qword [rsp + local_10h], 0x609110 ; [0x609110:8]=1
|     ::|   0x00406527      48c704247092.  mov qword [rsp], 0x609270   ; [0x609270:8]=0
|     ::|   0x0040652f      e83c0d0000     call sub.pthread_create_270
```

What I did is to search all the addresses and dump the assembly in separate files:

    r2> pd 108 @ 0x402060 > asm.th/01-2060.asm
    r2> pd 108 @ 0x403250 > asm.th/02-3250.asm
    r2> pd 108 @ 0x403c90 > asm.th/03-3c90.asm
    r2> pd 108 @ 0x405740 > asm.th/04-5740.asm
    r2> pd 108 @ 0x403470 > asm.th/05-3470.asm
    r2> pd 108 @ 0x402640 > asm.th/06-2640.asm
    r2> pd 108 @ 0x401490 > asm.th/07-1490.asm
    r2> pd 108 @ 0x403680 > asm.th/08-3680.asm
    r2> pd 108 @ 0x4042a0 > asm.th/09-42a0.asm
    r2> pd 108 @ 0x402840 > asm.th/10-2840.asm
    r2> pd 108 @ 0x405b80 > asm.th/11-5b80.asm
    r2> pd 108 @ 0x402e40 > asm.th/12-2e40.asm
    r2> pd 108 @ 0x405fc0 > asm.th/13-5fc0.asm
    r2> pd 108 @ 0x401a60 > asm.th/14-1a60.asm
    r2> pd 108 @ 0x405da0 > asm.th/15-5da0.asm
    r2> pd 108 @ 0x4061d0 > asm.th/16-61d0.asm
    r2> pd 108 @ 0x4040b0 > asm.th/17-40b0.asm
    r2> pd 108 @ 0x403050 > asm.th/18-3050.asm
    r2> pd 108 @ 0x402a40 > asm.th/19-2a40.asm
    r2> pd 108 @ 0x4048d0 > asm.th/20-48d0.asm
    r2> pd 108 @ 0x405540 > asm.th/21-5540.asm
    r2> pd 108 @ 0x401870 > asm.th/22-1870.asm
    r2> pd 108 @ 0x404ef0 > asm.th/23-4ef0.asm
    r2> pd 108 @ 0x405310 > asm.th/24-5310.asm
    r2> pd 108 @ 0x401260 > asm.th/25-1260.asm
    r2> pd 108 @ 0x403890 > asm.th/26-3890.asm
    r2> pd 108 @ 0x402c50 > asm.th/27-2c50.asm
    r2> pd 108 @ 0x403ea0 > asm.th/28-3ea0.asm
    r2> pd 108 @ 0x405100 > asm.th/29-5100.asm
    r2> pd 108 @ 0x4046b0 > asm.th/30-46b0.asm
    r2> pd 108 @ 0x403a80 > asm.th/31-3a80.asm
    r2> pd 108 @ 0x401e60 > asm.th/32-1e60.asm
    r2> pd 108 @ 0x401c70 > asm.th/33-1c70.asm
    r2> pd 108 @ 0x404cd0 > asm.th/34-4cd0.asm
    r2> pd 108 @ 0x404ad0 > asm.th/35-4ad0.asm
    r2> pd 108 @ 0x4044a0 > asm.th/36-44a0.asm
    r2> pd 108 @ 0x402260 > asm.th/37-2260.asm
    r2> pd 108 @ 0x402440 > asm.th/38-2440.asm
    r2> pd 108 @ 0x405960 > asm.th/39-5960.asm
    r2> pd 108 @ 0x401670 > asm.th/40-1670.asm

Radare could not recognize the functions at these addresses so I had to guess their lengths. 
Looking at the code a similar structure emerges in all threads:

```nasm
; Boiler plate code ..
; ...
; Beginning of calculations. Note the use of 'r14'. As I discover later - it holds the input in an integer array
...-----> 0x004020f5      498b06         mov rax, qword [r14]
:::||||   0x004020f8      488b88f00000.  mov rcx, qword [rax + 0xf0] ; [0xf0:8]=-1 ; 240
:::||||   0x004020ff      488b7008       mov rsi, qword [rax + 8]    ; [0x8:8]=-1 ; 8
:::||||   0x00402103      488b90980000.  mov rdx, qword [rax + 0x98] ; [0x98:8]=-1 ; 152
; ...
; ...
; Some calculations
; ...
; ...
; The comparison
:::||||   0x004021c1      483d77021400   cmp rax, 0x140277
; ...
; Exit code
```

I did some dynamic analysis in GDB also:

    break *(0x402060+0x98)
    break *(0x403250+0x98)
    ...
    break *(0x401670+0x98)
    run qwertyuiopasdfghjklzxcvbnm0123456789_=+-

I saw that `r14` holds the input (hexdump of `qword ptr [r14/rax]`):

    pwndbg> hexdump $rax
    +0000 0x61fcf0  71 00 00 00  00 00 00 00  77 00 00 00  00 00 00 00  │q...│....│w...│....│
    +0010 0x61fd00  65 00 00 00  00 00 00 00  72 00 00 00  00 00 00 00  │e...│....│r...│....│
    +0020 0x61fd10  74 00 00 00  00 00 00 00  79 00 00 00  00 00 00 00  │t...│....│y...│....│
    +0030 0x61fd20  75 00 00 00  00 00 00 00  69 00 00 00  00 00 00 00  │u...│....│i...│....│
    pwndbg> 
    +0040 0x61fd30  6f 00 00 00  00 00 00 00  70 00 00 00  00 00 00 00  │o...│....│p...│....│
    +0050 0x61fd40  61 00 00 00  00 00 00 00  73 00 00 00  00 00 00 00  │a...│....│s...│....│
    +0060 0x61fd50  64 00 00 00  00 00 00 00  66 00 00 00  00 00 00 00  │d...│....│f...│....│
    +0070 0x61fd60  67 00 00 00  00 00 00 00  68 00 00 00  00 00 00 00  │g...│....│h...│....│
    pwndbg> 
    +0080 0x61fd70  6a 00 00 00  00 00 00 00  6b 00 00 00  00 00 00 00  │j...│....│k...│....│
    +0090 0x61fd80  6c 00 00 00  00 00 00 00  7a 00 00 00  00 00 00 00  │l...│....│z...│....│
    +00a0 0x61fd90  78 00 00 00  00 00 00 00  63 00 00 00  00 00 00 00  │x...│....│c...│....│
    +00b0 0x61fda0  76 00 00 00  00 00 00 00  62 00 00 00  00 00 00 00  │v...│....│b...│....│
    pwndbg> 
    +00c0 0x61fdb0  6e 00 00 00  00 00 00 00  6d 00 00 00  00 00 00 00  │n...│....│m...│....│
    +00d0 0x61fdc0  30 00 00 00  00 00 00 00  31 00 00 00  00 00 00 00  │0...│....│1...│....│
    +00e0 0x61fdd0  32 00 00 00  00 00 00 00  33 00 00 00  00 00 00 00  │2...│....│3...│....│
    +00f0 0x61fde0  34 00 00 00  00 00 00 00  35 00 00 00  00 00 00 00  │4...│....│5...│....│
    pwndbg> 
    +0100 0x61fdf0  36 00 00 00  00 00 00 00  37 00 00 00  00 00 00 00  │6...│....│7...│....│
    +0110 0x61fe00  38 00 00 00  00 00 00 00  39 00 00 00  00 00 00 00  │8...│....│9...│....│
    +0120 0x61fe10  5f 00 00 00  00 00 00 00  3d 00 00 00  00 00 00 00  │_...│....│=...│....│
    +0130 0x61fe20  2b 00 00 00  00 00 00 00  2d 00 00 00  00 00 00 00  │+...│....│-...│....│

Then I cleaned up the code and gathered it all in [all-asm.json](all-asm.json) 

By searching all offsets in the snippets of all threads:

```nasm
mov rcx, qword [rax + 0xf0]
mov rsi, qword [rax + 8]
mov rdx, qword [rax + 0x98]
```

I came up with this:

```python
>>> indexes = [0xf0, 8, 0x98, ..., 0x10, 0xa8, 0x58, 0xc8]
>>> len(set(indexes))
3: 44
>>> max(set(indexes))
4: 352
>>> 352/8
5: 44
```

So the length of the input is 45 characters long. Expecting the input to have the format of a flag (`VolgaCTF{...}`)
I came up with the following start input in GDB:

    pwndbg> run "VolgaCTF{qwertyuiopasdfghjklzxcvbnmQWERTYUIO}"

The analysis part finishes with:
* having length and format of the input/flag
* isolated `asm` code in [all-asm.json](all-asm.json)

What has left is to parse the code and cram into z3.

## Z3 Script

The script has the following main goals:
* parse the limited operations in `all-asm.json`
* extract a constraint for each thread
* cram all into `solve(..)`

Some tricky stuff include:
* usage of `BitVecVal` and `BitVec` to simulate machine registers
* use python globals (simulate registers) as processor state
* craft valid python statements from assembly code that can be `exec`-ed (lazy to think of more sophisticated parser/interpreter) 

I can make the task easier cause I know part of the input:

```python
from z3 import *


TABLE = [
    BitVecVal(0x56, 64),
    BitVecVal(0x6f, 64),
    BitVecVal(0x6c, 64),
    BitVecVal(0x67, 64),
    BitVecVal(0x61, 64),
    BitVecVal(0x43, 64),
    BitVecVal(0x54, 64),
    BitVecVal(0x46, 64),
    BitVecVal(0x7b, 64),
]

TABLE = TABLE + [BitVec("x_%i" % i, 64) for i in range(9, 44)] + [BitVecVal(0x7d, 64)]

```

For more details look at [analysis.py](analysis.py).

At the end I get:

    $ python analysis.py
    ...
    ...
    ----------------------------------------
    [x_19 = 48,
     x_38 = 101,
     x_11 = 36,
     x_20 = 117,
     x_26 = 101,
     x_17 = 95,
     x_15 = 115,
     x_39 = 95,
     x_9 = 68,
     x_34 = 117,
     x_32 = 121,
     x_29 = 110,
     x_28 = 97,
     x_43 = 101,
     x_33 = 48,
     x_27 = 95,
     x_40 = 115,
     x_13 = 117,
     x_42 = 102,
     x_35 = 95,
     x_25 = 100,
     x_18 = 121,
     x_41 = 64,
     x_31 = 95,
     x_14 = 105,
     x_37 = 114,
     x_10 = 49,
     x_12 = 103,
     x_36 = 64,
     x_30 = 100,
     x_22 = 95,
     x_24 = 111,
     x_23 = 99,
     x_21 = 114,
     x_16 = 51]
    None

and I then converted this to:

```python
x = [i for i in "VolgaCTF{qwertyuiopasdfghjklzxcvbnmQWERTYUIO}"]
x[19] = chr(48)
x[38] = chr(101)
x[11] = chr(36)
x[20] = chr(117)
x[26] = chr(101)
x[17] = chr(95)
x[15] = chr(115)
x[39] = chr(95)
x[9 ]= chr(68)
x[34] = chr(117)
x[32] = chr(121)
x[29] = chr(110)
x[28] = chr(97)
x[43] = chr(101)
x[33] = chr(48)
x[27] = chr(95)
x[40] = chr(115)
x[13] = chr(117)
x[42] = chr(102)
x[35] = chr(95)
x[25] = chr(100)
x[18] = chr(121)
x[41] = chr(64)
x[31] = chr(95)
x[14] = chr(105)
x[37] = chr(114)
x[10] = chr(49)
x[12] = chr(103)
x[36] = chr(64)
x[30] = chr(100)
x[22] = chr(95)
x[24] = chr(111)
x[23] = chr(99)
x[21] = chr(114)
x[16] = chr(51)
print "".join(x)
```

    VolgaCTF{D1$guis3_y0ur_code_and_y0u_@re_s@fe}