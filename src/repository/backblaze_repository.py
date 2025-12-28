from b2sdk.v2 import B2Api, InMemoryAccountInfo
from config.backblaze_config import BACKBLAZE_KEY_ID, BACKBLAZE_APPLICATION_KEY, BACKBLAZE_BUCKET_NAME
from io import BytesIO

# Singleton untuk B2 connection - hanya authorize sekali saat startup
class B2Connection:
    _instance = None
    _b2_api = None
    _bucket = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._b2_api = B2Api(InMemoryAccountInfo())
            cls._b2_api.authorize_account(
                'production', BACKBLAZE_KEY_ID, BACKBLAZE_APPLICATION_KEY
            )
            cls._bucket = cls._b2_api.get_bucket_by_name(BACKBLAZE_BUCKET_NAME)
            print("[B2] Connection initialized and authorized")
        return cls._instance
    
    @property
    def bucket(self):
        return self._bucket
    
    @property
    def api(self):
        return self._b2_api

# Initialize connection saat module di-import
_b2_conn = B2Connection.get_instance()

class BackblazeRepository:
    def __init__(self):
        # Reuse existing connection instead of creating new one
        self.bucket = _b2_conn.bucket

    def upload_file(self, filename: str, file_data: bytes) -> str:
        uploaded_file = self.bucket.upload_bytes(
            file_data, 
            filename, 
            file_info={ 
                'original_filename': filename,
                'encryption_type': 'AES-256'
            }
        )
        return uploaded_file.id_

    def get_all_files(self):
        files = self.bucket.ls()
        return [
            {
                "fileId": file.id_,
                "fileName": file.file_info.get("original_filename", "No filename")
            } 
            for file, _ in files
        ]

    def get_file_byID(self, file_id: str) -> tuple[bytes, str]:
        """Get file by ID and return bytes with filename"""
        buffer = BytesIO()
        file_info = self.bucket.get_file_info_by_id(file_id)
        self.bucket.download_file_by_id(file_id).save(buffer)
        original_filename = file_info.file_info.get("original_filename", "unknown")
        return buffer.getvalue(), original_filename
    
    def delete_file(self, file_id: str) -> None:
        try:
            file_info = self.bucket.get_file_info_by_id(file_id)
            self.bucket.delete_file_version(file_id, file_info.file_name)
        except Exception as e:
            raise ValueError(f"Gagal menghapus file: {str(e)}")
    
    def update_file(self, file_id: str, new_filename: str, new_file_data: bytes) -> str:
        self.delete_file(file_id)
        return self.upload_file(new_filename, new_file_data)

