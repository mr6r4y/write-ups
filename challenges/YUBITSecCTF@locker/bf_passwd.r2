?e
?e 'Run the main analysis'
?e
. ./analysis.r2

?e
?e
?e

?e 'Load the file in debug mode with write permissions'
?e 'The changes are made at the vaddr offset so there are no file changes (at 0x0 offset)'
?e
ood+

?e
?e 'Break after init of "password"'
db important.after_password_init
?e

?e 'Stop at important.after_password_init'
?e 'We have the password initialised to 0 by the program'
?e
dc
?e

?e 'Break on flag'
db important.flag_passwd_eax

?e
?e 'Rewrite init password into increment'
?e 'I need 7 bytes that turn init "password" into increment "password"'
wx `!rasm2 -b 64 -a x86 'add dword [rbp-0x34], 0x1; nop; nop; nop'` @ important.password_init

?e

?e 'NOP the 1st print'
wx 9090909090 @ important.first_printf

?e

?e 'NOP the scanf'
wx 9090909090 @ important.get_password_scanf

?e

?e 'NOP the false flag print'
wx 9090909090 @ important.false_flag_printf

?e

?e 'NOP the no cookies print'
wx 9090909090 @ important.no_cookies_printf

?e

?e 'Try a relative jump to "important.after_password_init"'
?e 'abs(-372) = 0x174 = offset to important.password_init with 2 bytes for prev instruction'
wx `!rasm2 -b 64 -a x86 'xor eax, eax; jmp -372'` @ important.main_exit

?e

?e 'Remove initial breakpoint'
?e
db -important.after_password_init

?e 'Must break on flag goodboy'
?e
dc

?e
?e 'One step further :)'
?e
ds
?e
?e

?e "The password is: "
?vi `dr?eax`
?e
?e