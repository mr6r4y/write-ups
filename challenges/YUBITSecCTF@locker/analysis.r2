# NOTES:
#   GNU MP library used https://gmplib.org/

aaa

s main

f important.flag @ main + 0x14e
f important.flag_passwd_eax @ main + 0x127
f important.password_init @ main + 0x8
f important.after_password_init @ main + 0xf

f important.first_printf @ main + 0x34
f important.get_password_scanf @ main + 0x4a
f important.false_flag_printf @ main + 0xf8
f important.no_cookies_printf @ main + 0x164

# Address at "return eax"
f important.main_exit @ main + 0x17c

# Address of 'ret' instruction
f important.main_ret @ main + 0x182


afvn local_34h password
afvn local_30h no_flag_for_you
pdf
