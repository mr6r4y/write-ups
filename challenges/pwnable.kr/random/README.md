# `random` Solution

Because `rand()` is called without seeding it will return the same "random" number on every execution:

    gdb> break *(main+18)
    gdb> run
    gdb> print $rax
    $1 = 1804289383

and `1804289383^0xdeadbeef` is `3039230856`.