# Ghidra Show Case - Reversing `restart-service.exe`

This PE file is found on a HTB machine. A friend of mine gave it to me because he was stuck on it. Later he uncovered a hidden password used for a login but he found it by using dynamic utility for Windows API tracing. I'm determined to solve this challenge with no dynamic tools only with Ghidra.

So lets start ..

## Initial Analysis

First thing that is noticed is the wrong default Compiler ID guessed by Ghidra so we need to fix it:

[![Watch the video](figs/v1.gif)](https://vimeo.com/559584993)

**WARNING:** Not quite a fix yet - [MinGW analysis identifies incorrect calling conventions and demanging analyzer partially fails](https://github.com/NationalSecurityAgency/ghidra/issues/2208). Unfortunatelly when choosing `gcc` as a Compiler ID the calling conventions of the executable are messed up (uses `__stdcall` instead of the right `__fastcall`). When you let the `windows` Compiler ID - the C++ symbol names are not demangled.

The executable obviously uses C++ and the C++ `std` library. There are string artefacts in support in this:

![Std in strings](figs/s1-std.png)

This is perfect opportunity for Ghidra's FID plugin. Based on the `GCC: (GNU) 8.3-win32 20190406` the exact version of Mingw-w64 toolchain and `libstdc++` library can be pinpointed to [g++-mingw-w64-x86-64](https://packages.debian.org/buster/g++-mingw-w64-x86-64). Lets extract `libstdc++-6.dll`:

[![Watch the video](figs/v2.gif)](https://vimeo.com/560524519)

Minding the **WARNING** the plan is:

1. Import and analyze `libstdc++-6.dll` with `gcc` Compiler ID - the `__stdcall` is the right one for `.dll` files.
1. Leave `restart-service.exe` with the `windows` Compiler ID.
1. Create and populate a `.fiddb` from `libstdc++` with Compiler ID in Language set to `windows`
1. Apply this `.fiddb` to `restart-service.exe`

[![Watch the video](figs/v3.gif)](https://vimeo.com/560968132)

Now we can separate partially the boilerplate code and we can easier locate `main()`.

## Finding `main()`

So we know `mingw-w64` is used. In `$GHIDRA_HOME/docs/GhidraClass/Advanced/Examples/` there is a example file - `animals.cpp`. A very simple C++ program with simple object initialization. The idea is to compile this file with `mingw-w64` and let `g++`'s symbols in and then analyse it with Ghidra. We find that `main()` is actually named `.text.startup`:

[![Watch the video](figs/v4.gif)](https://vimeo.com/561694968)

Finally we are at the gates of the challenge:

![main()](figs/s2-main.png)

## `main()` - Initial Analysis

Two function calls are observed:

```c
...
FUN_004016d0();
...
iVar1 = FUN_004017b0(&DAT_00401950,(ulonglong)DAT_004a8010,&local_10,1,DAT_004a8014);
...
```

`FUN_004016d0` makes some strange reading from GS register -`GS:[0x30]` which in Windows is [Thread Information Block](https://en.wikipedia.org/wiki/Win32_Thread_Information_Block), reads values from memory (`_sysc:004ab004 7e aa 44 39  undefined4 3944AA7Eh`) , makes calculations with it and than write back to the same global variables.

Lets see `FUN_004017b0`:

![FUN_004017b0](figs/s3.png)

`syscall()` indicates direct usage of `SYSCALL` instruction. Knowing that the `RAX/EAX` register contains the syscall ID and recognizing the same global variables used in the previous function are loaded in `EAX`:

```
...
.text:004017f9 8b 05 09 98  MOV  EAX,dword ptr [DAT_004ab008]
...
.text:00401827 0f 05  SYSCALL
...
```

we can assume that `FUN_004016d0` decodes the syscall IDs that are used in `FUN_004017b0`. Lets rename `FUN_004016d0` to `decode_syscall_ids`.

## Analysis of `decode_syscall_ids`

In order to grasp the insane pointer dereferences at:

```c
  lVar2 = *(longlong *)
           (**(longlong **)
              (*(longlong *)(*(longlong *)(*(longlong *)(in_GS_OFFSET + 0x30) + 0x60) + 0x18) + 0x10
              ) + 0x30);
```

and using the following resources:

- [BytePointer:tebpeb64](http://bytepointer.com/resources/tebpeb64.htm)
- [GeoffChappell:PEB](https://www.geoffchappell.com/studies/windows/km/ntoskrnl/inc/api/pebteb/peb/index.htm)
- [Nirsoft:LDR_DATA_TABLE](http://www.nirsoft.net/kernel_struct/vista/LDR_DATA_TABLE_ENTRY.html)
- [Undocumented.NTinternals:PEB](http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FNT%20Objects%2FProcess%2FPEB.html)
- numerous MSDN searches

I was able to put together [tebpeb64.h](tebpeb64.h) (Most of it is from [BytePointer]((http://bytepointer.com) but some edition was needed). It is time to show some Ghidra kung fu. The plan is the following:

1. Clean the `.h` file using gcc
1. Parse the `.h` with Ghidra and make a Data DB
1. Use the new Data DB to annotate the appropriate structure data types

[![Watch the video](figs/v5.gif)](https://vimeo.com/562144909)

So we have the base address where the first DLL is loaded:

```c
  PVar2 = ((((in_GS_OFFSET->TEB->ProcessEnvironmentBlock->Ldr->InLoadOrderModuleList).Flink)->
           InLoadOrderLinks).Flink)->DllBase;

```

Later in this function `DllBase` is used in a bunch of other pointer dereferences.

From [How to find dlls loaded into a process and its location etc](https://stackoverflow.com/questions/3454281/how-to-find-dlls-loaded-into-a-process-and-its-location-etc) and what we know from `FUN_004017b0` the best candidate for `DllBase` is `ntdll.dll`. This makes perfect sense because `ntdll.dll` is the only place in Windows API where the `SYSCALL` instruction is used.

For figuring out what the rest of the code is doing we'll take different approach. Beaceuse every operation and dereference is done on another program the easiest way is to implement a simple script and apply it to analyzed `ntdll.dll` program in Ghidra.

### Scripting in `ntdll.dll`

TO-DO: ..
