__all__ = [
    "gen_key",
    "mbstowcs",
    "decrypt_file",
]

from pwn import xor
from binascii import unhexlify, hexlify
import hashlib
# from Crypto.Cipher import AES
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def gen_key(s):
    xor_key = unhexlify("78027680f544aa98ee651176")
    xor_key = xor_key + xor_key[:4]
    ls = len(s)
    if ls > 0:
        dt = bytes([s[i % ls] for i in range(0x10)])
    else:
        dt = b"\x00" * 16

    return xor(dt, xor_key)


def mbstowcs(s):
    ## Failed attempt for naive conversion
    # return b"".join([bytes([0,i]) for i in s])

    ## The official way I saw `mbstowcs()` is working
    return s.decode("latin-1").encode("utf16")


def decrypt_file(filename, env_os):
    key = gen_key(env_os)
    lk = len(key)

    ## From the source code it seems that the character length is used as length of the `char *` put inside SHA156 algo
    # key = mbstowcs(key)
    h = hashlib.sha256(key).digest()

    ## As from https://stackoverflow.com/questions/4793583/implement-windows-cryptoapi-cryptderivekey-using-openssl-apis
    aes_key = h[:16]
    aes_iv = h[16:]

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv))
    decryptor = cipher.decryptor()

    encrypted_data = open(filename, "rb").read()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    return decrypted_data


def write_decrypted(k=b"Windows_NT"):
    return open("Confidential.pdf", "wb").write(decrypt_file("Confidential.pdf.alien", k))


# def decrypt_file_1(filename, env_os):
#     key = gen_key(env_os)
#     h = hashlib.sha256(key).digest()

#     aes_key = h[:16]
#     aes_iv = h[16:]

#     cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv))
#     decryptor = cipher.decryptor()

#     bl_size = 0x30

#     decrypted_data = b""
#     encrypted_data = open(filename, "rb").read()
#     for i in range(len(encrypted_data) // bl_size):
#         bl = decryptor.update(encrypted_data[i * bl_size:(i+1) * bl_size])
#         decrypted_data += bl
#     rest_len = len(encrypted_data) % bl_size
#     if rest_len > 0:
#         bl = decryptor.update(encrypted_data[-rest_len:])
#         decrypted_data += bl
#     bl = decryptor.finalize()
#     decrypted_data += bl

#     return decrypted_data


# def decrypt_file_2(filename, env_os):
#     key = gen_key(env_os)
#     h = hashlib.sha256(key).digest()

#     aes_key = h[:16]
#     aes_iv = h[16:]

#     a = AES.new(aes_key, AES.MODE_CBC, IV=aes_iv)

#     encrypted_data = open(filename, "rb").read()
#     decrypted_data = a.decrypt(encrypted_data)

#     return decrypted_data
