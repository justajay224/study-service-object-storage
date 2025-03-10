from b2sdk.v2 import B2Api, InMemoryAccountInfo
from config.backblaze_config import BACKBLAZE_KEY_ID, BACKBLAZE_APPLICATION_KEY, BACKBLAZE_BUCKET_NAME
from utils.encrypt_decrypt import encrypt_file, decrypt_file
import base64
from io import BytesIO

class BackblazeService:
    def __init__(self):
        self.b2_api = B2Api(InMemoryAccountInfo())
        self.b2_api.authorize_account(
            'production', BACKBLAZE_KEY_ID, BACKBLAZE_APPLICATION_KEY
        )
        self.bucket = self.b2_api.get_bucket_by_name(BACKBLAZE_BUCKET_NAME)

    # Upload
    def upload_file(self, filename: str, file_data: bytes, password: str) -> str:
        # Enkripsi file sebelum di-upload
        encrypted_file_data = encrypt_file(file_data, password)
        print(f"Panjang encrypted_data (sebelum upload): {len(password)}")
        print(f"Panjang file_data (sebelum enkripsi): {len(file_data)}")  
        print(f"Panjang encrypted_data (setelah enkripsi): {len(password)}")  
        # Upload ke Backblaze
        uploaded_file = self.bucket.upload_bytes(
            encrypted_file_data, 
            filename, 
            file_info={ 
                'original_filename': filename,
                'encryption_type': 'AES-256'
            }
        )
        
        backblaze_file_id = uploaded_file.id_
        
        return backblaze_file_id

    # Mendapatkan daftar file
    def list_files(self):
        files = self.bucket.ls()

        file_list = []
        
        for file, _ in files: 
            # pprint(file.file_info)
            file_info = {
                "fileId": file.id_,
                "fileName": file.file_info.get("original_filename", "No fileName found")
            }
            file_list.append(file_info)
        
        return file_list
    
     # Download file
    def download_file(self, file_id: str, password: str) -> bytes:
        try:
            buffer = BytesIO()
            self.bucket.download_file_by_id(file_id).save(buffer)
            encrypted_data = buffer.getvalue()
            print(f"Panjang downloaded_data (setelah download): {len(encrypted_data)}")
            decrypted_data = decrypt_file(encrypted_data, password)
            return decrypted_data
        except Exception as e:
            raise Exception(f"Error: {str(e)}")

    
