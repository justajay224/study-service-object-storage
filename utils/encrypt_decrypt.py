from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def encrypt_file(file_data: bytes, key: bytes) -> bytes:
    nonce = get_random_bytes(12)
    
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    
    return nonce + tag + ciphertext

def decrypt_file(encrypted_data: bytes, key: bytes) -> bytes:
    nonce = encrypted_data[:12]
    tag = encrypted_data[12:28]
    ciphertext = encrypted_data[28:]
    
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    
    return cipher.decrypt_and_verify(ciphertext, tag)