
import base64

def encrypt_data(data: str) -> str:
    return base64.urlsafe_b64encode(data.encode()).decode().rstrip("=")

def decrypt_data(encoded_data: str) -> str:
    return base64.urlsafe_b64decode(encoded_data + "==").decode()

# import zlib
# from cryptography.fernet import Fernet
# import os

# def get_fernet():
#     key = os.getenv("ENCRYPTION_KEY_ID")
#     if not key:
#         raise ValueError("ENCRYPTION_KEY_ID environment variable not set")
#     return Fernet(key.encode())

# def encrypt_data(data: str) -> str:
#     # Kompresi data
#     compressed_data = zlib.compress(data.encode())
#     # Enkripsi data terkompresi
#     fernet = get_fernet()
#     encrypted_data = fernet.encrypt(compressed_data)
#     return encrypted_data.decode()

# def decrypt_data(encrypted_data: str) -> str:
#     fernet = get_fernet()
#     # Dekripsi data
#     decrypted_data = fernet.decrypt(encrypted_data.encode())
#     # Dekompresi data
#     decompressed_data = zlib.decompress(decrypted_data)
#     return decompressed_data.decode()