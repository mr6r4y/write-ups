# `cmd2` Solution

After all the effort to delete all the `environ` variables the `PWD` variable still holds its value. I also have several functions such as `printf`. So the crafted payload is:

    ./cmd2 '$(cd .. && cd .. && printf $PWD)bin$(cd .. && cd .. && printf $PWD)cat f*'