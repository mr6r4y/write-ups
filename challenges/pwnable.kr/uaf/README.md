# `uaf` Solution

- [d_uaf.py](d_uaf.py) - Debug session and GDB script used while working on solution
- [e_uaf.py](e_uaf.py) - Exploit used on pwnable.kr server

All you need to catch is that the size of the payload should be equal to the size of the created objects. The memory footprint for `Man` for example is similar to:

    +------------------------+
    | Man Object on heap     |
    | ...                    |
    +========================+
    | pointer to 1st method  | 8 bytes
    +------------------------+
    | int age                | 8 bytes
    +------------------------+
    | string name            | 8 bytes
    +------------------------+

At `main()` you can see the dereference of method `introduce` as:

```nasm
0x00400fcd      488b45c8       mov rax, qword [local_38h]
0x00400fd1      488b00         mov rax, qword [rax]
0x00400fd4      4883c008       add rax, 8
0x00400fd8      488b10         mov rdx, qword [rax]
0x00400fdb      488b45c8       mov rax, qword [local_38h]
0x00400fdf      4889c7         mov rdi, rax
0x00400fe2      ffd2           call rdx
```

We can now construct a payload that has its first 8 bytes a pointer (mind the `add rax, 8`) that will have the address of `Human::give_shell`.