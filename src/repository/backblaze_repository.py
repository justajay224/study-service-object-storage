from b2sdk.v2 import B2Api, InMemoryAccountInfo
from config.backblaze_config import BACKBLAZE_KEY_ID, BACKBLAZE_APPLICATION_KEY, BACKBLAZE_BUCKET_NAME
from io import BytesIO

class BackblazeRepository:
    def __init__(self):
        self.b2_api = B2Api(InMemoryAccountInfo())
        self.b2_api.authorize_account(
            'production', BACKBLAZE_KEY_ID, BACKBLAZE_APPLICATION_KEY
        )
        self.bucket = self.b2_api.get_bucket_by_name(BACKBLAZE_BUCKET_NAME)

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

    def list_files(self):
        files = self.bucket.ls()
        return [
            {
                "fileId": file.id_,
                "fileName": file.file_info.get("original_filename", "No filename")
            } 
            for file, _ in files
        ]

    def download_file(self, file_id: str) -> bytes:
        buffer = BytesIO()
        self.bucket.download_file_by_id(file_id).save(buffer)
        return buffer.getvalue()