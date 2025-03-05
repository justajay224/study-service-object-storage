from fastapi import UploadFile, File
from src.service.backblaze_service import BackblazeService

class BackblazeController:
    def __init__(self):
        self.backblaze_service = BackblazeService()

    async def upload_file(self, file: UploadFile = File(...)):
        # Menjalankan service untuk mengupload file
        uploaded_file_id = self.backblaze_service.upload_file(file.filename, await file.read())

        # Mengembalikan response dengan file info yang diperlukan
        return {
            "fileName": file.filename,
            "fileId": uploaded_file_id,
            "message": "File uploaded successfully"
        }

    async def list_files(self):
        files = self.backblaze_service.list_files()
        return {"files": files}
