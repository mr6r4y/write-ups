# Alienware

## Description

We discovered this tool in the E.T. toolkit which they used to encrypt and exfiltrate files from infected systems. Can you help us recover the files?

[rev_alienware.zip](rev_alienware.zip) - password `rev_alienware`

## Solution

There are two files observed:

- `Alienware.exe` - PE executable
- `Confidential.pdf.alien` - encrypted content

### `Alienware.exe` Analysis

After a shallow analysis an interesting function draws attention:

![](https://i.imgur.com/GUx2FqQ.png)

This is an encrypted resource and this function drops `xuTaV.dll` and executes `encryptFiles` out of it.

Extract `xuTaV.dll.enc` via `010 Editor`:

![](https://i.imgur.com/e2tzk3G.png)

You can see the 12 byte `XOR_KEY` at:

![](https://i.imgur.com/sHoXLxm.png)

and it is used at:

![](https://i.imgur.com/u0NoMPg.png)

Now we can decrypt via:

```python
from pwn import xor
from binascii import unhexlify

r = open("xuTaV.dll.enc", "rb").read()
lr = len(r)
k = unhexlify("78027680f544aa98ee651176")
lk = len(k)

rr = xor(r, k * (lr // len(k)) + k[0:lr % lk])

open("xuTaV.dll", "wb").write(rr)
```

### `xuTaV.dll` Analysis

![](https://i.imgur.com/5wT2zxc.png)

Interesting thing is that the string at `param_1` is passed from `Alienware.exe` and it is later used in `encrypt_file` to derive the key from:

![](https://i.imgur.com/z1owQqO.png)

![](https://i.imgur.com/X5R1InT.png)

where `param_3` comes from the parameter passed to `encryptFiles` from `Alienware.exe`:

![](https://i.imgur.com/juC42tG.png)

![](https://i.imgur.com/NdqRBHZ.png)

![](https://i.imgur.com/mPkH3Kn.png)

![](https://i.imgur.com/C7AsWuF.png)


The derived algorithm for decryption is:

```python
from pwn import xor
from binascii import unhexlify
import hashlib

from wincrypto import CryptCreateHash, CryptHashData, CryptDeriveKey, CryptEncrypt, CryptDecrypt
from wincrypto.constants import CALG_SHA_256, CALG_AES_128, bType_SIMPLEBLOB


def gen_key(s):
    xor_key = unhexlify("78027680f544aa98ee651176")
    xor_key = xor_key + xor_key[:4]
    ls = len(s)

    return bytes([xor_key[i] ^ s[i % ls] for i in range(0x10)])


def decrypt_file(filename, env_os):
    key = gen_key(env_os)
    sha256_hasher = CryptCreateHash(CALG_SHA_256)
    CryptHashData(sha256_hasher, key)
    aes_key = CryptDeriveKey(sha256_hasher, CALG_AES_128)
    encrypted_data = open(filename, "rb").read()
    decrypted_data = CryptDecrypt(aes_key, encrypted_data)

    return decrypted_data
```

Failed fix `wincrypto`:

![](https://i.imgur.com/FQlTNr7.png)

## Trying The Decryption Algo

Better way to emulate `wincrypto`. Using [Implement Windows CryptoAPI CryptDeriveKey Using OpenSSL APIs](https://stackoverflow.com/questions/4793583/implement-windows-cryptoapi-cryptderivekey-using-openssl-apis) but I still don't know what to do with:

![](https://i.imgur.com/8kaGRg9.png)

and:

![](https://i.imgur.com/dJKTKJY.png)

This may be helpful: [hasherezade/aes_crypt.cpp](https://gist.github.com/hasherezade/2860d94910c5c5fb776edadf57f0bef6)


```python
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
    print(hexlify(passwd))
    print(hexlify(passwd.decode("latin-1").encode("utf16")))
    t = c_size_t()
    passwd_buf = create_string_buffer(0x22)
    mbstowcs(passwd_buf, c_char_p(passwd), 0x10)
    passwd_len = lstrlenW(passwd_buf)
    print(passwd_len)
    print(hexlify(passwd_buf.raw))

    
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
```

aaaaand this **WORKED** !

![](https://i.imgur.com/bancmTX.png)

## Wine Setup

![](https://i.imgur.com/TWIekVG.png)

![](https://i.imgur.com/LPkK21S.png)

Ofcourse WINE is installed from the Wine repository (check in Google). You run anything with Wine such as:

```
wpwn ~/archs/python-3.8.9-amd64.exe 
wpwn pip install cryptography
wpwn pip install pwntools
```

and then the script:

```
wpwn python ./wdecr.py 
```