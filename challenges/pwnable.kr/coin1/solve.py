#!/usr/bin/env python


from pwn import *
import argparse
import re
import random


def get_args():
    parser = argparse.ArgumentParser(description="Pwnable.kr - coin1 challenge solver")
    return parser.parse_args()


def parse_coins(line):
    p = "^N=([\d]+) C=([\d]+)$"
    r = re.match(p, line)

    return int(r.group(1)), int(r.group(2))


def process_coins(r):
    try:
        n, c = parse_coins(r.recvline_regex("^N=[\d]+ C=[\d]+$", timeout=10.0))
    except Exception:
        log.info(r.recvall())
    log.info("N=%i, c=%i" % (n, c))

    all_n = range(n)

    for i in range(c):
        m = len(all_n) / 2

        left_n, right_n = all_n[:m], all_n[m:]
        inp = " ".join(["%i" % i for i in left_n])
        r.sendline(inp)

        out = int(r.recvline())
        # log.info("Coins: %s, Weight: %i" % (inp, out))

        if out < 10 * len(left_n):
            all_n = left_n
        else:
            all_n = right_n

    wrong_coin = "%i" % all_n[0]
    r.sendline(wrong_coin)

    result = r.recvline()
    log.info("Result: %s" % result)


def main():
    args = get_args()

    # host, port = "pwnable.kr", 9007
    host, port = "127.0.0.1", 9007

    r = remote(host, port)

    try:
        while True:
            process_coins(r)
    except EOFError:
        log.info("Game Over")


if __name__ == '__main__':
    main()
