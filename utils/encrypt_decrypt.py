import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from typing import Tuple

# Menghasilkan kunci AES-256 menggunakan password
def generate_key(password: str, salt: bytes) -> bytes:
    return scrypt(
        password.encode(), 
        salt, 
        key_len=32,
        N=2**14,     
        r=8,
        p=1
    )

# Enkripsi
def encrypt_file(file_data: bytes, password: str) -> bytes:
    salt = get_random_bytes(16)
    nonce = get_random_bytes(12)
    key = scrypt(password.encode(), salt, key_len=32, N=2**14, r=8, p=1)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    encrypted_data = salt + nonce + tag + ciphertext
    return base64.b64encode(encrypted_data)

# Deskripsi
def decrypt_file(encrypted_data: bytes, password: str) -> bytes:
    encrypted_data = base64.b64decode(encrypted_data)
    salt = encrypted_data[:16]
    nonce = encrypted_data[16:28]
    tag = encrypted_data[28:44]
    ciphertext = encrypted_data[44:]
    key = scrypt(password.encode(), salt, key_len=32, N=2**14, r=8, p=1)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
