from b2sdk.v2 import B2Api, InMemoryAccountInfo
from config.backblaze_config import BACKBLAZE_KEY_ID, BACKBLAZE_APPLICATION_KEY, BACKBLAZE_BUCKET_NAME
import uuid
from pprint import pprint

class BackblazeService:
    def __init__(self):
        self.b2_api = B2Api(InMemoryAccountInfo())
        self.b2_api.authorize_account(
            'production', BACKBLAZE_KEY_ID, BACKBLAZE_APPLICATION_KEY
        )
        self.bucket = self.b2_api.get_bucket_by_name(BACKBLAZE_BUCKET_NAME)

    # ulpoad
    def upload_file(self, filename: str, file_data: bytes):
        file_id = str(uuid.uuid4())

        file_info = {
            'fileName': filename, 
            'fileId': file_id 
        }

        uploaded_file = self.bucket.upload_bytes(file_data, filename, file_info=file_info)

        # pprint(uploaded_file.file_info)

        return uploaded_file.file_info.get('fileId', file_id)

    # untuk menampilkan file info dari backblaze
    def list_files(self):
        files = self.bucket.ls()

        file_list = []
        
        for file, _ in files:  # Unpacking tuple (file, metadata)
            # pprint(file.file_info)
            file_info = {
                "fileId": file.file_info.get("fileid", "No fileId found"),
                "fileName": file.file_info.get("filename", "Nama tidak ada")
            }
            file_list.append(file_info)
        
        return file_list
