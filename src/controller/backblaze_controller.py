from fastapi import UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from src.service.backblaze_service import BackblazeService
from src.validation.file_validation import validate_file_extension, validate_file_size
from src.model.models import ApiResponse, ResponseModel, MetaDataModel
from utils.encrypt_decrypt import encrypt_file, decrypt_file
from utils.response_api import generate_response, generate_error_response
from dotenv import load_dotenv
from pprint import pprint
import os
import base64

class BackblazeController:
    def __init__(self):
        self.backblaze_service = BackblazeService()
        
    def _get_encryption_key(self):
        load_dotenv() 
        return os.getenv("ENCRYPTION_KEY")  

    async def upload_file(self, file: UploadFile = File(...)):
        
        password = self._get_encryption_key()
        
        file_data = await file.read()
        # Validasi ekstensi file
        if not validate_file_extension(file.filename):
            return generate_error_response("File extension is not allowed. Only PNG, JPG, JPEG, and PDF are allowed.", 400, "0001")

        # Validasi ukuran file
        if not validate_file_size(len(file_data)):
            return generate_error_response("File is too large. Maximum size is 10MB.", 400, "0002")
        
        # Enkripsi file
        encrypted_file_data = encrypt_file(file_data, password) 
        
        print(f"Panjang file_data (original): {len(file_data)}")
        print(f"Panjang encrypted_data (base64): {len(password)}")
        print(f"Panjang encrypted_data_raw (decode base64): {len(base64.b64decode(password))}") 

        # Upload file ke Backblaze
        uploaded_file_id = self.backblaze_service.upload_file(file.filename, encrypted_file_data, password)

        # response data
        response_data = ResponseModel(
            fileId=uploaded_file_id,
            fileName=file.filename,
            message="File uploaded and encrypted successfully",
            status="Success"
        )

        meta_data = MetaDataModel(
            message="OK",
            code=201,
            response_code="0001"
        )
        
        return generate_response(metaData=meta_data.dict(), data=response_data.dict())

    # daftar file
    async def list_files(self):
        try:
            files = self.backblaze_service.list_files()

            meta_data = MetaDataModel(
                message="OK",
                code=200,
                response_code="0000"
            )
            return generate_response(metaData=meta_data.dict(), data=files)

        except Exception as e:
            error_message = f"Error while fetching files: {str(e)}"
            return generate_error_response(message=error_message, code=500, response_code="0002")
    
    # donwload
    async def download_file(self, file_id: str):
        try:
            password = self._get_encryption_key()
            decrypted_data = self.backblaze_service.download_file(file_id, password )
            file_info = self.backblaze_service.bucket.get_file_info_by_id(file_id)
            original_filename = file_info.file_name
            
            return StreamingResponse(
                content=iter([decrypted_data]),
                media_type="application/octet-stream",
                headers={"Content-Disposition": f"attachment; filename={original_filename}"}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}") 
   