# 64bit_Confusion

## Intro

This is a crackme from http://crackmes.de/. It is a elf64 compiled on Gentoo in 2004. The crackme is solved and it is fairly easy one. However things have changed in Linux for the last 13 years. There is incompatibility between current libc versions used then and now. The resurection of the executable under modern Ubuntu was even more interesting then the crackme itself.

## Analysis

This was easy one. 

However, I spent some time researching ELF format in order to fix its sections. This is a very old crackme and it won't start on modern Linux distribution. I had to patch first the `.dynsym` section before moving ahead.

The "protection" is a check after `ptrace` call which is easily patched.



