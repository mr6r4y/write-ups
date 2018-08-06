# `ezpz` by Gynvael

## Intro

This crackme is from Gynvael's [Hacking Livestream #1: ReRe and EZPZP](https://www.youtube.com/watch?v=JExnV1-GNxk).

## Scripts

The solution script can be used either statically:

    $ tar -xvzf ezpz.tar.gz
    $ ./ezpz_solution.py -f ezpz

or within *radare2* debug session:

    $ r2 -d ./ezpz

    [0x7fa8478c0cc0]> #!pipe ./ezpz_solution.py

