# abrams_crackme_2017

## Intro

Crackme from [/r/ReverseEngineering](https://www.reddit.com/r/ReverseEngineering/comments/68iojj/linux_crackme_easy_must_patchrun_on_disk_sunday/)

You can dowlnoad it from: [abrams_crackme_2017](http://www.mindcrash.ca/abrams_crackme_2017)

## Analysis

Opening the binary in `radare2` shows the following:

    $ r2 ./abrams_crackme_2017

    [0x004009be]> s entry0
    [0x004009be]>

    [0x004009be]> pd 10
                ;-- entry0:
                ;-- rip:
                0x004009be      52             push rdx
                0x004009bf      54             push rsp
                0x004009c0      48c7c7000040.  mov rdi, sym.imp.__libc_start_main ; loc.imp.__gmon_start ; 0x400000
                0x004009c7  ~   48c7c64208ff.  mov rsi, 0xffffffffffff0842
                ;-- section_end..eh_frame:
                ;-- segment_end.LOAD0:
                0x004009cc      ff             invalid
                0x004009cd      ff             invalid
                0x004009ce      ff             invalid
                0x004009cf      ff             invalid
                0x004009d0      ff             invalid
                0x004009d1      ff             invalid

Because I've seen the binary under `gdb` I know that something is missing here:

    $ gdb ./abrams_crackme_2017
    ...
    gef➤  start
    ...
    ─────────────────────────────────────────────────────────────────────[ code:i386:x86-64 ]────
     →   0x4009be                  push   rdx
         0x4009bf                  push   rsp
         0x4009c0                  mov    rdi, 0x400000
         0x4009c7                  mov    rsi, 0x842
         0x4009ce                  mov    rdx, 0x7
         0x4009d5                  mov    rax, 0xa
    ──────────────────────────────────────────────────────────────────────────────[ threads ]────
    [#0] Id 1, Name: "abrams_crackme_", stopped, reason: BREAKPOINT
    ────────────────────────────────────────────────────────────────────────────────[ trace ]────
    [#0] 0x4009be → push rdx
    ─────────────────────────────────────────────────────────────────────────────────────────────
    gef➤



Somehow `r2` screws up during the loading and mapping of the ELF file because of wrong sizes in ELF headers.

I try loading the file without RBin info and get a different result:

    $ r2 -n ./abrams_crackme_2017

    [0x00000000]>

I'm dropped at `0x0` offset and the file is mapped with no VA offset. I have to recalculate my `entry0` - `0x4009be - 0x400000 = 0x9be`:

    [0x00000000]> s 0x9be
    [0x000009be]> aaa
    [x] Analyze all flags starting with sym. and entry0 (aa)
    [x] Analyze function calls (aac)
    [x] Analyze len bytes of instructions for references (aar)
    [x] Constructing a function name for fcn.* and sym.func.* functions (aan)
    [x] Type matching analysis for all functions (afta)
    [x] Use -AA or aaaa to perform additional experimental analysis.

Luckily the analysis of `r2` got better and I can list all the code just with `pdf` command (you can use `pd 20` to double check). In this case things are straight forward - you've got a `syscall`, a loop, and jump to modified code `jmp rax`:

    [0x000009be]> pdf
    |           ;-- rip:
    / (fcn) fcn.000009be 68
    |   fcn.000009be ();
    |           0x000009be      52             push rdx
    |           0x000009bf      54             push rsp
    |           0x000009c0      48c7c7000040.  mov rdi, 0x400000
    |           0x000009c7      48c7c6420800.  mov rsi, 0x842
    |           0x000009ce      48c7c2070000.  mov rdx, 7
    |           0x000009d5      48c7c00a0000.  mov rax, 0xa
    |           0x000009dc      0f05           syscall
    |           0x000009de      31d2           xor edx, edx
    |           ; CODE XREF from fcn.000009be (0x9f5)
    |       .-> 0x000009e0      8d0425700540.  lea eax, [0x400570]
    |       :   0x000009e7      678034100c     xor byte [eax + edx], 0xc
    |       :   0x000009ec      83c201         add edx, 1
    |       :   0x000009ef      81fad2020000   cmp edx, 0x2d2
    |       `=< 0x000009f5      75e9           jne 0x9e0
    |           0x000009f7      48c7c0700540.  mov rax, 0x400570
    |           0x000009fe      5c             pop rsp
    |           0x000009ff      5a             pop rdx
    \           0x00000a00      ffe0           jmp rax
    [0x000009be]>

### Fixing the `LOAD0` Program Header and `eh_frame` Section

As inspecting segments and sections of the ELF file I see that:

* `LOAD0` segment ends too early
* same with `eh_frame` section

However, somehow Linux loader is able to run the executable without problem but that screws up radare2's RBin parser and pwntools's ELF library:

    $ readelf -l abrams_crackme_2017

    Elf file type is EXEC (Executable file)
    Entry point 0x4009be
    There are 9 program headers, starting at offset 64

    Program Headers:
    ...
      LOAD           0x0000000000000000 0x0000000000400000 0x0000000000400000
                     0x00000000000009cc 0x00000000000009cc  R E    200000
    ...


    $ readelf -S abrams_crackme_2017
    There are 28 section headers, starting at offset 0x1170:

    Section Headers:
      [Nr] Name              Type             Address           Offset
           Size              EntSize          Flags  Link  Info  Align
    ...
           000000000000003c  0000000000000000 WAX       0     0     4
      [17] .eh_frame         PROGBITS         00000000004008b8  000008b8
           0000000000000114  0000000000000000 WAX       0     0     8
    ...


    $ readelf -e abrams_crackme_2017
    ELF Header:
    ...
      Start of program headers:          64 (bytes into file)
      Start of section headers:          4464 (bytes into file)
    ...

What I did is to finding the offending headers and patch them:

* `LOAD0` header is at `0x40+0x38*2` and size fields are at offsets `0x20` and `0x28`
* `eh_frame` section header is at `0x1170+17*0x40` and size field is at offset `0x20`

See:

* [load0.segment-size.patch.r2](load0.segment-size.patch.r2)
* [eh_frame.section-size.patch.r2](eh_frame.section-size.patch.r2)
* [Makefile](Makefile)

### Continue with Analysis

Let's see the syscall:

* syscall no: rax=0xa (`#define __NR_mprotect 10`) from `<unistd_64.h>`
* param1: `rdi=sym.imp.__gmon_start__ (void *addr)`
* param2: `rsi=0x842 (size_t len)`
* param3: `rdx=7 (int prot) = read+write+exec`

This gives write permissions to the program segment where `.text` is. It is necessary when you have self-modifying code. 

`eax` stores the base offset (`0x00400570` which is inside loaded `.text` section) and `edx` stores the counter. At offset `0x000009e7` there is a byte XOR with `0xc`. Obviously this is a decryption cycle. The loop ends when `edx` reaches `0x2d2` (code length).

The plan is:

1. decrypt payload into new `abrams_crackme_2017.decr`
1. remove the `xor` operation from `abrams_crackme_2017.decr`
1. analyze `abrams_crackme_2017.decr` (if working only on the binary payload, context is lost)

`abrams_crackme_2017.decr` should be a working executable with decrypted payload ready for analysis. You can check the [decryption script](decryptor.py).

### Payload Analysis

The rest is easier:

    $ r2 abrams_crackme_2017.decr 
    [0x004009be]> aaa
    [x] Analyze all flags starting with sym. and entry0 (aa)
    [x] Analyze function calls (aac)
    [x] Analyze len bytes of instructions for references (aar)
    [x] Constructing a function name for fcn.* and sym.func.* functions (aan)
    [x] Type matching analysis for all functions (afta)
    [x] Use -AA or aaaa to perform additional experimental analysis.
    [0x004009be]> pdf
    |           ;-- rip:
    / (fcn) entry0 66
    |   entry0 ();
    |           0x004009be      52             push rdx
    |           0x004009bf      54             push rsp
    |           0x004009c0      48c7c7000040.  mov rdi, sym.imp.__libc_start_main ; loc.imp.__gmon_start ; 0x400000
    |           0x004009c7      48c7c6420800.  mov rsi, 0x842              ; 2114
    |           0x004009ce      48c7c2070000.  mov rdx, 7
    |           0x004009d5      48c7c00a0000.  mov rax, 0xa
    |           0x004009dc      0f05           syscall
    |           0x004009de      31d2           xor edx, edx
    |           ; CODE XREF from entry0 (0x4009f5)
    |       .-> 0x004009e0      8d0425700540.  lea eax, [0x400570]         ; section..text ; "1\xedI\x89\xd1^H\x89\xe2H\x83\xe4\xf0PTI\xc7\xc0@\b@"
    |       :   0x004009e7      90             nop
    |       :   0x004009e8      90             nop
    |       :   0x004009e9      90             nop
    |       :   0x004009ea      90             nop
    |       :   0x004009eb      90             nop
    |       :   0x004009ec      83c201         add edx, 1
    |       :   0x004009ef      81fad2020000   cmp edx, 0x2d2              ; 722
    |       `=< 0x004009f5      75e9           jne 0x4009e0
    |           0x004009f7      48c7c0700540.  mov rax, 0x400570           ; section..text ; "1\xedI\x89\xd1^H\x89\xe2H\x83\xe4\xf0PTI\xc7\xc0@\b@"
    |           0x004009fe      5c             pop rsp
    \           0x004009ff      5a             pop rdx
    [0x004009be]> 

Go to the payload:
        
    [0x004009be]> s 0x400570
    [0x00400570]> pd
                ;-- section_end..plt:
                ;-- section..text:
                ; DATA XREFS from entry0 (0x4009e0, 0x4009f7)
                0x00400570      31ed           xor ebp, ebp                ; [13] -rwx section size 722 named .text
                0x00400572      4989d1         mov r9, rdx
                0x00400575      5e             pop rsi
                0x00400576      4889e2         mov rdx, rsp
                0x00400579      4883e4f0       and rsp, 0xfffffffffffffff0
                0x0040057d      50             push rax
                0x0040057e      54             push rsp
                0x0040057f      49c7c0400840.  mov r8, 0x400840
                0x00400586      48c7c1d00740.  mov rcx, 0x4007d0
                0x0040058d      48c7c74c0740.  mov rdi, 0x40074c
                0x00400594      ff15560a2000   call qword [reloc.__libc_start_main] ; [0x600ff0:8]=0
                0x0040059a      f4             hlt
    ...

This is a familiar `libc` boilerplate code. The `main()` is the first argument to `__libc_start_main`: `mov rdi, 0x40074c`

    [0x00400570]> s 0x40074c
    [0x0040074c]> pd
                ; DATA XREF from section_end..plt (+0x1d)
                0x0040074c      55             push rbp
                0x0040074d      4889e5         mov rbp, rsp
                0x00400750      4883ec10       sub rsp, 0x10
                0x00400754      c745fc010000.  mov dword [rbp - 4], 1
                0x0040075b      b900000000     mov ecx, 0
                0x00400760      ba00000000     mov edx, 0
                0x00400765      be00000000     mov esi, 0
                0x0040076a      bf00000000     mov edi, 0
                0x0040076f      b800000000     mov eax, 0
                0x00400774      e8c7fdffff     call sym.imp.ptrace
                0x00400779      4883f8ff       cmp rax, 0xffffffffffffffff
            ,=< 0x0040077d      7507           jne 0x400786
            |   0x0040077f      b8ffffffff     mov eax, 0xffffffff         ; -1
           ,==< 0x00400784      eb40           jmp 0x4007c6
           ||   ; CODE XREF from sub.getppid_666 (+0x117)
           |`-> 0x00400786      b800000000     mov eax, 0
           |    0x0040078b      e8d6feffff     call sub.getppid_666
           |    0x00400790      85c0           test eax, eax
           |,=< 0x00400792      7407           je 0x40079b
           ||   0x00400794      b8ffffffff     mov eax, 0xffffffff         ; -1
          ,===< 0x00400799      eb2b           jmp 0x4007c6
          |||   ; CODE XREF from sub.getppid_666 (+0x12c)
          ||`-> 0x0040079b      b800000000     mov eax, 0
          ||    0x004007a0      e8c1feffff     call sub.getppid_666
          ||    0x004007a5      837dfc00       cmp dword [rbp - 4], 0
          ||,=< 0x004007a9      750c           jne 0x4007b7
          |||   0x004007ab      bf65084000     mov edi, str.cracked        ; 0x400865 ; "cracked"
          |||   0x004007b0      e85bfdffff     call sym.imp.puts           ; int puts(const char *s)
         ,====< 0x004007b5      eb0a           jmp 0x4007c1
         ||||   ; CODE XREF from sub.getppid_666 (+0x143)
         |||`-> 0x004007b7      bf6d084000     mov edi, str.not_cracked    ; 0x40086d ; "not cracked"
         |||    0x004007bc      e84ffdffff     call sym.imp.puts           ; int puts(const char *s)
         |||    ; CODE XREF from sub.getppid_666 (+0x14f)
         `----> 0x004007c1      b800000000     mov eax, 0
          ||    ; CODE XREFS from sub.getppid_666 (+0x11e, +0x133)
          ``--> 0x004007c6      c9             leave
                0x004007c7      c3             ret
    ...

What we have here is:

* anti-debugging: `call sym.imp.ptrace`, `call sub.getppid_666`
* a simple `if` statement: `cmp dword [rbp - 4], 0`, `jne 0x4007b7`

In order to get `cracked` the simplest patch is to change the variable at `0x00400754  ..  mov dword [rbp - 4], 1`. The offset of this byte is `0x00400754+0x3`. If working with the original XORed binary we have to patch with `0x0^0xc` whcih is `0xc`. You can find the 1 byte patch at [crack-patch.r2](crack-patch.r2).

## Scripts

For all the magic to happen you need to have installed:

* [radare2](https://rada.re/r/)
* Python's [pwntools](https://github.com/Gallopsled/pwntools)

and type:

    $ cd write-ups/challenges/abrams_crackme_2017
    $ make
    ...
    $ ./abrams_crackme_2017.cracked 
    cracked
