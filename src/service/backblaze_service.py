from src.repository.backblaze_repository import BackblazeRepository
import base64
from utils.encrypt_decrypt import encrypt_file, decrypt_file
from dotenv import load_dotenv
import os

class BackblazeService:
    def __init__(self):
        self.repository = BackblazeRepository()
        load_dotenv()
        self.encryption_key = os.getenv("ENCRYPTION_KEY") 

    def upload_file(self, filename: str, base64_data: str) -> str:
        # Validasi
        try:
            decoded_data = base64.b64decode(base64_data)
        except Exception as e:
            raise ValueError("Invalid base64 data") from e

        
        encrypted_data = encrypt_file(decoded_data, self.encryption_key)
        
        
        return self.repository.upload_file(filename, encrypted_data)

    def list_files(self):
        return self.repository.list_files()

    def download_file(self, file_id: str) -> str:
        encrypted_data = self.repository.download_file(file_id)
        decrypted_data = decrypt_file(encrypted_data, self.encryption_key)
        return base64.b64encode(decrypted_data).decode("utf-8")