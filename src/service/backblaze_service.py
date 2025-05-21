from src.repository.backblaze_repository import BackblazeRepository
import base64
from utils.encrypt_decrypt import encrypt_file, decrypt_file
from config.aes_config import KEY

class BackblazeService:
    def __init__(self):
        self.repository = BackblazeRepository()
        self.encryption_key = KEY
        
    def upload_file(self, filename: str, base64_data: str) -> str:
        try:
            decoded_data = base64.b64decode(base64_data)
        except Exception as e:
            raise ValueError("Invalid base64 data") from e

        
        try:
            encrypted_data = encrypt_file(decoded_data, self.encryption_key)
        except ValueError as e:
            raise ValueError(f"Encryption failed: {str(e)}") from e
          
        return self.repository.upload_file(filename, encrypted_data)

    def get_all_files(self):
        return self.repository.get_all_files()

    def get_file_byID(self, file_id: str) -> str:
        encrypted_data = self.repository.get_file_byID(file_id)
        decrypted_data = decrypt_file(encrypted_data, self.encryption_key)
        return base64.b64encode(decrypted_data).decode("utf-8")
    
    def update_file(self, file_id: str, new_filename: str, base64_data: str) -> str:
        try:
            decoded_data = base64.b64decode(base64_data)
            encrypted_data = encrypt_file(decoded_data, self.encryption_key)
            return self.repository.update_file(file_id, new_filename, encrypted_data)
        except Exception as e:
            raise ValueError(f"Update failed: {str(e)}")
        
    def delete_file(self, file_id: str) -> None:
        try:
            self.repository.delete_file(file_id)
        except Exception as e:
            raise ValueError(f"Delete error: {str(e)}")