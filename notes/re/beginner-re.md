# Beginnig Reverse Code Engineering

## Execution File Formats

- PE:
    - [An In-Depth Look into the Win32 Portable Executable File Format](https://docs.microsoft.com/en-us/archive/msdn-magazine/2002/february/inside-windows-win32-portable-executable-file-format-in-detail)
    - [An In-Depth Look into the Win32 Portable Executable File Format, Part 2](https://docs.microsoft.com/en-us/archive/msdn-magazine/2002/march/inside-windows-an-in-depth-look-into-the-win32-portable-executable-file-format-part-2%20)
- ELF:
    - [Learning Linux Binary Analysis](https://www.amazon.com/Learning-Binary-Analysis-elfmaster-ONeill/dp/1782167102/) - Ch 1, Ch 2
    - [How glibc calls main()](https://hammertux.github.io/libc-start) - полезно когато `main()` не се казва така и как да го намериш през `entry`

### Example: How to find `main()` in stripped ELF

By following `entry`:

![](https://imgur.com/gSaHWz7.png)

The first argument passed to a strange fuction is the `main` address - `LAB_00101170`:

![](https://imgur.com/x07Bfwu.png)

![](https://imgur.com/FT22Y7t.png)


## Processor Architecture and Assembler

- x86/amd64:
    - [Practical Reverse Engineering](https://www.amazon.com/Practical-Reverse-Engineering-Reversing-Obfuscation/dp/1118787315/) - Ch 1
    - google "x86 assembly"
- ARM:
    - [Practical Reverse Engineering](https://www.amazon.com/Practical-Reverse-Engineering-Reversing-Obfuscation/dp/1118787315/) - Ch 2
    - [Azeria Labs](https://azeria-labs.com/)

## Very Easy Challenges

- [IOLI-crackme](https://github.com/Maijin/radare2-workshop-2015/tree/master/IOLI-crackme)

## Tools

- [Ghidra](https://ghidra-sre.org/)
    - [Three Heads are Better Than One: Mastering Ghidra - Alexei Bulazel, Jeremy Blackthorne - INFILTRATE 2019](https://vimeo.com/335158460)
- [Radare2](https://rada.re/n/radare2.html)