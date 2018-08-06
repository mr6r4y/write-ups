#!/usr/bin/env python

import os
import sys
import subprocess as sp
import socket
import time


def main():
    # Stage 1
    a = [('A%i' % i) for i in range(99)]
    a[64] = ""
    a[65] = "\x20\x0a\x0d"
    a[66] = "4444"  # Stage 5 port

    # Stage 3
    os.environ["\xde\xad\xbe\xef"] = "\xca\xfe\xba\xbe"

    # Stage 4
    open("\x0a", "w").write("\x00\x00\x00\x00")

    # Stage 2
    r, w = os.pipe()
    p = sp.Popen(['/home/input2/input'] + a, stdin=sp.PIPE, stderr=r)

    os.close(r)
    os.write(w, "\x00\x0a\x02\xff")
    os.close(w)

    p.stdin.write("\x00\x0a\x00\xff")

    # Stage 5
    time.sleep(1)

    host = '127.0.0.1'
    port = 4444
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall("\xde\xad\xbe\xef")
    s.close()

    p.wait()


if __name__ == '__main__':
    main()
