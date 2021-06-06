# Ghidra Show Case - Reversing `restart-service.exe`

This PE file is found on a HTB machine. A friend of mine gave it to me because he was stuck on it. Later he uncovered a hidden password used for a login but he found it by using dynamic utility for Windows API tracing. I'm determined to solve this challenge with no dynamic tools only with Ghidra.

So lets start ..

# Analysis

First thing that is noticed is the wrong default Compiler ID guessed by Ghidra so we need to fix it:

[![Watch the video](figs/v1.gif)](https://vimeo.com/559584993)
