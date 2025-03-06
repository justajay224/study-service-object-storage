from fastapi import UploadFile, File, HTTPException
from src.service.backblaze_service import BackblazeService
from src.validation.file_validation import validate_file_extension, validate_file_size
from src.model.models import ApiResponse, ResponseModel, MetaDataModel
from utils.response_api import generate_response, generate_error_response

class BackblazeController:
    def __init__(self):
        self.backblaze_service = BackblazeService()

    async def upload_file(self, file: UploadFile = File(...)):
        
        # Validasi ekstensi file
        if not validate_file_extension(file.filename):
            return generate_error_response("File extension is not allowed. Only PNG, JPG, JPEG, and PDF are allowed.", 400, "0001")

        # Validasi ukuran file
        if not validate_file_size(len(await file.read())):
            return generate_error_response("File is too large. Maximum size is 10MB.", 400, "0002")
        
        # Mengembalikan file_id setelah validasi berhasil
        file_data = await file.read()
        uploaded_file_id = self.backblaze_service.upload_file(file.filename, file_data)

        # response data
        response_data = ResponseModel(
            fileId=uploaded_file_id,
            fileName=file.filename,
            message="File uploaded successfully",
            status="Success"
        )
        
        # metadata
        meta_data = MetaDataModel(
            message="OK",
            code=201,
            response_code="0001"
        )
    
        # Mengembalikan response dengan file info dan metadata menggunakan generate_response
        return generate_response(metaData=meta_data.dict(), data=response_data.dict())

    async def list_files(self):
        """Mengambil daftar file dari Backblaze B2 dan mengembalikan respons dengan generate_response"""
        try:
            # Memanggil service untuk mengambil daftar file
            files = self.backblaze_service.list_files()

            # Menyiapkan metadata
            meta_data = MetaDataModel(
                message="OK",
                code=200,
                response_code="0000"
            )

            # Menggunakan generate_response untuk menghasilkan format yang konsisten
            return generate_response(metaData=meta_data.dict(), data=files)

        except Exception as e:
            # Jika terjadi error, menggunakan generate_error_response
            error_message = f"Error while fetching files: {str(e)}"
            return generate_error_response(message=error_message, code=500, response_code="0002")
