/ (fcn) main 490
|   int main (int argc, char **argv, char **envp);
|           ; var int local_60h @ rbp-0x60
|           ; var int local_54h @ rbp-0x54
|           ; var int local_50h @ rbp-0x50
|           ; var int local_40h @ rbp-0x40
|           ; var int local_38h @ rbp-0x38
|           ; var int local_30h @ rbp-0x30
|           ; var int local_28h @ rbp-0x28
|           ; var int local_20h @ rbp-0x20
|           ; var int local_18h @ rbp-0x18
|           ; var int local_12h @ rbp-0x12
|           ; var int local_11h @ rbp-0x11
|           ; arg int argc @ rdi
|           ; arg char **argv @ rsi
|           ; DATA XREF from entry0 (0x400dfd)
|           0x00400ec4      55             push rbp
|           0x00400ec5      4889e5         mov rbp, rsp
|           0x00400ec8      4154           push r12
|           0x00400eca      53             push rbx
|           0x00400ecb      4883ec50       sub rsp, 0x50               ; 'P'
|           0x00400ecf      897dac         mov dword [local_54h], edi  ; argc
|           0x00400ed2      488975a0       mov qword [local_60h], rsi  ; argv
|           0x00400ed6      488d45ee       lea rax, [local_12h]
|           0x00400eda      4889c7         mov rdi, rax
|           0x00400edd      e88efeffff     call sym.std::allocator_char_::allocator
|           0x00400ee2      488d55ee       lea rdx, [local_12h]
|           0x00400ee6      488d45b0       lea rax, [local_50h]
|           0x00400eea      bef0144000     mov esi, str.Jack           ; 0x4014f0 ; "Jack"
|           0x00400eef      4889c7         mov rdi, rax
|           0x00400ef2      e819feffff     call sym.std::basic_string_char_std::char_traits_char__std::allocator_char__::basic_string_charconst__std::allocator_char_const
|           0x00400ef7      4c8d65b0       lea r12, [local_50h]
|           0x00400efb      bf18000000     mov edi, 0x18               ; 24
|           0x00400f00      e88bfeffff     call sym.operatornew_unsignedlong
|           0x00400f05      4889c3         mov rbx, rax
|           0x00400f08      ba19000000     mov edx, 0x19               ; 25
|           0x00400f0d      4c89e6         mov rsi, r12
|           0x00400f10      4889df         mov rdi, rbx
|           0x00400f13      e84c030000     call sym.Man::Man_std::string_int
|           0x00400f18      48895dc8       mov qword [local_38h], rbx
|           0x00400f1c      488d45b0       lea rax, [local_50h]
|           0x00400f20      4889c7         mov rdi, rax
|           0x00400f23      e8d8fdffff     call sym.std::basic_string_char_std::char_traits_char__std::allocator_char__::_basic_string
|           0x00400f28      488d45ee       lea rax, [local_12h]
|           0x00400f2c      4889c7         mov rdi, rax
|           0x00400f2f      e80cfeffff     call sym.std::allocator_char_::_allocator
|           0x00400f34      488d45ef       lea rax, [local_11h]
|           0x00400f38      4889c7         mov rdi, rax
|           0x00400f3b      e830feffff     call sym.std::allocator_char_::allocator
|           0x00400f40      488d55ef       lea rdx, [local_11h]
|           0x00400f44      488d45c0       lea rax, [local_40h]
|           0x00400f48      bef5144000     mov esi, str.Jill           ; 0x4014f5 ; "Jill"
|           0x00400f4d      4889c7         mov rdi, rax
|           0x00400f50      e8bbfdffff     call sym.std::basic_string_char_std::char_traits_char__std::allocator_char__::basic_string_charconst__std::allocator_char_const
|           0x00400f55      4c8d65c0       lea r12, [local_40h]
|           0x00400f59      bf18000000     mov edi, 0x18               ; 24
|           0x00400f5e      e82dfeffff     call sym.operatornew_unsignedlong
|           0x00400f63      4889c3         mov rbx, rax
|           0x00400f66      ba15000000     mov edx, 0x15               ; 21
|           0x00400f6b      4c89e6         mov rsi, r12
|           0x00400f6e      4889df         mov rdi, rbx
|           0x00400f71      e892030000     call sym.Woman::Woman_std::string_int
|           0x00400f76      48895dd0       mov qword [local_30h], rbx
|           0x00400f7a      488d45c0       lea rax, [local_40h]
|           0x00400f7e      4889c7         mov rdi, rax
|           0x00400f81      e87afdffff     call sym.std::basic_string_char_std::char_traits_char__std::allocator_char__::_basic_string
|           0x00400f86      488d45ef       lea rax, [local_11h]
|           0x00400f8a      4889c7         mov rdi, rax
|           0x00400f8d      e8aefdffff     call sym.std::allocator_char_::_allocator
|           ; CODE XREF from main (0x4010a9)
|       .-> 0x00400f92      befa144000     mov esi, str.1._use__2._after__3._free ; 0x4014fa ; "1. use\n2. after\n3. free\n"
|       :   0x00400f97      bf60226000     mov edi, obj.std::cout      ; obj._ZSt4cout__GLIBCXX_3.4 ; 0x602260
|       :   0x00400f9c      e84ffdffff     call sym.std::basic_ostream_char_std::char_traits_char___std::operator___std::char_traits_char___std::basic_ostream_char_std::char_traits_char____charconst
|       :   0x00400fa1      488d45e8       lea rax, [local_18h]
|       :   0x00400fa5      4889c6         mov rsi, rax
|       :   0x00400fa8      bfe0206000     mov edi, obj.std::cin       ; obj._ZSt3cin__GLIBCXX_3.4 ; 0x6020e0
|       :   0x00400fad      e81efeffff     call sym.std::istream::operator___unsignedint
|       :   0x00400fb2      8b45e8         mov eax, dword [local_18h]
|       :   0x00400fb5      83f802         cmp eax, 2                  ; 2
|      ,==< 0x00400fb8      7446           je 0x401000
|      |:   0x00400fba      83f803         cmp eax, 3                  ; 3
|     ,===< 0x00400fbd      0f84b3000000   je 0x401076
|     ||:   0x00400fc3      83f801         cmp eax, 1                  ; 1
|    ,====< 0x00400fc6      7405           je 0x400fcd
|   ,=====< 0x00400fc8      e9dc000000     jmp 0x4010a9

; Use: 1
|   ||||:   ; CODE XREF from main (0x400fc6)
|   |`----> 0x00400fcd      488b45c8       mov rax, qword [local_38h]
|   | ||:   0x00400fd1      488b00         mov rax, qword [rax]
|   | ||:   0x00400fd4      4883c008       add rax, 8
|   | ||:   0x00400fd8      488b10         mov rdx, qword [rax]
|   | ||:   0x00400fdb      488b45c8       mov rax, qword [local_38h]
|   | ||:   0x00400fdf      4889c7         mov rdi, rax
|   | ||:   0x00400fe2      ffd2           call rdx
|   | ||:   0x00400fe4      488b45d0       mov rax, qword [local_30h]
|   | ||:   0x00400fe8      488b00         mov rax, qword [rax]
|   | ||:   0x00400feb      4883c008       add rax, 8
|   | ||:   0x00400fef      488b10         mov rdx, qword [rax]
|   | ||:   0x00400ff2      488b45d0       mov rax, qword [local_30h]
|   | ||:   0x00400ff6      4889c7         mov rdi, rax
|   | ||:   0x00400ff9      ffd2           call rdx


|   |,====< 0x00400ffb      e9a9000000     jmp 0x4010a9
|   ||||:   ; CODE XREF from main (0x400fb8)
|   |||`--> 0x00401000      488b45a0       mov rax, qword [local_60h]
|   ||| :   0x00401004      4883c008       add rax, 8
|   ||| :   0x00401008      488b00         mov rax, qword [rax]
|   ||| :   0x0040100b      4889c7         mov rdi, rax
|   ||| :   0x0040100e      e80dfdffff     call sym.imp.atoi           ; int atoi(const char *str)
|   ||| :   0x00401013      4898           cdqe
|   ||| :   0x00401015      488945d8       mov qword [local_28h], rax
|   ||| :   0x00401019      488b45d8       mov rax, qword [local_28h]
|   ||| :   0x0040101d      4889c7         mov rdi, rax
|   ||| :   0x00401020      e84bfcffff     call sym.operatornew___unsignedlong
|   ||| :   0x00401025      488945e0       mov qword [local_20h], rax
|   ||| :   0x00401029      488b45a0       mov rax, qword [local_60h]
|   ||| :   0x0040102d      4883c010       add rax, 0x10
|   ||| :   0x00401031      488b00         mov rax, qword [rax]
|   ||| :   0x00401034      be00000000     mov esi, 0
|   ||| :   0x00401039      4889c7         mov rdi, rax
|   ||| :   0x0040103c      b800000000     mov eax, 0
|   ||| :   0x00401041      e87afdffff     call sym.imp.open           ; int open(const char *path, int oflag)
|   ||| :   0x00401046      488b55d8       mov rdx, qword [local_28h]
|   ||| :   0x0040104a      488b4de0       mov rcx, qword [local_20h]
|   ||| :   0x0040104e      4889ce         mov rsi, rcx
|   ||| :   0x00401051      89c7           mov edi, eax
|   ||| :   0x00401053      e848fcffff     call sym.imp.read           ; ssize_t read(int fildes, void *buf, size_t nbyte)
|   ||| :   0x00401058      be13154000     mov esi, str.your_data_is_allocated ; 0x401513 ; "your data is allocated"
|   ||| :   0x0040105d      bf60226000     mov edi, obj.std::cout      ; obj._ZSt4cout__GLIBCXX_3.4 ; 0x602260
|   ||| :   0x00401062      e889fcffff     call sym.std::basic_ostream_char_std::char_traits_char___std::operator___std::char_traits_char___std::basic_ostream_char_std::char_traits_char____charconst
|   ||| :   0x00401067      be600d4000     mov esi, sym.std::basic_ostream_char_std::char_traits_char___std::endl_char_std::char_traits_char___std::basic_ostream_char_std::char_traits_char ; 0x400d60
|   ||| :   0x0040106c      4889c7         mov rdi, rax
|   ||| :   0x0040106f      e8dcfcffff     call sym.std::ostream::operator___std::ostream_____std::ostream
|   |||,==< 0x00401074      eb33           jmp 0x4010a9


; Delete objects: 3
|   ||||:   ; CODE XREF from main (0x400fbd)
|   ||`---> 0x00401076      488b5dc8       mov rbx, qword [local_38h]
|   || |:   0x0040107a      4885db         test rbx, rbx
|   ||,===< 0x0040107d      7410           je 0x40108f
|   ||||:   0x0040107f      4889df         mov rdi, rbx
|   ||||:   0x00401082      e8b3010000     call sym.Human::_Human
|   ||||:   0x00401087      4889df         mov rdi, rbx
|   ||||:   0x0040108a      e8f1fbffff     call sym.operatordelete_void
|   ||||:   ; CODE XREF from main (0x40107d)
|   ||`---> 0x0040108f      488b5dd0       mov rbx, qword [local_30h]
|   || |:   0x00401093      4885db         test rbx, rbx
|   ||,===< 0x00401096      7410           je 0x4010a8
|   ||||:   0x00401098      4889df         mov rdi, rbx
|   ||||:   0x0040109b      e89a010000     call sym.Human::_Human
|   ||||:   0x004010a0      4889df         mov rdi, rbx
|   ||||:   0x004010a3      e8d8fbffff     call sym.operatordelete_void
|   ||||:   ; CODE XREF from main (0x401096)
|   ||`---> 0x004010a8      90             nop
|   || ||   ; CODE XREFS from main (0x400fc8, 0x400ffb, 0x401074)


\   ``-``=< 0x004010a9      e9e4feffff     jmp 0x400f92
