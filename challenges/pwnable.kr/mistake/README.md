# `mistake` Solution

The `mistake` needs local compilation in order to fix a hardcoded path: `open("/home/mistake/password",O_RDONLY,0400)` becomes `open("./password",O_RDONLY,0400)`.

The bug is in:

    if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0){

which always assigns 0 to `fd` (stdin). So by setting input to:
    
    bbbbbbbbbbcccccccccc

I win - `xor("bbbbbbbbb") = "ccccccccc"`

# Notes

    python -c "print '\x01'*10" > i.txt

    gdb -x ./mistake.gdb ./mistake.1