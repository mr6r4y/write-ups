# Ghidra Show Case - Reversing `restart-service.exe`

This PE file is found on a HTB machine. A friend of mine gave it to me because he was stuck on it. Later he uncovered a hidden password used for a login but he found it by using dynamic utility for Windows API tracing. I'm determined to solve this challenge with no dynamic tools only with Ghidra.

So lets start ..

## Initial Analysis

First thing that is noticed is the wrong default Compiler ID guessed by Ghidra so we need to fix it:

[![Watch the video](figs/v1.gif)](https://vimeo.com/559584993)

Lets fix this:

[![Watch the video](figs/v2.gif)](https://vimeo.com/559590060)

The executable obviously uses C++ and the C++ `std` library. There are string artefacts in support in this:

![Std in strings](figs/s1-std.png)

This is perfect opportunity for Ghidra's FID plugin. Based on the `GCC: (GNU) 8.3-win32 20190406` the exact version of Mingw-w64 toolchain and `libstdc++` library can be pinpointed to [g++-mingw-w64-x86-64](https://packages.debian.org/buster/g++-mingw-w64-x86-64). Lets create a new `.fiddb`:

[![Watch the video](figs/v3.gif)](https://vimeo.com/559839745)

Now we can apply it against our target:

[![Watch the video](figs/v4.gif)](https://vimeo.com/559840666)

That is better but we still have no clue where `main()` is.

## Finding `main()`

So we know `mingw-w64` is used. In `$GHIDRA_HOME/docs/GhidraClass/Advanced/Examples/` there is a example file - `animals.cpp`. A very simple C++ program with simple object initialization. The idea is to compile this file with `mingw-w64` and let `g++`'s symbols in and then analyse it with Ghidra. We find that `main()` is actually named `.text.startup`:

[![Watch the video](figs/v5.gif)](https://vimeo.com/manage/videos/560280901)

Finally we are at the gates of the challenge:

![main()](figs/s2-main.png)

## `main()` - Initial Analysis

**TO-DO: ..**
