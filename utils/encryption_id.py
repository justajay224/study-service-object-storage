from cryptography.fernet import Fernet
import os

def get_fernet():
    key = os.getenv("ENCRYPTION_KEY_ID")
    if not key:
        raise ValueError("ENCRYPTION_KEY_ID environment variable not set")
    return Fernet(key.encode())

def encrypt_data(data: str) -> str:
    fernet = get_fernet()
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    fernet = get_fernet()
    return fernet.decrypt(encrypted_data.encode()).decode()