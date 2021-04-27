from pwn import xor
from binascii import unhexlify, hexlify
from ctypes import *
from ctypes.wintypes import *
import os


crypt32 = windll.Advapi32
mbstowcs = windll.msvcr100.mbstowcs
lstrlenW = windll.kernel32.lstrlenW
CryptAcquireContext = crypt32.CryptAcquireContextW
CryptCreateHash = crypt32.CryptCreateHash
CryptHashData = crypt32.CryptHashData
CryptDeriveKey = crypt32.CryptDeriveKey
CryptDecrypt = crypt32.CryptDecrypt

SHA256 = 0x800c
AES128 = 0x660e
provider = "Microsoft Enhanced RSA and AES Cryptographic Provider"


def gen_key(s):
    xor_key = unhexlify("78027680f544aa98ee651176")
    xor_key = xor_key + xor_key[:4]
    ls = len(s)
    if ls > 0:
        dt = bytes([s[i % ls] for i in range(0x10)])
    else:
        dt = b"\x00" * 16

    return xor(dt, xor_key)


def decrypt_file_w(filename, env_os):
    passwd = gen_key(env_os)
    t = c_size_t()
    passwd_buf = create_string_buffer(0x22)
    mbstowcs(passwd_buf, c_char_p(passwd), 0x10)
    passwd_len = lstrlenW(passwd_buf)

    ctx = c_void_p()
    CryptAcquireContext(byref(ctx), 0, provider, 0x18, 0xf0000000)
    chash = c_void_p()
    CryptCreateHash(ctx, SHA256, 0, 0, byref(chash))
    CryptHashData(chash, passwd_buf, passwd_len, 0);
    aes_key = c_void_p()
    CryptDeriveKey(ctx, AES128, chash, 0, byref(aes_key))
    
    bl_size = 0x30
    data_buf = create_string_buffer(bl_size)

    decrypted_data = b""
    encrypted_data = open(filename, "rb").read()
    len_enc_data = len(encrypted_data)
    rest_len = len_enc_data % bl_size
    last = len_enc_data // bl_size - 1
    for i in range(len_enc_data // bl_size):
        if i == last and rest_len == 0:
            data_buf.raw = encrypted_data[i * bl_size:(i+1) * bl_size]
            CryptDecrypt(aes_key, 0, True, 0, data_buf, byref(DWORD(bl_size)))
            decrypted_data += data_buf.raw
        else:
            data_buf.raw = encrypted_data[i * bl_size:(i+1) * bl_size]
            CryptDecrypt(aes_key, 0, False, 0, data_buf, byref(DWORD(bl_size)))
            decrypted_data += data_buf.raw
    
    if rest_len > 0:
        data_buf.raw = encrypted_data[-rest_len:]
        CryptDecrypt(aes_key, 0, True, 0, data_buf, byref(DWORD(rest_len)))
        decrypted_data += data_buf.raw
    
    return decrypted_data


def main():
    open("Confidential.pdf", "wb").write(decrypt_file_w("Confidential.pdf.alien", b"Windows_NT"))


if __name__ == "__main__":
    main()
